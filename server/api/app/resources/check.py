from server.api.app import app_api
from server.api.app.models.check import CheckResponseModel
from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from bson import ObjectId

@app_api.get('/check/<wallet:string>')
@doc.summary('Check device registeration')
@doc.produces(CheckResponseModel, content_type='application/json', description='Successful')
@doc.response(200, None, description='Success')
@doc.response(404, None, description='No such device')
@doc.response(500, None, description='Error while execution')
async def check(request, wallet):
    try:
        device = await request.app.db.devices.find_one({
            'wallet': wallet
        })
        if not device:
            abort(404)
        return res_json({})
    except:
        abort(500)
