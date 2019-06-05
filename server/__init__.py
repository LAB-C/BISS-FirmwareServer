from sanic import Sanic, Blueprint
from sanic_openapi import swagger_blueprint, doc
from sanic_cors import CORS
from sanic_jwt_extended import JWTManager
from config import DevConfig

def create_app():
    _app = Sanic(__name__)
    _app.config.from_object(DevConfig)
    JWTManager(_app)
    CORS(_app)

    _app.blueprint(swagger_blueprint)

    from motor.motor_asyncio import AsyncIOMotorClient
    @_app.listener('before_server_start')
    def init(app, loop):
        _app.db = AsyncIOMotorClient(_app.config.MONGO_URI)[_app.config.MONGO_DB]

    from server.api import api
    _app.blueprint(api)

    return _app


app = create_app()
