from sanic_openapi import doc

class RegisterRequestModel:
    name = doc.String('Device name', required=True)
    wallet = doc.String('Device wallet address', required=True)
