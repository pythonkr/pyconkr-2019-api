from django.contrib.auth.models import User
from api.models import Presentation


def initialize():
    user = User.objects.create_user(
        'testname', 'test@test.com', 'testpassword')
    Presentation.objects.create(name='Graphql로 api를 만들어보자', owner=user)
    Presentation.objects.create(name='django로 웹 개발하기', owner=user)
