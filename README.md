# Firmware Server
Upload firmware & hash 

1. 희원섭에서 파일 받기(POST)

2. 랜덤한 키(`utils.randomKey()`)를 생성해서 블록체인에 넣기, 키/txHash/파일경로를 내 DB에 저장

3. 파일의 다운로드 링크(찐)를 만들기, 해당 row에 추가

4. public 링크를 만듦 -> 여기서 정확한 key가 들어오면 다운로드 링크로 연결

## 