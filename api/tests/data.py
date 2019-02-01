from datetime import datetime

from django.contrib.auth.models import User
from django.utils.timezone import get_current_timezone
from api.models.program import Conference, Presentation
from api.models.program import Place, Category, Difficulty


def initialize():
    user = User.objects.create_user(
        'testname', 'test@test.com', 'testpassword')
    Conference.objects.create(name='Pycon Korea 2018')
    category = Category.objects.create(
        name='machine learning', slug='ML', visible=True)
    difficulty = Difficulty.objects.create(name_en='beginner', name_ko='초급')

    place = Place.objects.create(name='101')

    presentation = Presentation()

    presentation.language = Presentation.LANGUAGE_KOREAN
    presentation.name_ko = 'Graphql로 api를 만들어보자'
    presentation.name_en = 'Make api using Graphql'
    presentation.desc_ko = 'Graphql은 아주 훌륭한 도구입니다'
    presentation.desc_en = 'Graphql is very good package.'
    presentation.owner = user
    presentation.price = 0
    presentation.visable = False
    presentation.room = place
    presentation.accepted = False
    timezone = get_current_timezone()
    presentation.started_at = datetime(2017, 8, 21, 13, 00, tzinfo=timezone)
    presentation.finished_at = datetime(2017, 8, 21, 15, 00, tzinfo=timezone)
    presentation.category = category
    presentation.slide_url = 'https://slide/1'
    presentation.pdf_url = 'https://pdf/1'
    presentation.video_url = 'https://video/1'
    presentation.difficulty = difficulty
    presentation.recordable = True
    presentation.save()
