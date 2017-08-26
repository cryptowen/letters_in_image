# -*- coding: utf-8 -*-
from django.http import JsonResponse, HttpResponse
from . import logics


def index(request):
    msg = '''visit
    '''
    return HttpResponse(msg)


def letters_in_image(request):
    raw_image = request.FILES.get('image')
    res = logics.LettersInImage(raw_image=raw_image).response()
    return JsonResponse(res)
