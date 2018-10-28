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
klay = Klaytn('http://klaytn.ngrok.io')

@app.before_request
def session_config():
    session.permanent = True # permanent session

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # 파일경로와 랜덤키
            filename = secure_filename(file.filename)
            _dir = os.path.join(app.config['UPLOAD_FOLDER'], randomKey() + hash_string(filename) + '/')
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
                key = randomKey()
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
            # save file in blockchain, get txHash
            newfile.txhash = _txhash
        
            db.session.commit() 

            return json.dumps({'success': {'txhash': _txhash, 'file_id': newfile.id}}, sort_keys=True, indent=4)
        else:
            return json.dumps({'error': {'code': 400, 'message': 'No file'}}, sort_keys=True, indent=4)
    return json.dumps({'error': {'code': 405, 'message': 'Wrong method; POST only'}}, sort_keys=True, indent=4)

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