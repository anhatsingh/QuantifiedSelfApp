from sqlalchemy.sql import func
from .database import db


class tracker_type(db.Model):
    __tablename__ = 'tracker_type'
    id = db.Column(db.Integer, autoincrement = True , primary_key = True)
    name = db.Column(db.String, unique = True)
    datatype = db.Column(db.String , unique = True)

class Tracker(db.Model):
    __tablename__ = 'tracker'
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String, unique = True)
    description = db.Column(db.String)
    tracker_type = db.Column(db.Integer , db.ForeignKey("tracker_type.id"))

class Settings(db.Model):
    __tablename__ = 'settings'
    __table_args__ = (
        db.UniqueConstraint("tracker_id", "value"),
    )
    tracker_id = db.Column(db.Integer, db.ForeignKey("tracker.id"), primary_key = True)
    value = db.Column(db.String, primary_key = True)

class Tracker_log(db.Model):
    __tablename__ = 'tracker_logs'
    id = db.Column(db.Integer,autoincrement = True, primary_key=True)
    tracker_id = db.Column(db.Integer,db.ForeignKey("tracker.id"))
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())
    value = db.Column(db.String)
    note = db.Column(db.String)

class Login_data(db.Model):
    __tablename__ = 'login_data'
    username= db.Column(db.String , primary_key = True)
    name = db.Column(db.String)
    password = db.Column(db.String)

class Website(db.Model):
    __tablename__ = 'website_data'
    name = db.Column(db.String,primary_key=True)
    value = db.Column(db.String)
