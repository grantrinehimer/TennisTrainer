import os

from flask import Flask
from flask import request
import json

from db import User
from db import db

app = Flask(__name__)
db_filename = "tennisTrainer.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


# your routes here
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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
