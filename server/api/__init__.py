from sanic import Blueprint
from server.api.app import app_api
from server.api.device import device_api

api = Blueprint.group(
    app_api,
    device_api
)
