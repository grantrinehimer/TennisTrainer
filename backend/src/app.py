import os

from flask import Flask
from flask import request
import json

from db import Course
from db import db
from db import User
from db import Assignment

app = Flask(__name__)
db_filename = "cms.db"

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


@app.route("/api/courses/")
def get_courses():
    return success_response(
        {"courses": [c.serialize() for c in Course.query.all()]}
    )


@app.route("/api/courses/", methods=["POST"])
def create_course():
    body = json.loads(request.data)
    code = body.get("code")
    name = body.get("name")
    if name is None or code is None:
        return failure_response("Did not provide required data.", 400)

    new_course = Course(code=code, name=name)

    db.session.add(new_course)
    db.session.commit()
    return success_response(new_course.serialize(), 201)


@app.route("/api/courses/<int:course_id>/")
def get_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found.")
    return success_response(course.serialize())


@app.route("/api/courses/<int:course_id>/", methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found.")
    db.session.delete(course)
    db.session.commit()
    return success_response(course.serialize())


@app.route("/api/courses/<int:course_id>/assignment/", methods=["POST"])
def create_assignment(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found.")

    body = json.loads(request.data)
    title = body.get("title")
    due_date = body.get("due_date")
    if title is None or due_date is None:
        return failure_response("Did not provide required data.", 400)

    new_assignment = Assignment(title=title, due_date=due_date, course_id=course_id)

    db.session.add(new_assignment)
    db.session.commit()
    return success_response(new_assignment.serialize(), 201)


@app.route("/api/users/", methods=['POST'])
def create_user():
    body = json.loads(request.data)
    name = body.get("name")
    netid = body.get("netid")
    if name is None or netid is None:
        return failure_response("Did not provide required data.", 400)

    new_user = User(name=name, netid=netid)

    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)


@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found.")
    return success_response(user.serialize())


@app.route("/api/courses/<int:course_id>/add/", methods=['POST'])
def add_user_to_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found.")

    body = json.loads(request.data)
    user_id = body.get("user_id")
    type = body.get("type")
    if user_id is None or not (type == "student" or type == "instructor"):
        return failure_response("Incorrect data provided.", 400)

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found.")

    if type == "student":
        course.students.append(user)
    else:
        course.teachers.append(user)

    db.session.commit()

    return success_response(course.serialize())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
