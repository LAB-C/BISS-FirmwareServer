from sanic_openapi import doc


class UploadRequestModel:
    devices = doc.List(doc.String, 'List of device names', required=True)
