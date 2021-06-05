from django.urls import path

from youni_record.service.country import *
from youni_record.service.page import get_page
from youni_record.service.region import *
from youni_record.service.city import *
from youni_record.service.colleges import *

urlpatterns = [
    path('page', get_page, name='get_page'),
    path('country/add', add_country, name='add_country'),
    path('country/query', query_countries, name='query_countries'),
    path('region/add', add_region, name='add_region'),
    path('region/query', query_regions, name='query_regions'),
    path('region/delete', del_region, name='del_region'),
    path('city/add', add_city, name='add_city'),
    path('city/query', query_cites, name='query_cites'),
    path('city/delete', del_city, name='del_city'),
    path('college/add', add_college, name='add_college'),
    path('college/query', query_colleges, name='query_colleges'),
    path('college/delete', del_college, name='del_college'),
]