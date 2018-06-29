# dapli-server
![license](https://img.shields.io/badge/license-MIT-brightgreen.svg)
![python version](https://img.shields.io/badge/python-3.6-blue.svg)

Server for Dapli

## How to start
```bash
$ pip3 install django djangorestframework
$ git clone https://github/dapli-2018/dapli-server
$ cd dapli-server
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver 0.0.0.0:<port>
```


## API Reference

### Host

1. GroupPlaylist 생성

- url: group/host/
- method: POST
- request

|Data|Description|Type|
|---|---|---|
|songs|required|Array|
songs는 [[title, artist, album], ...] 형태의 이중 nested array

- response

|Name|Type|
|---|---|
|id|Number(Integer)|
|key|Number(Integer)|

- status code

|Code|Description|
|---|---|
|201|Success|
|412|Input data is wrong|
|503|Too many users. Wait a minute.|

-----

2. GroupPlaylist 제거

- url: group/host
- method: DELETE
- request

|Data|Description|Type|
|---|---|---|
|id|required|Number(Integer)|

- response : status code

- status code:

|Code|Description|
|---|---|
|200|Success|
|412|Input data is wrong|

-----

3. Indices 리스트 동기화

- url: group/host/
- method: GET
- request

|Data|Description|Type|
|---|---|---|
|id|required|Number(Integer)|

- response

|Name|Type|
|---|---|
|songs|Array|
songs는 [[title, is_on_playlist, is_played], ...] 형태의 이중 nested array

- status code:

|Code|Description|
|---|---|
|200|Success|
|412|Input data is wrong|


### Guest

1. GroupPlaylist 동기화: Host랑 동일

- url: group/guest/
- method: GET
- request

|Data|Description|Type|
|---|---|---|
|key|required|Number(Integer)|

- response

|Name|Type|
|---|---|
|id|Number(Integer)|
|songs|Array|
songs는 [[title, artist, album, is_on_playlist, is_played], ...] 형태의 이중 nested array

- status code:

|Code|Description|
|---|---|
|200|Success|

-----

2. GroupPlaylist 업데이트

- url: group/guest/
- method: PUT
- request

|Data|Description|Type|
|---|---|---|
|id|Number(Integer)|
|songs|required|Array|
songs는 [[title, artist, album, is_on_playlist, is_played], ...] 형태의 이중 nested array

- response : status code

- status code:

|Code|Description|
|---|---|
|200|Success|
|412|Input data is wrong|


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
