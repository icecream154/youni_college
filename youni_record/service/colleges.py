import json

from django.http import HttpResponse, HttpResponseBadRequest

from youni_record.models.college import College
from youni_record.models.location import *
from youni_record.utils.request_processor import fetch_parameter_dict, EM_INVALID_OR_MISSING_PARAMETERS
from youni_record.utils.retrive import get_entity_by_info


def get_all_colleges(language: str = None):
    college_list = []
    countries = Country.objects.all()
    for country in countries:
        college_list.extend(get_country_colleges(country, language))
    return college_list


def get_city_colleges(city: City, language: str = None):
    college_list = []
    colleges = city.college_set.all()
    for college in colleges:
        college_list.append(college.to_dict(language))
    return college_list


def get_region_colleges(region: Region, language: str = None):
    college_list = []
    cities = region.city_set.all()
    for city in cities:
        college_list.extend(get_city_colleges(city, language))
    return college_list


def get_country_colleges(country: Country, language: str = None):
    college_list = []
    regions = country.region_set.all()
    for region in regions:
        college_list.extend(get_region_colleges(region, language))
    return college_list


def query_colleges(request):
    parameter_dict = fetch_parameter_dict(request, 'GET')
    language = parameter_dict.get('language', None)
    country_info = parameter_dict.get('country_info', None)
    country_info = None if country_info == '' else country_info
    region_info = parameter_dict.get('region_info', None)
    region_info = None if region_info == '' else region_info
    city_info = parameter_dict.get('city_info', None)
    city_info = None if city_info == '' else city_info

    if country_info:
        country = get_entity_by_info(country_info, Country)
        if country:
            return HttpResponse(json.dumps(get_country_colleges(country, language)))
        else:
            return HttpResponse(json.dumps([]))

    if region_info:
        region = get_entity_by_info(region_info, Region)
        if region:
            return HttpResponse(json.dumps(get_country_colleges(region, language)))
        else:
            return HttpResponse(json.dumps([]))

    if city_info:
        city = get_entity_by_info(city_info, City)
        if city:
            return HttpResponse(json.dumps(get_country_colleges(city, language)))
        else:
            return HttpResponse(json.dumps([]))

    return HttpResponse(json.dumps(get_all_colleges(language)))


def add_college(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        city_info = parameter_dict['city_info']
        name_en = parameter_dict['name_en']
        name_zh = parameter_dict['name_zh']
    except KeyError:
        return HttpResponseBadRequest(json.dumps({'message': EM_INVALID_OR_MISSING_PARAMETERS}))

    city = get_entity_by_info(city_info, City)
    if city:
        college = College(city=city, name_zh=name_zh, name_en=name_en)
        college.save()
        return HttpResponse(json.dumps({
            'message': 'add college success',
            'college': college.to_dict()
        }))
    return HttpResponseBadRequest(json.dumps({'message': EM_INVALID_OR_MISSING_PARAMETERS}))


def del_college(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        college_info = parameter_dict['college_info']
    except KeyError:
        return HttpResponseBadRequest(json.dumps({'message': EM_INVALID_OR_MISSING_PARAMETERS}))
    college = get_entity_by_info(college_info, College)
    name_zh, name_en = college.name_zh, college.name_en
    if college:
        college.delete()
        return HttpResponse(json.dumps({
            'message': 'delete college [' + name_zh + '][' + name_en + '] success',
        }))
