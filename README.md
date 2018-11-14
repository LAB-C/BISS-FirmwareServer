# BISS Firmware Server
Upload firmware & hash 

1. 디바이스 정보 등록<br>
Register device information(`name`, `wallet`) -> table `Device`

2. 펌웨어 업로드, 업로드할 디바이스 선택<br>
Upload firmware file, choose devices 

3. 블록체인에 랜덤 키 넣고 전송, DB에 파일 키와 URL, 해시 저장<br>
Put random key(`utils.random_key()`) in blockchain, save `key`/`route`(route is URL location in server)/`filehash` in DB -> table `File`

3. receipt가 돌아오면 txHash를 해당 row에 추가<br>
Append `txHash` in current file row when `receipt` returns

4. Server sends `txHash`, `file_id` to client API(client checks updates with certain time)

5. Client uses `file_id` and `txHash` to get public URL and can download file

6. Client hashes recived file and check with hash in server DB

7. When everything is perfect, Client updates firmware (AND PROFIT!!! ~~at last~~)
