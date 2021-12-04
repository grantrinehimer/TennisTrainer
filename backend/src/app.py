#!/usr/bin/env python3

import json
import os
import boto3

from botocore.client import Config

from dotenv import load_dotenv
from flask import Flask
from flask import request
from werkzeug.utils import secure_filename

from media import *
import media

from db import User
from db import Upload
from db import Tag
from db import db

from google.oauth2 import id_token
from google.auth.transport import requests

app = Flask(__name__)

# load environment variables
load_dotenv()

# constants
ENV = "prod"
DB_NAME = str(os.environ.get("DB_NAME")).strip()
DB_USERNAME = str(os.environ.get("DB_USERNAME")).strip()
DB_PASSWORD = str(os.environ.get("DB_PASSWORD")).strip()
G_CLIENT_ID = str(os.environ.get("G_CLIENT_ID")).strip()
AWS_ACCESS_KEY_ID = str(os.environ.get("ACCESS_KEY_ID")).strip()
AWS_SECRET_ACCESS_KEY = str(os.environ.get("SECRET_ACCESS_KEY")).strip()
AWS_BUCKET_NAME = 'appdev-backend-final'
AWS_BUCKET_REGION_NAME = 'us-east-2'

# global Amazon S3 client
s3 = boto3.client('s3', region_name=AWS_BUCKET_REGION_NAME, 
                  endpoint_url=f'https://s3.{AWS_BUCKET_REGION_NAME}.amazonaws.com',
                  aws_access_key_id=AWS_ACCESS_KEY_ID, 
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  config=Config(signature_version='s3v4'))

# To use on your local machine, you must configure postgres at port 5432 and put your credentials in your .env.
if ENV == "dev":
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"
    app.config["SQLALCHEMY_ECHO"] = True
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = str(os.environ.get('DATABASE_URL')).replace("postgres", "postgresql")
    app.config["SQLALCHEMY_ECHO"] = False

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 512 # Don't accept files larger than 0.5GB
app.config['UPLOAD_EXTENSIONS'] = ['.mp4']
app.config['UPLOAD_PATH'] = 'tmp'

db.init_app(app)
with app.app_context():
    db.create_all()

# Routes
def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


@app.route("/api/user/authenticate/", methods=["POST"])
def authenticate_user():
    """
    Request:
    {
        "token": "{User's ID Token}"
    }
    Response:
    {
        "uid": {User's local id},
        "display_name": "{User's display name}",
        "email": "{User's email}"
        "uploads":
            [
                {
                    "vid": {video id},
                    "display_title": {display title of video}
                    "tags": [
                        {
                            "tid": 1,
                            "name": "backhand"
                        }
                        ...
                    ]
                }
                ...
            ]
    }
    """

    body = json.loads(request.data)
    token = body.get("token")

    if token is None:
        return failure_response("Could not get token from request body.", 400)

    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), G_CLIENT_ID)

        gid = idinfo["sub"]
        email = idinfo["email"]
        display_name = idinfo["name"]

        if gid is None or email is None or display_name is None:
            return failure_response("Could not retrieve required fields (Google Account ID, email, and name) from"
                                    "Google token. Unauthorized.", 401)

        user = User.query.filter_by(gid=gid).first()

        if user is None:
            # User does not exist, add them.
            user = User(gid=gid, display_name=display_name, email=email)
            db.session.add(user)
            db.session.commit()

        return success_response(user.serialize(), 200)
    except ValueError:
        return failure_response("Could not authenticate user. Unauthorized.", 401)


@app.route("/api/user/<int:uid>/media/")
def get_user_media(uid):
    """
    Request:
    Response:
    {
        "uploads": [
            {
                "vid": 1,
                "display_title": "{the new display title for the video}",
                "tags": [
                    {
                        "tid": 1,
                        "name": "backhand"
                    }
                ]
            }
        ]
    }
    """
    user = User.query.filter_by(uid=uid).first()
    if user is None:
        return failure_response("User not found.")
    return success_response(
        {"uploads": [u.serialize() for u in Upload.query.filter_by(uid=uid)]}
    )


@app.route("/api/media/<int:vid>/update-title/", methods=['POST'])
def update_upload_title(vid):
    """
    Request:
    {
        "new_title": "{the new display title for the video}" or None (keeps display title the same)
    }
    Response:
    {
        "vid": {video id},
        "display_title": {display title of video}
        "tags": [
            {
                "tid": 1,
                "name": "backhand"
            }
        ]
    }
    """

    upload = Upload.query.filter_by(vid=vid).first()

    if upload is None:
        return failure_response("Upload not found.")

    body = json.loads(request.data)

    new_title = body.get("new_title")

    if new_title is not None:
        upload.display_title = new_title

    db.session.commit()

    return success_response(upload.serialize())


