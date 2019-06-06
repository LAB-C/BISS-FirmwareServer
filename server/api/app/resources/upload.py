from server.api.app import app_api
from server.api.app.models.upload import UploadRequestModel
from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from bson import ObjectId


@app_api.post('/upload')
@doc.summary('Upload device firmware')
@doc.consumes(
    UploadRequestModel,
    content_type='application/json',
    location='body')
@doc.response(200, None, description='Success')
@doc.response(500, None, description='Error while execution')
async def upload(request):
    return res_json({})
