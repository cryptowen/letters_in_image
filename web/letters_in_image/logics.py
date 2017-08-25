# -*- coding: utf-8 -*-
from io import BytesIO
from PIL import Image
from string import ascii_letters as letters
from letters_in_image import util, mongodb
import logging
import datetime
from bson import Binary
import hashlib
from django.conf import settings


logger = logging.getLogger('letters_in_image')


class LettersInImage(object):

    letters_to_extract = set(letters)
    largest_image_size = 5 * 1024 * 1024

    # all the error messages
    no_image_data_err = {'error_code': 1, 'message': 'no image data'}
    image_too_large_err = {'error_code': 2, 'message': 'image can be no more than 5 MB'}
    wrong_format_err = {'error_code': 3, 'message': 'image can only be jpg/png format'}
    fail_to_ocr_err = {'error_code': 4, 'message': 'fail to extract data from image, please try again'}
    not_image_err = {'error_code': 5, 'message': 'file should be jpg/png image'}

    def __init__(self, raw_image):
        self.raw_image = raw_image

    def check_params(self):
        if not self.raw_image:
            return self.no_image_data_err

        self.image_data = b''.join(self.raw_image.chunks())
        if len(self.image_data) > self.largest_image_size:
            return self.image_too_large_err

        try:
            self.image_obj = Image.open(BytesIO(self.image_data))
        except Exception:
            logger.exception('fail to open file with PIL')
            return self.not_image_err

        if self.image_obj.format.lower() not in ['jpg', 'png', 'jpeg']:
            return self.wrong_format_err

    def response(self):
        check_res = self.check_params()
        if check_res:
            return check_res

        try:
            self.txt = util.image_to_string(self.image_obj)
        except Exception:
            logger.exception('fail to ocr from image')
            return self.fail_to_ocr_err

        self.content = sorted(set(self.txt) & self.letters_to_extract)
        res = {
            'content': self.content,
        }
        self.save_to_db()
        return res

    def save_to_db(self):
        try:
            md5 = hashlib.md5(self.image_data).hexdigest()
            d = {
                'contents': self.content,
                'ocr_txt': self.txt,
                'image': Binary(self.image_data),
                'create_time': datetime.datetime.now(),
                'md5': md5,
            }
            mongodb.client[settings.MONGO_DATABASE][settings.MONGO_COLLECTION].insert_one(d)
        except Exception:
            logger.exception('fail to save db')


