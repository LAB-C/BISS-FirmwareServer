from firmware_server.klaytn import Klaytn
import os.path, json, requests

import logging
logging.basicConfig(level=logging.INFO)

klay = Klaytn('http://ubuntu.hanukoon.com:8551/')

def make_info():
    wallet = klay.newAccount('_labc')
    info = {
        'wallet': wallet
    }
    logging.info(info)
    klay.unlockAccount(wallet, '_labc', 30000)
    logging.info('Unlocked wallet: ' + wallet)
    with open('./info.json', 'w') as f:
        json.dump(info, f, indent=4)
    return info

if __name__ == '__main__':
    if not os.path.isfile('./info.json'): # 존재 x
        logging.debug('info.json: file not found -> calling make_info()')
        info = make_info()
    else:
        try:
            with open('./info.json', 'r') as f:
                logging.debug('info.json: file found')
                info = json.load(f)
                logging.info(info)
                wallet = info['wallet']
                logging.info('Wallet: ' + wallet)

                klay.unlockAccount(wallet, '_labc', 30000)
                logging.info('Unlocked wallet: ' + wallet)
        except:
            logging.debug('info.json: parsing error -> calling make_info()')
            info = make_info()

    print('[*] Finish')