@app.route("/api/media/<int:vid>/")
def get_video_url(vid):
    """
    Request: NA
    Response:
    {
        "url": "www.something.m3u8",
    }
    """
    upload = Upload.query.filter_by(vid=vid).first()

    if upload is None:
        return failure_response("Could not locate video id in database.")

    vkey = upload.vkey
    object_url = get_object_url(AWS_BUCKET_NAME, AWS_BUCKET_REGION_NAME, vkey)

    if object_url is None:
        return failure_response("Could not locate video in S3 bucket.")

    return success_response({'url': object_url})


@app.route("/api/media/", methods=["POST"])
def upload_video():
    """
    Request encoding = form-data:
    {
        'file': <FILEDATA>
        'filename': 'backhand.mp4',
        'display_title': 'Backhand Serve 12-2-2021',
        'uid': 5
    }
    Response encoding = JSON:
    {
        'vid': 4
    }
    """

    filename = request.form.get("filename")
    display_title = request.form.get("display_title")
    uid = request.form.get("uid")

    if filename is None or display_title is None or uid is None:
        return failure_response("Did not provide all requested fields.", 400)

    # Sanitize filename
    filename = secure_filename(filename)

    # Check if UID is int
    if not uid.isdigit():
        return failure_response("UID is not a number.", 400)

    uid = int(uid)

    if filename.isspace() or display_title.isspace() or uid < 0:
        return failure_response("Invalid fields.", 400)

    # Check for valid file
    # For security reference, see:
    # https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
    uploaded_file = request.files['file']
    file_ext = os.path.splitext(filename)[1]
    if file_ext not in app.config['UPLOAD_EXTENSIONS'] \
            or not verify_mp4_integrity(uploaded_file.stream):
        failure_response("Bad MP4.", 400)

    try:
        # Creates upload with vkey as filename and then changes it after using the new vid to make the vkey
        new_upload = Upload(vkey=filename, display_title=display_title, uid=uid)
        db.session.add(new_upload)
        db.session.flush()
        vid = new_upload.vid
        vkey = str(abs(hash(str(filename+str(uid)+str(vid)))))
        new_upload.vkey = vkey
        db.session.commit()
    except Exception as e:
        print(e)
        return failure_response("Error while trying to submit to database")

    try:
        # Save file to disk
        path_to_mp4 = os.path.join(app.config['UPLOAD_PATH'], vkey)
        uploaded_file.save(path_to_mp4)

        # Convert, compress, and upload file to AWS
        path_to_fmp4 = convert_mp4_to_hsl(path_to_mp4)
        compress_fmp4(path_to_fmp4)
        object_url = upload_to_aws(s3, AWS_BUCKET_NAME, AWS_BUCKET_REGION_NAME, path_to_fmp4)
        remove_fmp4(path_to_fmp4)
    except Exception as e:
        # Delete unsuccessful upload from database
        Upload.query.filter_by(vid=vid).delete()
        db.session.commit()
        print(e)
        return failure_response("Error while transferring video", 502)

    return success_response({'vid': vid})


@app.route("/api/media/<int:vid>/tag/", methods=['POST'])
def add_tag(vid):
    """
    Request:
    {
        "name": "backhand"
    }
    Response:
    {
        "vid": 1,
        "display_title": "{the new display title for the video}",
        "tags": [
            {
                "tid": 1,
                "name": "backhand"
            }
        ]
    }
    """
    upload = Upload.query.filter_by(vid=vid).first()
    if upload is None:
        return failure_response("Upload not found.")

    body = json.loads(request.data)
    name = body.get("name")

    if name is None:
        return failure_response("Could not get name from request.", 400)

    tag = Tag.query.filter_by(name=name).first()

    status_code = 200

    if tag is None:
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.flush()
        status_code = 201

    upload.tags.append(tag)
    db.session.commit()

    return success_response(upload.serialize(), status_code)


@app.route("/api/media/<int:vid>/tag/")
def get_tags(vid):
    """
    Request:
    Response:
    {
        "tags": [
            {
                "tid": 1,
                "name": "backhand"
            }
        ]
    }
    """
    upload = Upload.query.filter_by(vid=vid).first()
    if upload is None:
        return failure_response("Upload not found.")

    return success_response({"tags": [t.serialize() for t in upload.tags]})


@app.route("/api/media/<int:vid>/tag/<int:tid>/", methods=['DELETE'])
def delete_tag(vid, tid):
    """
    Request:
    Response:
    {
        "vid": 1,
        "display_title": "{the display title for the video}",
        "tags": []
    }
    """
    upload = Upload.query.filter_by(vid=vid).first()
    if upload is None:
        return failure_response("Upload not found.")

    upload.tags = [t for t in upload.tags if t.tid != tid]

    db.session.commit()

    return success_response(upload.serialize())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
