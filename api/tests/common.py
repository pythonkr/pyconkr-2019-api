from api.models.program import Conference


def create_conference(name='Conference', field='Conference Field'):
    return Conference.objects.create(name=name, conference_field=field)


def get_first_class_item_from_arr(arr, cls):
    items = [item for item in arr if isinstance(item, cls)]
    return items[0] if items else None
