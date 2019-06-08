from sanic import Blueprint

app_api = Blueprint(
    'Application',
    url_prefix='/app',
    strict_slashes=True
)

__import__('server.api.app.resources.devices')
__import__('server.api.app.resources.register')
__import__('server.api.app.resources.upload')
