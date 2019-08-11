import graphene
from django.utils import timezone
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from graphql_extensions.auth.decorators import login_required

from api.models.program import LightningTalk
from api.schemas.common import SeoulDateTime, FileUrl
from api.schemas.user import UserNode


class LightningTalkNode(DjangoObjectType):
    class Meta:
        model = LightningTalk
        description = """
        LightningTalk
        """

    owner = graphene.Field(UserNode)
    submitted_at = graphene.Field(SeoulDateTime)
    material = graphene.Field(FileUrl)


class LightningTalkInput(graphene.InputObjectType):
    name = graphene.String()
    material_link = graphene.String()
    comment = graphene.String()


class UpdateLightningTalk(graphene.Mutation):
    lightning_talk = graphene.Field(LightningTalkNode)

    class Arguments:
        data = LightningTalkInput(required=True)

    @login_required
    def mutate(self, info, data):
        user = info.context.user
        lightning_talk, _ = \
            LightningTalk.objects.get_or_create(owner=user)
        for k, v in data.items():
            setattr(lightning_talk, k, v)
        lightning_talk.submitted_at = timezone.now()
        lightning_talk.save()
        return UpdateLightningTalk(lightning_talk=lightning_talk)


class UploadLightningTalkMaterial(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    file = graphene.Field(FileUrl)

    @login_required
    def mutate(self, info, file, **kwargs):
        user = info.context.user
        lightning_talk, _ = \
            LightningTalk.objects.get_or_create(owner=user)
        if lightning_talk.material:
            lightning_talk.material.delete()
        lightning_talk.material.save(f'{user.id}_{file.name}', file)
        return UploadLightningTalkMaterial(file=lightning_talk.material)


class Mutations(graphene.ObjectType):
    update_lightning_talk = UpdateLightningTalk.Field()
    upload_lightning_talk_material = UploadLightningTalkMaterial.Field()


class Query(graphene.ObjectType):
    lightning_talks = graphene.List(LightningTalkNode)
    my_lightning_talk = graphene.Field(LightningTalkNode)

    def resolve_lightning_talks(self, info):
        return LightningTalk.objects.filter(accepted_at__isnull=False)

    @login_required
    def resolve_my_lightning_talk(self, info):
        lightning_talk, _ = LightningTalk.objects.get_or_create(owner=info.context.user)
        return lightning_talk
