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
import time

@device_api.post('/check/update')
@doc.summary('Check update for device')
@doc.consumes(UpdateRequestModel, content_type='application/json', location='body')
@doc.produces(UpdateResponseModel, content_type='application/json', description='Successful')
@doc.response(200, None, description='Success')
@doc.response(404, None, description='No such device')
@doc.response(500, None, description='Error while execution or no update found')
async def check_update(request):
    # find device with given wallet
    device = await request.app.db.devices.find_one({
        'wallet': request.json['wallet']
    })
    if not device:
        abort(404)

    # return update info if available
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
async def check_hash(request, file_id):
    # find update with given fileId
    update = await request.app.db.updates.find_one({
        'fileId': ObjectId(file_id)
    })
    if not update:
        abort(404)

    # validation failed
    if update.hash != request.json['hash']:
        abort(400)

    # update device status
    res = await request.app.db.devices.update({
        'wallet': request.json['wallet']
    }, {
        '$set': { 'update': None }
    })
    if not res.acknowledged:
        abort(404)

    # log success
    log = {
        'type': 'success',
        'timestamp': int(time.time()),
        'json': {
            'route': update['route'],
            'hash': update['hash']
        }
    }
    await request.app.db.logs.insert_one(log)
    
    return res_json({})
