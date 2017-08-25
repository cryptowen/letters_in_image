# -*- coding: utf-8 -*-
import os
from django.test import Client
import json
import StringIO
import pytest

url = '/letters_in_image/'
dir = os.path.dirname(__file__)


def test_no_image(client):
    response = client.post(url)
    assert response.status_code == 200
    data = json.loads(response.content)
    print(data)
    assert data['error_code'] == 1


def test_large_file(client):
    params = {'image': StringIO.StringIO('a' * 6 * 2**20)}
    response = client.post(url, params)
    assert response.status_code == 200
    data = json.loads(response.content)
    print(data)
    assert data['error_code'] == 2


def test_wrong_format(client):
    params = {'image': StringIO.StringIO('a' * 4 * 2**20)}
    response = client.post(url, params)
    assert response.status_code == 200
    data = json.loads(response.content)
    print(data)
    assert data['error_code'] == 5


def test_fail_to_ocr(client, mocker):
    m = mocker.patch('letters_in_image.util.image_to_string')
    m.side_effect = Exception("fail to orc")
    params = {'image': open(os.path.join(dir, 'test.png'))}
    response = client.post(url, params)
    assert response.status_code == 200
    data = json.loads(response.content)
    print(data)
    assert data['error_code'] == 4


@pytest.mark.parametrize(
    'image_path, content', [
        (
            'test.png', [
                u'T', u'a', u'b', u'c', u'd', u'e', u'f', u'g', u'h', u'i', u'j', u'k', u'l', u'm', u'n', u'o', u'p',
                u'q', u'r', u's', u't', u'u', u'v', u'w', u'x', u'y', u'z'
            ]
        ),
        (
            'test-european.jpg', [
                u'A', u'C', u'D', u'E', u'F', u'H', u'L', u'O', u'T', u'a', u'b', u'c', u'd', u'e', u'f', u'g', u'h',
                u'i', u'j', u'k', u'l', u'm', u'n', u'o', u'p', u'q', u'r', u's', u't', u'u', u'v', u'w', u'x', u'y',
                u'z'
            ]
        ),
    ]
)
def test_normal(client, image_path, content):
    params = {'image': open(os.path.join(dir, image_path))}
    response = client.post(url, params)
    assert response.status_code == 200
    data = json.loads(response.content)
    print(data)
    assert data['content'] == content
