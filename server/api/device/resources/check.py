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
@doc.response(500, None, description='Error while execution')
async def check_update(request):
    return res_json({})

@device_api.post('/check/hash/<file_id:str>')
@doc.summary('Check firmware hash')
@doc.consumes(HashRequestModel, content_type='application/json', location='body')
@doc.response(200, None, description='Success')
@doc.response(500, None, description='Error while execution')
async def check_hash(request):
    return res_json({})
