import json

from django.http import HttpRequest

EM_INVALID_OR_MISSING_PARAMETERS = u'参数错误或缺失'


def fetch_parameter_dict(request: HttpRequest, request_type: str):
    if request_type == 'GET':
        parameter_dict = request.GET
    if request_type == 'POST':
        parameter_dict = request.POST
        if 'application/json' in request.META['CONTENT_TYPE']:
            parameter_dict = json.loads(request.body.decode('utf8'))
    return parameter_dict
