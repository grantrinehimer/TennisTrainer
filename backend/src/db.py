from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Player Table
class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    # 0 = player, 1 = coach
    uType = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")
        self.username = kwargs.get("username")
        self.uType = kwargs.get("uType")

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "username": self.username,
            "uType": self.uType
        }


# Player Uploads Table
class Upload(db.Model):
    __tablename__ = 'upload'
    vid = db.Column(db.Integer, primary_key=True)
    display_title = db.Column(db.Integer, nullable=False)
    vkey = db.Column(db.String, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey("user.uid"))

    def __init__(self, **kwargs):
        self.vid = kwargs.get("vid")
        self.display_title = kwargs.get("display_title")
        self.vkey = kwargs.get("vkey")

    # TODO: Serialize if needed
