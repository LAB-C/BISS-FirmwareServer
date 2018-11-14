from flask_login import UserMixin
from firmware_server import db, loginManager
from datetime import datetime
from passlib.hash import pbkdf2_sha256

class Device(db.Model):
    __tablename__ = 'Device'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    wallet = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return '<Device %r>' % self.name
        
class File(db.Model):
    __tablename__ = 'File'
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String, unique=True, nullable=False)
    key = db.Column(db.String, unique=False, nullable=False)
    txhash = db.Column(db.String, unique=False)
    
    def __repr__(self):
        return '<File %r>' % self.route

db.create_all()
