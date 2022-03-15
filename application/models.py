from .database import db
from sqlalchemy.sql import func
from flask_security import UserMixin, RoleMixin


class tracker_type(db.Model):
    __tablename__ = 'tracker_type'
    id = db.Column(db.Integer, autoincrement = True , primary_key = True)
    name = db.Column(db.String(55), unique = True)
    datatype = db.Column(db.String(15), unique = True)

class Tracker(db.Model):
    __tablename__ = 'tracker'
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String(100), unique = True)
    description = db.Column(db.String(255))
    tracker_type = db.Column(db.Integer , db.ForeignKey("tracker_type.id"))

class Settings(db.Model):
    __tablename__ = 'settings'
    __table_args__ = (
        db.UniqueConstraint("tracker_id", "value"),
    )
    tracker_id = db.Column(db.Integer, db.ForeignKey("tracker.id"), primary_key = True)
    value = db.Column(db.String(255), primary_key = True)

class Tracker_log(db.Model):
    __tablename__ = 'tracker_logs'
    id = db.Column(db.Integer,autoincrement = True, primary_key=True)
    tracker_id = db.Column(db.Integer,db.ForeignKey("tracker.id"))
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())
    value = db.Column(db.String(255))
    note = db.Column(db.String(255))

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username= db.Column(db.String(55))
    email = db.Column(db.String(55), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(55), unique = True)
    description = db.Column(db.String(255))

class Website(db.Model):
    __tablename__ = 'website_data'
    name = db.Column(db.String(55),primary_key=True)
    value = db.Column(db.String(255))
