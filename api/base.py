from flask import Response, request
from .BaseView import BaseView

def base():
    resp = Response(status=308)
    resp.headers['Location'] = request.url_root+'en'
    return resp

def home(language):
    return 'Hello world', 200