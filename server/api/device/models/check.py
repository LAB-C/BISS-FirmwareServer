from sanic_openapi import doc

class UpdateRequestModel:
    wallet = doc.String('Device wallet address', required=True)

class UpdateResponseModel:
    update = doc.Boolean('Update status')
    txhash = doc.String('Transaction hash of key')
    file_id = doc.String('ID of firmware file')

class HashRequestModel:
    hash = doc.String('MD5 Hash of downloaded file', required=True)
    wallet = doc.String('Device wallet address', required=True)
