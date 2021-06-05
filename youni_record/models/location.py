from django.db import models


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10)
    name_en = models.CharField(max_length=100, unique=True)
    name_zh = models.CharField(max_length=100, unique=True)
    sort = models.IntegerField(default=0)

    def to_dict(self, language: str = None):
        if language == 'en':
            dictionary = {
                'country_id': self.country_id,
                'code': self.code,
                'name': self.name_en,
                'sort': self.sort
            }
            return dictionary
        elif language == 'zh':
            dictionary = {
                'country_id': self.country_id,
                'code': self.code,
                'name': self.name_zh,
                'sort': self.sort
            }
            return dictionary
        else:
            dictionary = {
                'country_id': self.country_id,
                'code': self.code,
                'name_zh': self.name_zh,
                'name_en': self.name_en,
                'sort': self.sort
            }
            return dictionary


class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name_en = models.CharField(max_length=100, unique=True)
    name_zh = models.CharField(max_length=100, unique=True)
    sort = models.IntegerField(default=0)

    def to_dict(self, language: str = None):
        if language == 'en':
            dictionary = {
                'region_id': self.region_id,
                'name': self.name_en,
                'country_id': self.country.country_id,
                'country_name': self.country.name_en,
                'sort': self.sort
            }
            return dictionary
        elif language == 'zh':
            dictionary = {
                'region_id': self.region_id,
                'name': self.name_zh,
                'country_id': self.country.country_id,
                'country_name': self.country.name_zh,
                'sort': self.sort
            }
            return dictionary
        else:
            dictionary = {
                'region_id': self.region_id,
                'name_zh': self.name_zh,
                'name_en': self.name_en,
                'country_id': self.country.country_id,
                'country_name_zh': self.country.name_zh,
                'country_name_en': self.country.name_en,
                'sort': self.sort
            }
            return dictionary


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name_en = models.CharField(max_length=100, unique=True)
    name_zh = models.CharField(max_length=100, unique=True)
    sort = models.IntegerField(default=0)

    def to_dict(self, language: str = None):
        if language == 'en':
            dictionary = {
                'city_id': self.city_id,
                'name': self.name_en,
                'region_id': self.region.region_id,
                'region_name': self.region.name_en,
                'country_id': self.region.country.country_id,
                'country_name': self.region.country.name_zh,
                'sort': self.sort
            }
            return dictionary
        elif language == 'zh':
            dictionary = {
                'city_id': self.city_id,
                'name': self.name_zh,
                'region_id': self.region.region_id,
                'region_name': self.region.name_zh,
                'country_id': self.region.country.country_id,
                'country_name': self.region.country.name_zh,
                'sort': self.sort
            }
            return dictionary
        else:
            dictionary = {
                'city_id': self.city_id,
                'name_zh': self.name_zh,
                'name_en': self.name_en,
                'region_id': self.region.region_id,
                'region_name_zh': self.region.name_zh,
                'region_name_en': self.region.name_en,
                'country_id': self.region.country.country_id,
                'country_name_zh': self.region.country.name_zh,
                'country_name_en': self.region.country.name_en,
                'sort': self.sort
            }
            return dictionary
