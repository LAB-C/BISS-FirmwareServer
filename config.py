import os


class Config(object):
    API_VERSION = '1.3.1'
    API_TITLE = 'BISS Firmware Server API'
    API_DESCRIPTION = 'Provides API for updating BISS devices'

    JWT_TOKEN_LOCATION = 'headers'
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_SECRET_KEY = os.urandom(24)

    UPLOAD_FOLDER = './server/static/files'
    MONGO_URI = ''


class DevConfig(Config):
    HOST = 'localhost'
    PORT = 5000
    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017'
    MONGO_DB = 'biss'
