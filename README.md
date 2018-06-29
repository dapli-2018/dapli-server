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
|title|required|String|
|Author|required|String|
|Content|required|String|
|tag|required|String|

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



### Keygen

1. key 가져오기 by id

- url: group/keygen
- method: GET
- request:

|Data|Description|Type|
|---|---|---|
|id|Required|Number(Integer)|

- response : status code

|Code|Description|
|---|---|
|200|Success|
|404|Key does not exist|
|412|Input data is wrong|

-----

2. key 발급

- url: group/keygen
- method: POST
- request:

|Data|Description|Type|
|---|---|---|
|id|Required|Number(Integer)|

- response : status code

|Code|Description|
|---|---|
|201|Created|
|412|Input data is wrong|

-----

3. 키 만료

- url: group/keygen
- method: DELETE
- request:

|Data|Description|Type|
|---|---|---|
|key|required|Number(Integer)|

- response : status code

|Code|Description|
|---|---|
|200|Success|



### ImageView

1. playlist image 가져오기

- url: group/image
- method: GET
- request:

| Data | Description | Type            |
| ---- | ----------- | --------------- |
| id   | required    | Number(Integer) |

- response : status code and JSON

|Name|Type|
|---|---|
|image|String(url of image)|

- status code

| Code | Description |
| ---- | ----------- |
| 200  | Success     |

-----

2. playlist image 업로드

- url: group/image
- method: POST
- request: **multipart/form-data** (JSON 아님 주의)

| Data  | Description | Type            |
| ----- | ----------- | --------------- |
| id    | required    | Number(Integer) |
| image | required    | image(jpg)      |

- response : status code

| Code | Description |
| ---- | ----------- |
| 200  | Success     |



### Newsfeed

1. newsfeed

- url: group/newsfeed
- method: GET
- request: None
- response: JSON

```json
[
    {
        "id": 1,
        "title": "Hello Dapli",
        "author": "",
        "date": "2018-06-29T22:58:28.415651+09:00",
        "content": "Hello world and my friends.",
        "tag": "#echo"
    },
    ... 이하 생략
]
```



### Playlist Detail

1. playlist

- url: group/playlist
- method: GET
- request: 

| Data | Description | Type            |
| ---- | ----------- | --------------- |
| id   | required    | Number(Integer) |

- response: JSON

```json
[
    {
        "title": "The Middle",
        "artist": "Zedd",
        "album": "The Middle",
        "is_on_playlist": true,
        "is_played": false
    },
    ... 이하 생략
]
```







## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
