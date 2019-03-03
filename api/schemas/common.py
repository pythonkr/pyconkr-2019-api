import datetime
import graphene
import pytz
from graphene_django import DjangoObjectType

from api.models.program import Program


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


class ProgramNode(DjangoObjectType):
    class Meta:
        model = Program
        description = """
        Abstract node for program in Python Conference Korea.
        Many kinds of program inherit this node.
        """
