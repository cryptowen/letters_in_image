# letters in image

A web API which can take an uploaded image(jpg, png) and find any letters in it. Powered by Django and google's Tesseract-OCR.

## Quickstart with docker and docker-compose

```sh
$ git clone git@github.com:huwenchao/letters_in_image.git
$ cd letters_in_image
$ docker-compose up

# in another console
$ cd path/to/the/project

# normal response
$ curl localhost:8000/letters_in_image/ -X POST -F image=@web/letters_in_image/test/test.png
{"content": ["T", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]}%

# error response
$ touch /tmp/a
$ curl localhost:8000/letters_in_image/ -X POST -F image=@/tmp/a
{"message": "file should be jpg/png image", "error_code": 5}%
```

## API 说明

- url: `/letters_in_image/`
- method: POST
- request params
	- `image`: 文件格式，png 或 jpg 图片, 大小不超过 5 MB
- response: JSON 格式
	- success: `{"content": ["A", "b"]}`，图片中出现的字母，仅包含a-zA-Z,已去重和排序
	- error: `{"message": "file should be jpg/png image", "error_code": 5}`，错误码和提示信息

## Development

Just edit the code in `/web`, the server will reload automatically.

## Test

```sh
$ docker-compose run web pytest
==================================================================== test session starts =====================================================================
platform linux2 -- Python 2.7.13, pytest-3.2.1, py-1.4.34, pluggy-0.4.0
Django settings: letters_in_image.settings_dev (from environment variable)
rootdir: /code, inifile: pytest.ini
plugins: mock-1.6.2, django-3.1.2
collected 6 items

letters_in_image/test/test_letters_in_image.py ......

================================================================== 6 passed in 1.99 seconds ==================================================================
```

## Interact with database

```sh
$ docker-compose run web ipython -i letters_in_image/mongodb.py
Python 2.7.13 (default, Jul 24 2017, 20:13:18)
Type "copyright", "credits" or "license" for more information.

IPython 5.4.1 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]: client
Out[1]: MongoClient(host=['db:27017'], document_class=dict, tz_aware=False, connect=True)

In [2]: records = list(client['db']['collection'].find())
```

## 其他说明

- DB 在此处非必要，仅做存储备用，并发量大后可能成为瓶颈，可以 sharding 或替换为消息队列，异步消费入库
- service 功能仅依赖 python 和 Tesseract-OCR, 理论上可以无限横向扩展

## References

- ocr
	- [pyocr](https://github.com/openpaperwork/pyocr)
	- [google's Tesseract-OCR](https://github.com/tesseract-ocr/tesseract)
- pytest
    - [pytest: helps you write better Django apps](https://speakerdeck.com/pelme/pytest-helps-you-write-better-django-apps)
    - [Getting started with pytest and pytest-django](https://pytest-django.readthedocs.io/en/latest/tutorial.html)
    - [pytest-mock](https://github.com/pytest-dev/pytest-mock)
    - [Python testing using mock and pytest](https://www.slideshare.net/surajssd009005/python-testing-using-mock-and-pytest)
- docker
	- [install tesseract in docker](https://hub.docker.com/r/joergpatz/tesseract/~/dockerfile/)
