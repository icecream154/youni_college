import sys

from bs4 import BeautifulSoup

from rpc_test.rpc_request import *


def fetch_name_and_code(item, default_name: str, default_code: str):
    try:
        return item['name'], item['code']
    except KeyError:
        print('default name %s and code %s fetched' % (default_name, default_code))
        return default_name, default_code


def load_loc_xml(path: str):
    country_dict = {}
    region_dict = {}
    city_dict = {}

    with open(path, 'r') as f:
        en_data = f.read()

    loc_xml = BeautifulSoup(en_data, 'lxml').find('location')
    for country in loc_xml.find_all('countryregion'):
        country_name, country_code = fetch_name_and_code(country, '', '')
        # print('Country name: %s and Country code: %s' % (country_name, country_code))
        country_dict[country_code] = country_name
        for region in country.find_all('state'):
            region_name, region_code = fetch_name_and_code(region, country_name, country_code)
            # print('Region name: %s and Region code: %s' % (region_name, region_code))
            region_dict[region_code] = region_name
            for city in region.find_all('city'):
                city_name, city_code = fetch_name_and_code(city, region_name, region_code)
                # print('City name: %s and City code: %s' % (city_name, city_code))
                city_dict[city_code] = city_name

    return country_dict, region_dict, city_dict


def load_loc_zh_xml():
    pass


if __name__ == '__main__':
    # en_country_dict, en_region_dict, en_city_dict = load_loc_xml('LocList-en.xml')
    zh_country_dict, zh_region_dict, zh_city_dict = load_loc_xml('LocList.xml')

    with open('LocList-en.xml', 'r') as f:
        en_data = f.read()

    loc_xml = BeautifulSoup(en_data, 'lxml').find('location')
    for country in loc_xml.find_all('countryregion'):
        country_name, country_code = fetch_name_and_code(country, '', '')
        # print('Country name: %s and Country code: %s' % (country_name, country_code))
        add_country(country_code, country_name, zh_country_dict[country_code])
        for region in country.find_all('state'):
            region_name, region_code = fetch_name_and_code(region, country_name, country_code)
            # print('Region name: %s and Region code: %s' % (region_name, region_code))
            add_region(country_name, region_name, zh_region_dict[region_code])
            for city in region.find_all('city'):
                city_name, city_code = fetch_name_and_code(city, region_name, region_code)
                # print('City name: %s and City code: %s' % (city_name, city_code))
                status_code, _ = add_city(region_name, city_name, zh_city_dict[city_code])
                if status_code != 200:
                    print(city_name + ' ' + zh_city_dict[city_code])
                    sys.exit()
