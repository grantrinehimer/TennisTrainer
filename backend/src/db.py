from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

tag_association_table = db.Table(
    "tag_association",
    db.Model.metadata,
    db.Column("vid", db.Integer, db.ForeignKey("upload.vid")),
    db.Column("tid", db.Integer, db.ForeignKey("tag.tid"))
)


# Player Table
class User(db.Model):
    __tablename__ = 'user'

    # Local User ID and Google Account ID combine to make primary key.
    uid = db.Column(db.Integer, primary_key=True)
    gid = db.Column(db.String, primary_key=True)
    display_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    uploads = db.relationship("Upload", cascade="delete")

    def __init__(self, **kwargs):
        self.gid = kwargs.get("gid")
        self.display_name = kwargs.get("display_name")
        self.email = kwargs.get("email")

    def serialize(self):
        return {
            "uid": self.uid,
            "display_name": self.username,
            "email": self.email,
            "uploads": [u.serialize() for u in self.uploads]
        }


# Player Uploads Table
class Upload(db.Model):
    __tablename__ = 'upload'
    vid = db.Column(db.Integer, primary_key=True)
    display_title = db.Column(db.String, nullable=False)
    vkey = db.Column(db.String, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey("user.uid"))
    tags = db.relationship("Tag", secondary=tag_association_table)

    def __init__(self, **kwargs):
        self.display_title = kwargs.get("display_title")
        self.vkey = kwargs.get("vkey")
        self.uid = kwargs.get("uid")

    def serialize(self):
        return {
            "vid": self.vid,
            "display_title": self.display_title,
            "tags": [t.serialize() for t in self.tags]
        }


# Global Tags Table
class Tag(db.Model):
    __tablename__ = "tag"
    tid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")

    def serialize(self):
        return {
            "tid": self.tid,
            "name": self.name
        }
