from flask_login import UserMixin
from firmware_server import db, loginManager
from datetime import datetime
from passlib.hash import pbkdf2_sha256

class Device(db.Model):
    __tablename__ = 'Device'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    wallet = db.Column(db.String, unique=True, nullable=False)
    update = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Device %r>' % self.name
        
class File(db.Model):
    __tablename__ = 'File'
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String, unique=True, nullable=False)
    key = db.Column(db.String, unique=False, nullable=False)
    hash = db.Column(db.String, unique=False)
    txhash = db.Column(db.String, unique=False)
    
    def __repr__(self):
        return '<File %r>' % self.route

class Log(db.Model):
    __tablename__ = 'Log'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String, nullable=False)
    type = db.Column(db.String)
    json = db.Column(db.PickleType())

    def __repr__(self):
        return '<Log %r>' % self.timestamp

db.create_all()
