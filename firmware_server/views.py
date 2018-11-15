from firmware_server import app
from firmware_server.database import *
from firmware_server.utils import *
from flask import (
    render_template,
    redirect,
    request,
    url_for,
    session
)
from flask_login import (
    current_user, 
    login_user,
    logout_user,
    login_required
)
from werkzeug import secure_filename
from urllib.parse import urljoin
import os, os.path, json

from firmware_server.klaytn import *
klay = Klaytn('http://ubuntu.hanukoon.com:8551/')

@app.before_request
def session_config():
    session.permanent = True # permanent session

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # name, wallet
    if request.method == 'POST':
        wallet = request.form.get('wallet')
        if len(wallet) != 42:
            return 'Not vaild wallet address'
        try:
            newdevice = Device(
                name=request.form.get('name'),
                wallet=wallet
            )
            db.session.add(newdevice)
            db.session.commit()
        except:
            return 'Error'
        return 'Success<br>name: ' + newdevice.name + '<br>wallet: ' + newdevice.wallet
    return render_template('register.html')
    
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # list of devices, file
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # 파일경로와 랜덤키
            filename = secure_filename(file.filename)
            _dir = os.path.join(app.config['UPLOAD_FOLDER'], random_key() + hash_string(filename) + '/')
            print(app.config['UPLOAD_FOLDER'])
            print(_dir)
            if not os.path.exists(_dir):
                os.makedirs(_dir)
                print(_dir)
            _route = os.path.join(_dir + filename)
            print(_route)

            file.save(_route)
            newfile = File(
                route = _route,
                key = random_key(),
                hash = hash_file(_route)
            )
        
            db.session.add(newfile)
            db.session.commit()
            
            # 트랜잭션 해시
            with open('./firmware_server/static/config.json') as f:
                json_data = json.loads(f.read())
                wallet = json_data['wallet']
                passphrase = json_data['passphrase']
            klay.unlockAccount(wallet, passphrase, 3000)
            print(wallet, newfile.key)
            _txhash = klay.sendData(wallet, newfile.key)
            if not _txhash:
                return json.dumps({'error': {'code': 500, 'message': 'Error while sending'}}, sort_keys=True, indent=4)
            # save file in blockchain, get txHash
            newfile.txhash = _txhash
        
            db.session.commit() 

            return json.dumps({'success': {'txhash': _txhash, 'file_id': newfile.id}}, sort_keys=True, indent=4)
        else:
            return json.dumps({'error': {'code': 400, 'message': 'No file'}}, sort_keys=True, indent=4)
    return render_template('upload.html', devices=Device.query.all())

@app.route('/download/<file_id>', methods=['POST'])
def download(file_id):
    file_id = int(file_id)
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

@app.route('/check/<file_id>/<file_hash>', methods=['POST'])
def check(file_id):
    file_id = int(file_id)
    thisfile = File.query.get(file_id)
    if thisfile.hash != file_hash:
        return 'False'
    return 'True'
    