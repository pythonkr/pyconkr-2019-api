import graphene
from graphene_django import DjangoObjectType
from api.models.schedule import Schedule


class ScheduleNode(DjangoObjectType):
    class Meta:
        model = Schedule
        description = """
        Schedules of Python Korea.
        """


class Mutations(graphene.ObjectType):
    pass


class Query(graphene.ObjectType):
    schedule = graphene.Field(ScheduleNode)

    def resolve_schedule(self, info):
        return Schedule.objects.all().latest('id')
