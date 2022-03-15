from .database import db
from sqlalchemy.sql import func
from flask_security import UserMixin, RoleMixin


class Tracker_type(db.Model):
    __tablename__ = 'tracker_type'
    id = db.Column(db.Integer, autoincrement = True , primary_key = True)
    tracker_id = db.Column(db.Integer, db.ForeignKey("tracker.id"), nullable = False)
    datatype = db.Column(db.String(55), nullable = False)
    value = db.Column(db.String(255), nullable = True)
    

class Tracker(db.Model):
    __tablename__ = 'tracker'
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    settings = db.relationship('Settings', backref='tracker', cascade="all,delete")
    ttype = db.relationship('Tracker_type', backref='tracker', cascade="all,delete")

class Settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    tracker_id = db.Column(db.Integer, db.ForeignKey("tracker.id"), nullable = False)
    value = db.Column(db.String(255), nullable = False)

class Tracker_log(db.Model):
    __tablename__ = 'tracker_logs'
    id = db.Column(db.Integer,autoincrement = True, primary_key=True)
    tracker_id = db.Column(db.Integer,db.ForeignKey("tracker.id"), nullable = False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable = False)
    value = db.Column(db.String(255), nullable = False)
    note = db.Column(db.String(255))

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), nullable = False),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username= db.Column(db.String(55), nullable = False)
    email = db.Column(db.String(55), unique=True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    active = db.Column(db.Boolean(), nullable = False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(55), unique = True, nullable = False)
    description = db.Column(db.String(255), nullable = False)

class Website(db.Model):
    __tablename__ = 'website_data'
    name = db.Column(db.String(55),primary_key=True)
    value = db.Column(db.String(255), nullable = False)