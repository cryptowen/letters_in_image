# -*- coding: utf-8 -*-
import pyocr
import pyocr.builders

tool = pyocr.get_available_tools()[0]


def image_to_string(image):
    txt = tool.image_to_string(image, lang="eng", builder=pyocr.builders.TextBuilder())
    return txt
