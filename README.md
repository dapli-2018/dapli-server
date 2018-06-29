# dapli-server
Server for Dapli

## API Reference

### Host

1. GroupPlaylist 생성

- url: /host
- method: POST
- request

|Data|Description|Type|
|---|---|---|
|songs|required|Array|
songs는 [[title, artist, album], ...] 형태의 이중 nested array

- response

|Name|Type|
|---|---|
|code|Number(Integer)|
|key|Number(Integer)|

- status code

|Code|Description|
|---|---|
|201|Success|
|412|Input data is wrong|
|503|Too many users. Wait a minute.|

-----

2. GroupPlaylist 제거

- url: /host
- method: DELETE
- request

|Data|Description|Type|
|---|---|---|
|key|required|Number(Integer)|

- response :

|Name|Type|
|---|---|
|code|Number(Integer)|

- status code:

|Code|Description|
|---|---|
|200|Success|
|412|Input data is wrong|

-----

3. Indices 리스트 동기화

- url: /host
- method: GET
- request

|Data|Description|Type|
|---|---|---|
|key|required|Number(Integer)|

- response

|Name|Type|
|---|---|
|code|Number(Integer)|
|songs|Array|
songs는 [[title, artist, album], ...] 형태의 이중 nested array

- status code:

|Code|Description|
|---|---|
|200|Success|
|412|Input data is wrong|
