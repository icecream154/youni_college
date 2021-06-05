from django.db.models import Q


def get_entity_by_info(info: str, location_model):
    try:
        location_id = int(info)
        location_object = location_model.objects.get(pk=location_id)
        return location_object
    except ValueError:
        pass
    except location_model.DoesNotExist:
        return None

    location_objects = location_model.objects.filter(Q(name_en=info) | Q(name_zh=info))
    if len(location_objects) > 0:
        return location_objects[0]
    return None


