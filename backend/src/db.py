from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

teach_association_table = db.Table(
    "teach_association",
    db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)

student_association_table = db.Table(
    "student_association",
    db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)

# Player Table
class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    assignments = db.relationship("Assignment", cascade="delete")
    teachers = db.relationship("User", secondary=teach_association_table, back_populates="courses_teaching")
    students = db.relationship("User", secondary=student_association_table, back_populates="courses_learning")

    def __init__(self, **kwargs):
        self.code = kwargs.get("code")
        self.name = kwargs.get("name")

    def serialize(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "assignments": [a.serialize() for a in self.assignments],
            "instructors": [u.sub_serialize() for u in self.teachers],
            "students": [u.sub_serialize() for u in self.students]
        }

    def sub_serialize(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "assignments": [a.serialize() for a in self.assignments]
        }

    def sub_sub_serialize(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name
        }



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    courses_teaching = db.relationship("Course", secondary=teach_association_table, back_populates="teachers")
    courses_learning = db.relationship("Course", secondary=teach_association_table, back_populates="students")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.netid = kwargs.get("netid")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "courses": [c.sub_serialize() for c in self.courses_teaching + self.courses_learning]
        }

    def sub_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid
        }


class Assignment(db.Model):
    __tablename__ = 'assignment'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))

    def __init__(self, **kwargs):
        self.title = kwargs.get("title")
        self.due_date = kwargs.get("due_date")
        self.course_id = kwargs.get("course_id")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
            "course_id": Course.query.filter_by(id=self.course_id).first().sub_sub_serialize()
        }

#TODO: Join table and assignment table