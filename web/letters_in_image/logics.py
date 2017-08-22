# -*- coding: utf-8 -*-
from cStringIO import StringIO
from PIL import Image
from string import letters
import util
import logging


logger = logging.getLogger('letters_in_image')


class LettersInImage(object):

    letters_to_extract = set(letters)
    largest_image_size = 5 * 1024 * 1024

    # all the error messages
    no_image_data_err = {'error_code': 1, 'message': 'no image data'}
    image_too_large_err = {'error_code': 2, 'message': 'image can be no more than 5 MB'}
    wrong_format_err = {'error_code': 3, 'message': 'image can only be jpg/png format'}
    fail_to_ocr_err = {'error_code': 4, 'message': 'fail to extract data from image, please try again'}

    def __init__(self, raw_image):
        self.raw_image = raw_image

    def check_params(self):
        if not self.raw_image:
            return self.no_image_data_err

        image_data = ''.join(self.raw_image.chunks())
        if len(image_data) > self.largest_image_size:
            return self.image_too_large_err

        try:
            self.image_obj = Image.open(StringIO(image_data))
        except Exception:
            logger.exception('fail to open file with PIL')
            return self.wrong_format_err

        if self.image_obj.format.lower() not in ['jpg', 'png', 'jpeg']:
            return self.wrong_format_err

    def response(self):
        check_res = self.check_params()
        if check_res:
            return check_res

        try:
            txt = util.image_to_string(self.image_obj)
        except Exception:
            logger.exception('fail to ocr from image')
            return self.fail_to_ocr_err

        l = sorted(set(txt) & self.letters_to_extract)
        res = {
            'content': l,
        }
        return res
