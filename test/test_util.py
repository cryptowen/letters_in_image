# -*- coding: utf-8 -*-
from PIL import Image
from util import image_to_string


def test_image_to_string_png():
    image = Image.open('test.png')
    txt = image_to_string(image)
    print(txt)

if __name__ == "__main__":
    test_image_to_string_png()



