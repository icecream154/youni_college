from rpc_test.rpc_utils import do_rpc_post_request


def add_country(code: str, name_en: str, name_zh: str):
    return do_rpc_post_request('country/add', data={
        'code': code,
        'name_en': name_en,
        'name_zh': name_zh
    })


def add_region(country_info: str, name_en: str, name_zh: str):
    return do_rpc_post_request('region/add', data={
        'country_info': country_info,
        'name_en': name_en,
        'name_zh': name_zh
    })


def add_city(region_info: str, name_en: str, name_zh: str):
    return do_rpc_post_request('city/add', data={
        'region_info': region_info,
        'name_en': name_en,
        'name_zh': name_zh
    })