# -*- coding: utf-8 -*-
from PIL import Image
import pyocr
import pyocr.builders

tool = pyocr.get_available_tools()[0]


def image_to_string(image):
    txt = tool.image_to_string(image, lang="eng", builder=pyocr.builders.TextBuilder())
    return txt


def test_image_to_string_png():
    image = Image.open('test/test.png')
    txt = image_to_string(image)
    print(txt)
    assert txt

def test_image_to_string_jpg():
    image = Image.open('test/test-european.jpg')
    txt = image_to_string(image)
    print(txt)
    assert txt


if __name__ == "__main__":
    test_image_to_string_png()
    test_image_to_string_jpg()
