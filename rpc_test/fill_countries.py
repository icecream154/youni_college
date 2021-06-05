from rpc_test.rpc_utils import *


def load_country_json():
    with open('countries.json', 'r') as f:
        raw_content = f.read()
    # load_dict = json.loads(raw_content)
    # print(load_dict)
    return json.loads(raw_content)['countries']


def add_country(code: str, name_en: str, name_zh: str):
    return do_rpc_post_request('country/add', data={
        'code': code,
        'name_en': name_en,
        'name_zh': name_zh
    })


if __name__ == '__main__':
    country_list = load_country_json()
    for country_raw in country_list:
        code, name_en, name_zh = country_raw['code'], country_raw['name'], country_raw['cname']
        if code == '' or name_zh == '' or name_en == '':
            continue
        status_code, response_dict\
            = add_country(code, name_en, name_zh)
        show_info(status_code, response_dict)
