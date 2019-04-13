import graphene
from graphene_django import DjangoObjectType
from api.models.pyconkorea import PyconKorea


class PyconKoreaNode(DjangoObjectType):
    class Meta:
        model = PyconKorea
        description = """
        Schedules of Python Korea.
        """


class Mutations(graphene.ObjectType):
    pass


class Query(graphene.ObjectType):
    pycon_korea = graphene.Field(PyconKoreaNode)

    def resolve_pycon_korea(self, info):
        pycon_koreas = PyconKorea.objects.all()
        if pycon_koreas:
            return pycon_koreas[0]
        return None
