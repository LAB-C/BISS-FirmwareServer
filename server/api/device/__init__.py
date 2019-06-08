from sanic import Blueprint

device_api = Blueprint(
    'Device',
    url_prefix='/app',
    strict_slashes=True
)

__import__('server.api.device.resources.check')
__import__('server.api.device.resources.download')
