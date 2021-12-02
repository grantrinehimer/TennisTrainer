import os

from dotenv import load_dotenv
from flask import Flask
from flask import request
import json

from db import User
from db import db

app = Flask(__name__)

# load environment variables
load_dotenv()

ENV = "dev"
DB_NAME = str(os.environ.get("DB_NAME")).strip()
DB_USERNAME = str(os.environ.get("DB_USERNAME")).strip()
DB_PASSWORD = str(os.environ.get("DB_PASSWORD")).strip()

# To use on your local machine, you must configure postgres at port 5432 and put your credentials in your .env.
if ENV == "dev":
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"
    app.config["SQLALCHEMY_ECHO"] = True
else:
    app.config["SQLALCHEMY_ECHO"] = False
    # TODO: Configure prod environment

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
with app.app_context():
    db.create_all()


# Routes
def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


@app.route("/api/user/")
def get_players():
    return success_response(
        {"users": [u.serialize() for u in User.query.all()]}
    )


@app.route("/api/user/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    name = body.get("name")
    email = body.get("email")
    username = body.get("username")
    uType = body.get("uType")

    if name is None or email is None or username is None or uType is None:
        return failure_response("Did not provide required data.", 400)

    if uType != 0 and uType != 1:
        return failure_response("uType must be 0 (player) or 1 (coach)", 400)

    new_user = User(name=name, email=email, username=username, uType=uType)

    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)


@app.route("/api/user/<int:uid>/")
def get_user(uid):
    user = User.query.filter_by(uid=uid).first()
    if user is None:
        return failure_response("User not found.")
    return success_response(user.serialize())


"""
Request: NA
Response:
{
    url: www.something.m3u8
}
"""
@app.route("/api/media/<int:vid>")
def get_video_url(vid):
    pass

"""
Request:
{
    'filename': 'backhand.mp4',
    'uid': 5
}

Response:
{
    'url': 'https://s3.us-east-2.amazonaws.com/appdev-backend-final',
    'fields': 
    {
        'key': 'test2.jpg',
        'x-amz-algorithm': 'AWS4-HMAC-SHA256',
        'x-amz-credential': 'AKIAUNXPEGRSIPAECH7V/20211202/us-east-2/s3/aws4_request', 
        'x-amz-date': '20211202T032909Z', 
        'policy': 'eyJleHBpcmF0aW9uIjogIjIwMjEtMTItMDJUMDQ6Mjk6MDlaIiwgImNvbmRpdGlvbnMiOiBbeyJidWNrZXQiOiAiYXBwZGV2LWJhY2tlbmQtZmluYWwifSwgeyJrZXkiOiAidGVzdDIuanBnIn0sIHsieC1hbXotYWxnb3JpdGhtIjogIkFXUzQtSE1BQy1TSEEyNTYifSwgeyJ4LWFtei1jcmVkZW50aWFsIjogIkFLSUFVTlhQRUdSU0lQQUVDSDdWLzIwMjExMjAyL3VzLWVhc3QtMi9zMy9hd3M0X3JlcXVlc3QifSwgeyJ4LWFtei1kYXRlIjogIjIwMjExMjAyVDAzMjkwOVoifV19', 
        'x-amz-signature': 'e2bec138e2db65e361e60dbab614cced32f394bbe89c8d046bcc4caf50256237'
    }
}
"""
@app.route("/api/media/", methods=["POST"])
def get_video_upload_url():
    pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
