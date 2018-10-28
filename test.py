import requests, json
file = {
    'file':open('run.py')
}

r = requests.post('http://localhost/upload', files=file)
data = json.loads(r.text)

# data['success']['txhash'] -> block input -> get key 

r = requests.post('http://localhost/download/' + str(data['success']['file_id']), json={'key' : 'wrongkey'})
print(r.text)
