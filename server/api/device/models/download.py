from sanic_openapi import doc

class DownloadRequestModel:
    key = doc.String('Firmware download key', required=True)

class DownloadResponseModel:
    url = doc.String('Firmware download URL')
