from sanic_openapi import doc

class CheckResponseModel:
    exist = doc.Boolean('Device register status')
