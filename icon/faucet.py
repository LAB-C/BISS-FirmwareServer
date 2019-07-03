from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.wallet.wallet import KeyWallet
import http3
import json
import time
import sys
import os.path

def filepath(filename):
    return os.path.join(sys.path[0], filename)

icon_service = IconService(HTTPProvider('https://bicon.net.solidwallet.io/api/v3'))
with open(filepath('secret.json'), 'r') as f:
    secret = json.load(f)
wallet = KeyWallet.load(filepath(secret['keystore']), secret['password'])
wallet_addr = wallet.get_address()

def wallet_status(address):
    return '{}: {}'.format(
        address,
        icon_service.get_balance(address) / 10 ** 18
    )

def get_block_height():
    return icon_service.get_block('latest')['height']

def request(address):
    try:
        res = http3.get(
            'http://icon-faucet-api.ibriz.ai/api/requesticx/{}'.format(address),
            timeout=5
        ).json()
        if not res['status']: # fail
            print(res['message'])
    except http3.exceptions.ReadTimeout: # success
        print(wallet_status(address))

def loop():
    block_height = 0
    while True:
        current_height = get_block_height()
        if (current_height > block_height + 30):
            request(wallet_addr)
            block_height = current_height
        time.sleep(10)

if __name__ == '__main__':
    print('Starting auto-faucet with wallet {}'.format(wallet_addr))
    loop()
