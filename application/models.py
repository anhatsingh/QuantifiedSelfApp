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

class tracker_log(db.Model):
    __tablename__ = 'tracker_logs'
    id = db.Column(db.Integer,autoincrement = True, primary_key=True)
    tracker_id = db.Column(db.Integer,db.ForeignKey("tracker.id"))
    timestamp = db.Column(db.datetime)
    value = db.Column(db.String)
    note = db.Column(db.String)

class login_data(db.Model):
    __tablename__ = 'login_data'
    username= db.Column(db.String , primary_key = True)
    name = db.Column(db.String)
    password = db.Column(db.string)

class debug_logs(db.Model):
    __tablename__ = 'debug_logs'
    id = db.Column(db.Integer,primary_key= True,autoincrement= True)
    username = db.Column(db.string,db.ForeignKey("login_data.username"))
    timestamp = db.Column(db.datetime)
    description = db.column(db.string)

class website(db.Model):
    name = db.Column(db.string,primary_key=True)
    value = db.Column(db.string)
