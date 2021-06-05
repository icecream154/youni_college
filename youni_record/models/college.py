from django.db import models

from youni_record.models.location import City


class College(models.Model):
    college_id = models.AutoField(primary_key=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    sort = models.IntegerField(default=0)
    name_en = models.CharField(max_length=100)
    name_zh = models.CharField(max_length=100)

    def to_dict(self, language: str):
        if language == 'en':
            dictionary = {
                'college_id': self.college_id,
                'name': self.name_en,
                'city_id': self.city.city_id,
                'city_name': self.city.name_en,
                'region_id': self.city.region.region_id,
                'region_name': self.city.region.name_en,
                'country_id': self.city.region.country.country_id,
                'country_name': self.city.region.country.name_en,
                'sort': self.sort
            }
            return dictionary
        elif language == 'zh':
            dictionary = {
                'college_id': self.college_id,
                'name': self.name_zh,
                'city_id': self.city.city_id,
                'city_name': self.city.name_zh,
                'region_id': self.city.region.region_id,
                'region_name': self.city.region.name_zh,
                'country_id': self.city.region.country.country_id,
                'country_name': self.city.region.country.name_zh,
                'sort': self.sort
            }
            return dictionary
        else:
            dictionary = {
                'college_id': self.college_id,
                'city_id': self.city.city_id,
                'region_id': self.city.region.region_id,
                'country_id': self.city.region.country.country_id,
                'name_zh': self.name_zh,
                'city_name_zh': self.city.name_zh,
                'region_name_zh': self.city.region.name_zh,
                'country_name_zh': self.city.region.country.name_zh,
                'name_en': self.name_zh,
                'city_name_en': self.city.name_zh,
                'region_name_en': self.city.region.name_zh,
                'country_name_en': self.city.region.country.name_zh,
                'sort': self.sort
            }
            return dictionary
