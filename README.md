# BISS Firmware Server
Upload firmware & hash 

1. 대시보드 서버에서 펌웨어 파일 받기(POST)

2. 키(`utils.randomKey()`) 랜덤으로 생성해서 블록체인에 넣기, key/route(이는 서버에서의 파일 위치)를 본 서버의 DB에 저장

3. `receipt`가 돌아오면 `txHash`를 해당 row에 추가

4. `file_id`로 구할 수 있는 public 링크에 정확한 key(`txHash`로 블록체인에서 구함)보내면 파일을 다운로드 받을 수 있음

## Upload
`/upload`

### request

```json
{
    "file": "binary data"
}
```

- `file`: 파일을 전송

### success

```json
{
    "success": {
        "file_id": 24, 
        "txhash": "0xf6e80595b78253241182e3c528147bd249d4e8a47ba3cecaee616057485262be"
    }
}
```

- `file_id`: 파일의 id. 디바이스에서 파일을 다운받을 public URL을 구할 때 사용한다.
- `txhash`: 트랜잭션의 hash. 디바이스에서 이를 사용해서 블록체인 상에 저장된 input data인 `key`를 받아올 수 있다.

### fail

```json
{
    "error": {
        "code": 405, 
        "message": "Wrong method; POST only"
    }
}
```

- `code`: error code
- `message`: error message


## Download
`download/{file_id}`

### request

```json
{
    "key" : "eDBrG0SxTbCxsj8LsrH8q8laR8M0zz"
}
```

- `key`: `txhash`를 통해 구한 `key`를 전송

### success

```json
{
    "result": {
        "url": "http://localhost/static/files/Uk5aGnq7snoQKhHRKkBn4wsACWzeXb6e38f16215ae91c11fc5c54b74c66d54/firmware.c"
    }
}
```

- `url`: private url

### fail

```json
{
    "error": {
        "code": 401,
        "message": "Wrong login credentials"
    }
}
```

- `code`: error code
- `message`: error message
