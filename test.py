import requests, json
# file = {
#     'file':open('run.py')
# }

r = requests.post('http://localhost/upload', files={'file':1})
data = json.loads(r.text)
print(data)

# # data['success']['txhash'] -> block input -> get key 

# r = requests.post('http://localhost/download/3', json={'key' : 'eDBrG0SxTbCxsj8LsrH8q8laR8M0zz'})
# print(r.text)
