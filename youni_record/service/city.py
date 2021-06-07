import json

from django.http import HttpResponseBadRequest, HttpResponse

from youni_record.models.location import Region, City
from youni_record.utils.request_processor import fetch_parameter_dict, EM_INVALID_OR_MISSING_PARAMETERS
from youni_record.utils.retrive import get_entity_by_info


def add_city(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        region_info = parameter_dict['region_info']
        name_en = parameter_dict['name_en']
        name_zh = parameter_dict['name_zh']
    except KeyError:
        return HttpResponseBadRequest(json.dumps({'message': EM_INVALID_OR_MISSING_PARAMETERS}))

    print('[region]: %s [city_en]: %s [city_zh]: %s' % (region_info, name_en, name_zh))
    region = get_entity_by_info(region_info, Region)
    if region:
        city = City(region=region, name_zh=name_zh, name_en=name_en)
        city.save()
        return HttpResponse(json.dumps({
            'message': 'add country success',
            'city': city.to_dict()
        }))
    return HttpResponseBadRequest(json.dumps({'message': EM_INVALID_OR_MISSING_PARAMETERS}))


def del_city(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        city_info = parameter_dict['city_info']
    except KeyError:
        return HttpResponseBadRequest(json.dumps({'message': EM_INVALID_OR_MISSING_PARAMETERS}))
    city = get_entity_by_info(city_info, City)
    if city:
        name_zh, name_en = city.name_zh, city.name_en
        city.delete()
        return HttpResponse(json.dumps({
            'message': 'delete city [' + name_zh + '][' + name_en + '] success',
        }))
    return HttpResponseBadRequest(json.dumps({'message': EM_INVALID_OR_MISSING_PARAMETERS}))


def query_cites(request):
    parameter_dict = fetch_parameter_dict(request, 'GET')
    language = parameter_dict.get('language', None)
    region_info = parameter_dict.get('region_info', None)
    region_info = None if region_info == '' else region_info
    city_info = parameter_dict.get('city_info', None)
    city_info = None if city_info == '' else city_info

    if city_info:
        cities = []
        city = get_entity_by_info(city_info, City)
        if city:
            cities.append(city.to_dict(language))
        return HttpResponse(json.dumps(cities))

    if not region_info:
        cities = []
        city_list = City.objects.all()
        for city in city_list:
            cities.append(city.to_dict(language))
        return HttpResponse(json.dumps(cities))
    else:
        region = get_entity_by_info(region_info, Region)
        if region:
            cities = []
            city_list = region.city_set
            for city in city_list:
                cities.append(city.to_dict(language))
            return HttpResponse(json.dumps(cities))
        else:
            return HttpResponse(json.dumps([]))
