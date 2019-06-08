# BISS Firmware Server

## Workflow
1. **\*** - Check existence and Register device
2. **Application** - Upload firmware file, with device names to update2
3. **Server**
   1. Write random file key in blockchain
   2. Save file ID, file key, file hash and download URL to DB
   3. Update document with transaction hash when the receipt returns
   4. Provide API with update status(with transaction hash and file ID) or emit some event to device
4. **Device** - check for updates
   1. Use the transaction hash to get the file key from the blockchain
   2. Send found key with the file ID to server and receive the download URL
   3. Download the firmware from the recieved URL
5. **Device** - validation of downloaded firmware
   1. Calculate the MD5 sum of the file and send validation request to server
   2. Server compares the hash and (if correct) mark the upload as complete, respond to client
   3. Device updates itself if the response is valid

## API
- Application
  - check
    - exist
  - register 
  - upload
- Device
  - check
    - update
    - hash
  - download

## Models

### Device
```json
{
    "_id": "string",
    "name": "string",
    "wallet": "string",
    "update": "string"
}
```

### File
```json
{
    "_id": "string",
    "route": "string",
    "key": "string",
    "hash": "string",
    "txHash": "string"
}
```

### Log
```json
{
    "_id": "string",
    "timestamp": 0,
    "type": "string",
    "json": {}
}
```
