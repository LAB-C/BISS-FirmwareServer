from server.api.device import device_api
from server.api.device.models.check import (
    UpdateRequestModel, 
    UpdateResponseModel,
    HashRequestModel
)
from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from bson import ObjectId

@device_api.post('/check/update')
@doc.summary('Check update for device')
@doc.consumes(UpdateRequestModel, content_type='application/json', location='body')
@doc.produces(UpdateResponseModel, content_type='application/json', description='Successful')
@doc.response(200, None, description='Success')
@doc.response(404, None, description='No such device')
@doc.response(500, None, description='Error while execution or no update found')
async def check_update(request):
    wallet = request.json['wallet']
    device = await request.app.db.devices.find_one({
        'wallet': wallet
    })
    if not device:
        abort(404)

    if device['update']:
        update = await request.app.db.updates.find_one({
            '_id': ObjectId(device['update'])
        })
        if not update:
            abort(500)
        return res_json({
            'update': True,
            'id': str(update['_id']),
            'txHash': update['txHash'],
        })
    return res_json({
        'update': False
    })

@device_api.post('/check/hash/<file_id:str>')
@doc.summary('Check firmware hash')
@doc.consumes(HashRequestModel, content_type='application/json', location='body')
@doc.response(200, None, description='Success')
@doc.response(500, None, description='Error while execution')
async def check_hash(request):
    return res_json({})
