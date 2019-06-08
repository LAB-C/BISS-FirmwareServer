from server.api.app import app_api
from server.api.app.utils import hash_string, hash_file, random_key
from server.api.app.models.upload import UploadRequestModel
from sanic.exceptions import abort
from sanic.response import json as res_json
from sanic_openapi import doc
from bson import ObjectId
import os
import os.path


@app_api.post('/upload')
@doc.summary('Upload device firmware')
@doc.consumes(
    UploadRequestModel,
    content_type='application/json',
    location='body')
@doc.response(200, None, description='Success')
@doc.response(500, None, description='Error while execution')
async def upload(request):
    print(request.files)
    file = request.files.get('file')
    upload_dir = os.path.join(
        request.app.config['UPLOAD_FOLDER'],
        random_key() + hash_string(file.name) + '/')

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    route = os.path.join(upload_dir, file.name)
    with open(route, 'wb') as _f:
        _f.write(file.body)

    update = {
        'route': route,
        'key': random_key(),
        'hash': hash_file(route)
    }

    # TODO: send update.key to blockchain and receive txHash
    update['txHash'] = 'test'

    # save update
    res = await request.app.db.updates.insert_one(update)
    if not res.acknowledged:
        abort(500)
    
    # update device
    devices = request.json.get('devices')
    for device in devices:
        await request.app.db.devices.update({
            'name': device
        }, {
            '$set': { 'update': update['key'] }
        })

    # save log
    log = {
        'route': update['route'],
        'hash': update['hash'],
        'time': int(time.time())
    }
    await request.app.db.logs.insert_one(log)

    return res_json({
        'id': res.inserted_id,
        'txHash': update['txHash']
    })
