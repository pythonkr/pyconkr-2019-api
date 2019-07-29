import datetime
import graphene
import pytz
from graphene_django import DjangoObjectType

from api.models.profile import Profile
from api.models.program import Program, Difficulty, Place


class PlaceNode(DjangoObjectType):
    class Meta:
        model = Place
        description = """
        It is the place where the program is held.
        This can be either in the room or in the lobby.
        """


class DifficultyNode(DjangoObjectType):
    class Meta:
        model = Difficulty
        description = """
        Difficulty of presentation.
        """


class LanguageNode(graphene.Enum):
    KOREAN = Program.LANGUAGE_KOREAN
    ENGLISH = Program.LANGUAGE_ENGLISH


class SeoulDateTime(graphene.types.Scalar):
    '''
    It is used to replace timezone to Seoul for graphene queries.
    When using the time field, specify scala as follows and return it in Korean time.
    e.g)
    started_at = graphene.Field(SeoulDateTime)
    finished_at = graphene.Field(SeoulDateTime)
    '''

    @staticmethod
    def serialize(obj):
        timezone = pytz.timezone('Asia/Seoul')
        return obj.astimezone(tz=timezone).isoformat()

    @staticmethod
    def parse_literal(node):
        return datetime.datetime.strptime(
            node.value, "%Y-%m-%dT%H:%M:%S.%f")

    @staticmethod
    def parse_value(value):
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")


class ImageUrl(graphene.types.Scalar):
    '''
    It is used to get image url for graphene queries.
    e.g)
    image = graphene.Field(ImageUrl)
    to)
    image: http://www.pycon.kr/media/profile/image.png
    '''

    @staticmethod
    def serialize(obj):
        if not obj.name:
            return ''
        return obj.url


class FileUrl(graphene.types.Scalar):
    '''
    It is used to get file url for graphene queries.
    e.g)
    file = graphene.Field(FileUrl)
    to)
    file: http://www.pycon.kr/media/profile/image.pdf
    '''

    @staticmethod
    def serialize(obj):
        if not obj.name:
            return ''
        return obj.url


class ProgramNode(DjangoObjectType):
    class Meta:
        model = Program
        description = """
        Abstract node for program in Python Conference Korea.
        Many kinds of program inherit this node.
        """


class UserEmailNode(DjangoObjectType):
    class Meta:
        model = Profile
        only_fields = ('id', 'oauth_type', 'name', 'name_ko', \
                       'name_en', 'organization', 'image', 'email')
        description = '''
            스프린트와 튜토리얼 진행자에게 제공되는 유저 이름, 조직, 이메일 정보입니다.
        '''

    def resolve_image(self, info):
        if self.image.name:
            return self.image.url
        return self.avatar_url


def has_owner_permission(user, owner):
    if user.is_anonymous:
        return False
    if user.is_staff or user.is_superuser:
        return True
    if owner and owner is user:
        return True
    if user.profile and user.profile.is_organizer:
        return True
    return False
