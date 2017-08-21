# -*- coding: utf-8 -*-
from PIL import Image
import pyocr
import pyocr.builders
from string import letters

tool = pyocr.get_available_tools()[0]
letters_set = set(letters)


def image_to_string(image):
    txt = tool.image_to_string(image, lang="eng", builder=pyocr.builders.TextBuilder())
    return txt


def letters_in_image(image):
    txt = image_to_string(image)
    res = sorted(set(txt) & letters_set)
    return res


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
    # test_image_to_string_png()
    # test_image_to_string_jpg()
    image = Image.open('test/test-european.jpg')
    txt = image_to_string(image)
    print(txt)
    letters = letters_in_image(image)
    print(letters)
