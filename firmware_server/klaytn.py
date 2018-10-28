import requests, subprocess

class Klaytn:
    def __init__(self, url):
        self.url = url
        self.header = {'Content-Type':'application/json'}
    
    def _request(self, method, jsonrp='2.0', params=[], id=1):
        return requests.post(self.url, headers=self.header, 
            json={'jsonrpc':jsonrp, 'method':method, 'params':params, 'id':id}
        ).json()

    def newAccount(self, passphrase):
        wallet = self._request('personal_newAccount', params=[passphrase])['result']
        print('[*]', requests.get('https://apiwallet.klaytn.com/faucet?address=' + wallet).text) # get first klay from faucet
        return wallet
    
    def unlockAccount(self, address, passphrase, duration):
        return True if self._request('personal_unlockAccount', params=[address, passphrase, duration])=='true' else False

    def sendData(self, wallet, data):
        print(wallet, data)
        output = subprocess.Popen(['node', 'firmware_server/send.js', wallet, '\'' + data + '\''], stdout=subprocess.PIPE ).communicate()[0]
        print(output)
        return output.strip().decode()
