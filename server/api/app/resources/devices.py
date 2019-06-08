from server.api.app import app_api
from server.api.app.models.devices import DeviceListModel
from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc


@app_api.get('/devices')
@doc.summary('List of devices')
@doc.produces(
    DeviceListModel,
    content_type='application/json',
    description='Successful')
@doc.response(200, None, description='Success')
async def devices(request):
    devices = await request.app.db.devices.find({}).sort('_id').to_list(50)
    for idx, device in enumerate(devices):
        devices[idx]['_id'] = str(device['_id'])
    return res_json(devices)


@app_api.get('/devices/<wallet:string>')
@doc.summary('Get device infomation from wallet address')
@doc.response(200, None, description='Success')
@doc.response(404, None, description='No such device')
async def device_info(request, wallet):
    device = await request.app.db.devices.find_one({
        'wallet': wallet
    })
    if not device:
        abort(404)
    device['_id'] = str(device['_id'])
    return res_json(device)


@app_api.delete('/devices/<wallet:string>')
@doc.summary('Delete device from wallet address')
@doc.response(200, None, description='Success')
@doc.response(404, None, description='No such device')
async def device_info(request, wallet):
    res = await request.app.db.devices.delete_one({'wallet': wallet})
    if not res.acknowledged:
        abort(404)
    return res_json({})
