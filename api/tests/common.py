from unittest import mock
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser


def get_first_class_item_from_arr(arr, cls):
    items = [item for item in arr if isinstance(item, cls)]
    return items[0] if items else None


def generate_mock_response(
        status=200,
        content='',
        json=None,
        raise_for_status=None):
    mock_resp = mock.Mock()
    mock_resp.raise_for_status = mock.Mock()
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status
    mock_resp.json.return_value = json
    mock_resp.status_code = status
    if json:
        mock_resp.content = str(json)
    else:
        mock_resp.content = content

    return mock_resp


def generate_request_authenticated(user):
    request = RequestFactory().get('/')
    SessionMiddleware().process_request(request)
    request.session.save()
    request.user = user

    return request


def generate_request_anonymous():
    request = RequestFactory().get('/')
    SessionMiddleware().process_request(request)
    request.session.save()
    request.user = AnonymousUser()
    return request
