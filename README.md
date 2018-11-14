# BISS Firmware Server
Upload firmware & hash 

1. Register device information(`name`, `wallet`) -> table `Device`

2. Upload firmware file, choose devices 

3. Put random key(`utils.random_key()`) in blockchain, save `key`/`route`(route is URL location in server)/`filehash` in DB -> table `File`

3. Append `txHash` in current file row when `receipt` returns

4. Server sends `txHash`, `file_id` to client API(client checks updates with certain time)

5. Client uses `file_id` and `txHash` to get public URL and can download file

6. Client hashes recived file and check with hash in server DB

7. When everything is perfect, Client updates firmware (AND PROFIT!!! ~~at last~~)
