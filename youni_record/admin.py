from django.contrib import admin

# Register your models here.
from youni_record.models.college import College
from youni_record.models.location import *

admin.site.register(Country)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(College)
