from firmware_server.database import *
from firmware_server.utils import *
from flask import (
    render_template,
    redirect,
    request,
    url_for,
    Blueprint
)
from urllib.parse import urljoin
from datetime import date, datetime, timedelta
import os, os.path, json

api = Blueprint('api', __name__)

@api.route('/register', methods=['GET', 'POST'])
def api_register(): # when move to blueprint in future, change method name to 'register'
    # name, wallet
    if request.method == 'POST':
        wallet = request.json.get('wallet')
        if len(wallet) != 42:
            return json.dumps({'error': 'Not vaild wallet address'})
        newdevice = Device(
            name=request.json.get('name'),
            wallet=wallet,
            update=0
        )
        db.session.add(newdevice)
        db.session.commit()
        newlog = Log(
            type='register',
            timestamp=datetime.now().strftime('%Y-%m-%d'),
            json={
                'name':newdevice.name, 
                'wallet':newdevice.wallet, 
                'timestamp':datetime.now()
            }
        )
        db.session.add(newlog)
        db.session.commit()
        return json.dumps({'success' : {'name': newdevice.name, 'wallet': newdevice.wallet}})
    return json.dumps({'error': 'Method Not Allowed'})

@api.route('/download/<file_id>', methods=['GET', 'POST'])
def download(file_id):
    if request.method == 'POST':
        try:
            file_id = int(file_id)
        except:
            return json.dumps({'error': {'code': 400, 'message': 'No '}}, sort_keys=True, indent=4)        
        # check if credentials are vaild
        key = request.json['key']
        thisfile = File.query.get(file_id)
        if key == thisfile.key:
            return json.dumps({'result': {
                'url': urljoin(
                    request.url_root,
                    thisfile.route.replace('firmware_server', '')
                )
            }}, sort_keys=True, indent=4)
        return json.dumps({'error': {'code': 401, 'message': 'Wrong login credentials'}}, sort_keys=True, indent=4)
    return json.dumps({'error': 'Method Not Allowed'})    

@api.route('/check/exist', methods=['GET', 'POST'])
def check_exist():
    if request.method == 'POST':
        device = Device.query.filter_by(wallet=request.json.get('wallet')).first()
        if not device:
            return json.dumps({ 'exist': False }, indent=4)        
        return json.dumps({ 'exist': True }, indent=4)
    return json.dumps({'error': 'Method Not Allowed'})    
    
@api.route('/check/update', methods=['GET', 'POST'])
def check_update():
    if request.method == 'POST':
        device = Device.query.filter_by(wallet=request.json.get('wallet')).first()
        if device.update == 0: # nothing to update
            return json.dumps({'update': False}, indent=4)
        updated = File.query.get(device.update)
        return json.dumps({
            'update': True,
            'txHash': updated.txhash, 
            'file_id': updated.id
        }, sort_keys=True, indent=4)
    return json.dumps({'error': 'Method Not Allowed'})    
    
@api.route('/check/hash/<file_id>', methods=['GET', 'POST'])
def check_hash(file_id):
    if request.method == 'POST':
        file_id = int(file_id)
        thisfile = File.query.get(file_id)
        if thisfile.hash != request.json.get('hash'):
            return json.dumps({'equal': False})

        # log success
        newlog = Log(
            type='success',
            timestamp=datetime.now().strftime('%Y-%m-%d'),
            json={
                'route': thisfile.route,
                'hash': thisfile.hash,
                'timestamp':datetime.now()
            }
        )
        db.session.add(newlog)
        db.session.commit()

        device = Device.query.filter_by(wallet=request.json.get('wallet')).first()
        if device.update == thisfile.id:
            device.update = 0
        db.session.commit()

        return json.dumps({'equal': True})
    return json.dumps({'error': 'Method Not Allowed'})    
    