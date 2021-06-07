import json

from django.http import HttpResponseBadRequest, HttpResponse

from youni_record.models.location import Region, City, Country
from youni_record.service.database_backup import backup
from youni_record.utils.request_processor import fetch_parameter_dict, EM_INVALID_OR_MISSING_PARAMETERS
from youni_record.utils.retrive import get_entity_by_info


@backup
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


@backup
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


def get_all_cities(language: str = None):
    city_list = []
    countries = Country.objects.all()
    for country in countries:
        city_list.extend(get_country_cities(country, language))
    return city_list


def get_region_cities(region: Region, language: str = None):
    city_list = []
    cities = region.city_set.all()
    for city in cities:
        city_list.append(city.to_dict(language))
    return city_list


def get_country_cities(country: Country, language: str = None):
    city_list = []
    regions = country.region_set.all()
    for region in regions:
        city_list.extend(get_region_cities(region, language))
    return city_list


def query_cites(request):
    parameter_dict = fetch_parameter_dict(request, 'GET')
    language = parameter_dict.get('language', None)
    country_info = parameter_dict.get('country_info', None)
    country_info = None if country_info == '' else country_info
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

    if region_info:
        region = get_entity_by_info(region_info, Region)
        if region:
            return HttpResponse(json.dumps(get_region_cities(region, language)))
        else:
            return HttpResponse(json.dumps([]))

    if country_info:
        country = get_entity_by_info(country_info, Country)
        if country:
            return HttpResponse(json.dumps(get_country_cities(country, language)))
        else:
            return HttpResponse(json.dumps([]))

    return HttpResponse(json.dumps(get_all_cities(language)))
