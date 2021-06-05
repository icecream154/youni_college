import json

from django.http import HttpResponseBadRequest, HttpResponse

from youni_record.models.location import Country, Region
from youni_record.utils.request_processor import fetch_parameter_dict, EM_INVALID_OR_MISSING_PARAMETERS
from youni_record.utils.retrive import get_entity_by_info


def add_region(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        country_info = parameter_dict['country_info']
        name_en = parameter_dict['name_en']
        name_zh = parameter_dict['name_zh']
    except KeyError:
        return HttpResponseBadRequest(json.dumps({'message': EM_INVALID_OR_MISSING_PARAMETERS}))

    country = get_entity_by_info(country_info, Country)
    if country:
        region = Region(country=country, name_zh=name_zh, name_en=name_en)
        region.save()
        return HttpResponse(json.dumps({
            'message': 'add country success',
            'region': region.to_dict()
        }))
    return HttpResponseBadRequest(json.dumps({'message': EM_INVALID_OR_MISSING_PARAMETERS}))


def del_region(request):
    parameter_dict = fetch_parameter_dict(request, 'POST')
    try:
        region_info = parameter_dict['region_info']
    except KeyError:
        return HttpResponseBadRequest(json.dumps({'message': EM_INVALID_OR_MISSING_PARAMETERS}))

    region = get_entity_by_info(region_info, Region)
    name_zh, name_en = region.name_zh, region.name_en
    if region:
        region.delete()
        return HttpResponse(json.dumps({
            'message': 'delete region [' + name_zh + '][' + name_en + '] success',
        }))


def query_regions(request):
    parameter_dict = fetch_parameter_dict(request, 'GET')
    language = parameter_dict.get('language', None)
    country_info = parameter_dict.get('country_info', None)
    country_info = None if country_info == '' else country_info
    region_info = parameter_dict.get('region_info', None)
    region_info = None if region_info == '' else region_info

    if region_info:
        regions = []
        region = get_entity_by_info(region_info, Region)
        if region:
            regions.append(region.to_dict(language))
        return HttpResponse(json.dumps(regions))

    if not country_info:
        regions = []
        region_list = Region.objects.all()
        for region in region_list:
            regions.append(region.to_dict(language))
        return HttpResponse(json.dumps(regions))
    else:
        country = get_entity_by_info(country_info, Country)
        if country:
            regions = []
            region_list = country.region_set
            for region in region_list:
                regions.append(region.to_dict(language))
            return HttpResponse(json.dumps(regions))
        else:
            return HttpResponse(json.dumps([]))
