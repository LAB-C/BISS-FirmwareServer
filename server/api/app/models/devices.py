from sanic_openapi import doc


class DeviceModel:
    name = doc.String('Device name', required=True)
    wallet = doc.String('Device wallet address', required=True)


class DeviceListModel:
    devices: doc.List(DeviceModel)
