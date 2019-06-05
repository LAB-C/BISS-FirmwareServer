from server.api.app import app_api
from server.api.app.models.check import CheckRequestModel, CheckResponseModel
from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from bson import ObjectId

@app_api.post('/check')
@doc.summary('Check device registeration')
@doc.consumes(CheckRequestModel, content_type='application/json', location='body')
@doc.produces(CheckResponseModel, content_type='application/json', description='Successful')
@doc.response(200, None, description='Success')
@doc.response(500, None, description='Error while execution')
async def check(request):
    return res_json({
      'exist': True
    })
