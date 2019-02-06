from datetime import datetime, date

from django.contrib.auth.models import User
from django.utils.timezone import get_current_timezone
from api.models.program import Conference, Presentation
from api.models.program import Place, Category, Difficulty


def initialize():
    conference = Conference()
    conference.name_ko = '파이콘 한국 2019'
    conference.name_en = 'Pycon Korea 2019'
    conference.conference_started_at = date(2019, 8, 10)
    conference.conference_finished_at = date(2019, 8, 11)
    conference.sprint_started_at = date(2019, 8, 9)
    conference.sprint_finished_at = date(2019, 8, 9)
    conference.tutorial_started_at = date(2019, 8, 8)
    conference.tutorial_finished_at = date(2019, 8, 9)
    conference.save()

    user = User.objects.create_user(
        'testname', 'test@test.com', 'testpassword')
    category = Category.objects.create(
        name_ko='머신러닝', name_en='machine learning', slug='ML', visible=True)
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
    presentation.place = place
    presentation.accepted = False
    timezone = get_current_timezone()
    presentation.started_at = datetime(
        2019, 8, 21, 13, 00).astimezone(tz=timezone)
    presentation.finished_at = datetime(
        2019, 8, 21, 15, 00).astimezone(tz=timezone)
    presentation.category = category
    presentation.slide_url = 'https://slide/1'
    presentation.pdf_url = 'https://pdf/1'
    presentation.video_url = 'https://video/1'
    presentation.difficulty = difficulty
    presentation.recordable = True
    presentation.save()
