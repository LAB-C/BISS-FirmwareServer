from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = './firmware_server/static/files'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DATABASE.db'
app.logger.propagate = True

db = SQLAlchemy(app)

loginManager = LoginManager()
loginManager.init_app(app)

import firmware_server.views
