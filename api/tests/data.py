from django.contrib.auth.models import User
from api.models.programs import Presentation
from api.models.sponsors import Sponsor


def initialize():
    user = User.objects.create_user(
        'testname', 'test@test.com', 'testpassword')

    Presentation.objects.create(name='Graphql로 api를 만들어보자', owner=user)
    Presentation.objects.create(name='django로 웹 개발하기', owner=user)

    Sponsor.objects.create(
        slug = 'WADIZ_slug',
        name = 'WADIZ',
        desc = '크라우드펀딩 넘버원 와디즈',
        image = './',
        url = 'www.wadiz.co.kr',
        level = '5',
        paid_at = '2019-01-01',
        ticket_users =['test@test.com']
    )