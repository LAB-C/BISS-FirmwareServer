from server.api.app import app_api
from server.api.app.models.devices import DeviceModel
from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
import time


@app_api.post('/register')
@doc.summary('Register device')
@doc.consumes({
    'payload': DeviceModel
}, content_type='application/json', location='body')
@doc.response(200, None, description='Success')
@doc.response(200, None, description='Not valid wallet address')
@doc.response(500, None, description='Error while registration')
async def register(request):
    wallet = request.json['wallet']
    if len(wallet) != 42:
        abort(404)

    # register device
    device = {
        'name': request.json['name'],
        'wallet': wallet,
        'update': None
    }
    res = await request.app.db.devices.insert_one(device)
    if not res.acknowledged:
        abort(500)

    # save log
    log = {
        'type': 'register',
        'timestamp': int(time.time()),
        'json': {
            'name': device['name'],
            'wallet': device['wallet']
        }
    }
    await request.app.db.logs.insert_one(log)
    # error handling is not necessary for logging

    return res_json({})  # 200
