import json

from django.http import HttpResponseBadRequest, HttpResponse

from youni_record.models.location import Country
from youni_record.utils.request_processor import fetch_parameter_dict, EM_INVALID_OR_MISSING_PARAMETERS
from youni_record.utils.retrive import get_entity_by_info


def add_country(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        code = parameter_dict['code']
        name_en = parameter_dict['name_en']
        name_zh = parameter_dict['name_zh']
    except KeyError:
        return HttpResponseBadRequest(json.dumps({'message': EM_INVALID_OR_MISSING_PARAMETERS}))

    country = Country(code=code, name_zh=name_zh, name_en=name_en)
    country.save()
    return HttpResponse(json.dumps({
        'message': 'add country success',
        'country': country.to_dict()
    }))


def query_countries(request):
    parameter_dict = fetch_parameter_dict(request, 'GET')
    language = parameter_dict.get('language', None)
    country_info = parameter_dict.get('country_info', None)
    country_info = None if country_info == '' else country_info

    if country_info:
        countries = []
        country = get_entity_by_info(country_info, Country)
        if country:
            countries.append(country.to_dict(language))
        return HttpResponse(json.dumps(countries))

    countries = []
    country_list = Country.objects.all()
    for country in country_list:
        countries.append(country.to_dict(language))
    return HttpResponse(json.dumps(countries))
