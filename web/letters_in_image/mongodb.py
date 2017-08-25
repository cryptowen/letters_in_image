# -*- coding: utf-8 -*-
from pymongo import MongoClient
from django.conf import settings

client = MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)
