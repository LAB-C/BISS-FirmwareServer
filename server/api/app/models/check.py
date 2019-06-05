from sanic_openapi import doc

class CheckRequestModel:
    wallet = doc.String('Device wallet address', required=True)

class CheckResponseModel:
    exist = doc.Boolean('Device register status')
