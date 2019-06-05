from server.api.app import app_api
from server.api.app.models.register import RegisterRequestModel
from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from bson import ObjectId

@app_api.post('/register')
@doc.summary('Register device')
@doc.consumes(RegisterRequestModel, content_type='application/json', location='body')
@doc.response(200, None, description='Success')
@doc.response(500, None, description='Error while execution')
async def register(request):
    return res_json({})
