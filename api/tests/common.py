from api.models import Conference, Tutorial, Sprint, Youngcoder, Exercise


def create_conference(name='Conference', field='Conference Field'):
    return Conference.objects.create(name=name, conference_field=field)


def create_tutorial(name='Tutorial', field='Tutorial Field'):
    return Tutorial.objects.create(name=name, tutorial_field=field)


def create_sprint(name='Sprint'):
    return Sprint.objects.create(name=name)


def create_youngcoder(name='Youngcoder'):
    return Youngcoder.objects.create(name=name)


def create_exercise(name='Exercise'):
    return Exercise.objects.create(name=name)


def get_first_class_item_from_arr(arr, cls):
    items = [item for item in arr if isinstance(item, cls)]
    return items[0] if items else None
