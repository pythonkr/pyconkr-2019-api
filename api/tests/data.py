from datetime import datetime, date
from PIL import Image
from django.contrib.auth.models import User

from django.utils.timezone import get_current_timezone
from api.models.oauth_setting import OAuthSetting
from api.models.program import Conference, Presentation
from api.models.program import Place, Category, Difficulty
from api.models.sponsor import Sponsor, SponsorLevel


TIMEZONE = get_current_timezone()


def initialize():
    # initialize_conference()
    # initialize_oauthsetting()
    user = initialize_user()
    initialize_sponsor(user)
    initialize_presentation(user)


def initialize_conference():
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


def initialize_user():
    user = User.objects.create_user(
        'testname', 'test@test.com', 'testpassword')
    user.save()
    user.profile.name = '나영근'
    user.profile.bio = '안녕하세요 나영근입니다'
    user.profile.phone = '010-0000-0000'
    user.profile.organization = '파이콘 한국'
    user.profile.nationality = 'Korea'
    # img = Image.new('RGB', (800, 1280), (255, 255, 255))
    # img.save("/tmp/image.png", "PNG")
    # user.profile.image = img
    user.save()
    return user


def initialize_oauthsetting():
    oauth_setting = OAuthSetting()
    oauth_setting.env_name = 'prod'
    oauth_setting.github_client_id = 'prod_github_client_id'
    oauth_setting.github_client_secret = 'prod_github_client_secret'
    oauth_setting.gmail_client_id = 'prod_gmail_client_id'
    oauth_setting.gmail_client_secret = 'prod_gmail_client_secret'
    oauth_setting.save()
    oauth_setting = OAuthSetting()
    oauth_setting.env_name = 'develop'
    oauth_setting.github_client_id = 'develop_github_client_id'
    oauth_setting.github_client_secret = 'develop_github_client_secret'
    oauth_setting.gmail_client_id = 'develop_gmail_client_id'
    oauth_setting.gmail_client_secret = 'develop_gmail_client_secret'
    oauth_setting.save()


def initialize_sponsor(user):
    sponsor_level = SponsorLevel.objects.create(
        name='키스톤', desc='가장돈은 많이 낸 분들이죠', price='20000000', ticket_count='20')
    sponsor = Sponsor()

    sponsor.name_ko = '파이콘준비위원회'
    sponsor.desc_ko = '파이콘을 준비하는 준비위원회입니다.'
    sponsor.name_en = 'PyconKr'
    sponsor.desc_en = 'The people who want to open python conference'
    img = Image.new('RGB', (800, 1280), (255, 255, 255))
    img.save("/tmp/image_sponsor.png", "PNG")
    # sponsor.image = img
    sponsor.url = 'http://pythonkr/1'
    sponsor.level = sponsor_level
    sponsor.paid_at = datetime(
        2019, 8, 21, 13, 00).astimezone(tz=TIMEZONE)
    sponsor.ticket_users = user
    sponsor.save()


def initialize_presentation(user):
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
    presentation.started_at = datetime(
        2019, 8, 21, 13, 00).astimezone(tz=TIMEZONE)
    presentation.finished_at = datetime(
        2019, 8, 21, 15, 00).astimezone(tz=TIMEZONE)
    presentation.category = category
    presentation.slide_url = 'https://slide/1'
    presentation.pdf_url = 'https://pdf/1'
    presentation.video_url = 'https://video/1'
    presentation.difficulty = difficulty
    presentation.recordable = True
    presentation.save()
