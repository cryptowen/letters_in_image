# -*- coding: utf-8 -*-
import os
from django.test import Client
import json
import StringIO
import pytest

url = '/letters_in_image/'


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
    assert data['error_code'] == 3


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
    dir = os.path.dirname(__file__)
    params = {'image': open(os.path.join(dir, image_path))}
    response = client.post(url, params)
    assert response.status_code == 200
    data = json.loads(response.content)
    print(data)
    assert data['content'] == content
