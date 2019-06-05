from server.api.device import device_api
from server.api.device.models.download import (
    DownloadRequestModel,
    DownloadResponseModel
)
from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from bson import ObjectId

@device_api.post('/download/<file_id:string>')
@doc.summary('Process firmware downloads')
@doc.consumes(DownloadRequestModel, content_type='application/json', location='body')
@doc.produces(DownloadResponseModel, content_type='application/json', description='Successful')
@doc.response(200, None, description='Success')
@doc.response(500, None, description='Error while execution')
async def download(request):
    return res_json({})
