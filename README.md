# BISS Firmware Server
![index screenshot](./assets/index.png)

Upload firmware and update IoT device

## 1. 디바이스 정보 등록
Register device information(`name`, `wallet`) -> table `Device`

### Web
http://0.0.0.0/register

### API
POST, `/register`

```json
{
    "name": "somedevice1", 
    "wallet": "0x75a59b94889a05c03c66c3c84e9d2f8308ca4abd"
}
```

## 2. 펌웨어 업로드, 업로드할 디바이스 선택
Upload firmware file, choose devices 

### Web
http://0.0.0.0/upload

### API
POST, `/upload`

```json
{
    "file": file,
    "devices": ["somedevice1", "somedevice2", "somedevice3"]
}
```

## 3. 블록체인에 랜덤 키 넣고 전송, DB에 파일 키와 URL, 해시 저장
Put random key(`utils.random_key()`) in blockchain, save `key`/`route`(route is URL location in server)/`filehash` in DB -> table `File`

## 3. receipt가 돌아오면 txHash를 해당 row에 추가
Append `txHash` in current file row when `receipt` returns

## 4. Server sends `txHash`, `file_id` to client API(client checks updates with certain time)
내일 client API를 만들자

## 5. Client uses `file_id` and `txHash` to get public URL and can download file

## 6. Client hashes recived file and check with hash in server DB
이때 success 로그가 남음(나중에 7단계로 옮기자)

### API
POST, `/check/<file_id>`

```json
{
    "hash": "4e6e424c9e2c7ff4386616cba7bd6b8f"
}
```

## 7. When everything is perfect, Client updates firmware (AND PROFIT!!! ~~at last~~)
