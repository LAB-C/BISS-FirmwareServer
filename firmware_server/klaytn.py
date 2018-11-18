import requests, subprocess, json

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
        output = subprocess.Popen(['node', 'firmware_server/send.js', wallet, data, self.url], stdout=subprocess.PIPE ).communicate()[0]
        print(output)
        if 'Error' in str(output):
            return False
        return output.strip().decode()
    
    def getInputData(self, txhash):
        url = 'https://apiscope.klaytn.com/api/transaction/' + txhash
        res = json.loads(requests.get(url).text)
        print(res)
        if res['status'] == 'FAIL': 
            return False
        return bytes.fromhex(res['result']['input'][2:]).replace(b'\x00', b'').replace(b'6F\xd0! \x1e', b'').decode()
