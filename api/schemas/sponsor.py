import os

import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from graphql_extensions import exceptions
from graphql_extensions.auth.decorators import login_required

from api.models.sponsor import Sponsor, SponsorLevel
from api.schemas.common import SeoulDateTime, ImageUrl, FileUrl
from api.schemas.user import UserNode


class SponsorNode(DjangoObjectType):
    class Meta:
        model = Sponsor
        description = """
        Sponsors which spon python conference in Korea.
        """

    paid_at = graphene.Field(SeoulDateTime)


class SponsorLevelNode(DjangoObjectType):
    class Meta:
        model = SponsorLevel
        description = """
        The level of sponsors, python conference in Korea.
        """


class SponsorInput(graphene.InputObjectType):
    name_ko = graphene.String()
    name_en = graphene.String()
    manager_name = graphene.String()
    manager_phone = graphene.String()
    manager_secondary_phone = graphene.String()
    manager_email = graphene.String()
    level_id = graphene.Int()
    business_registration_number = graphene.String()
    contract_process_required = graphene.Boolean()
    url = graphene.String()
    desc_ko = graphene.String()
    desc_en = graphene.String()


class CreateOrUpdateSponsor(graphene.Mutation):
    sponsor = graphene.Field(SponsorNode)

    class Arguments:
        sponsor_input = SponsorInput(required=True)

    @login_required
    def mutate(self, info, sponsor_input):
        user = info.context.user

        if hasattr(user, 'sponsor'):
            sponsor = user.sponsor
        else:
            sponsor = Sponsor()
            sponsor.owner = user

        if 'level_id' in sponsor_input:
            sponsor.level = SponsorLevel.objects.get(
                pk=sponsor_input['level_id'])
            del sponsor_input['level_id']

        for k, v in sponsor_input.items():
            setattr(sponsor, k, v)

        sponsor.full_clean()
        sponsor.save()
        return CreateOrUpdateSponsor(sponsor=sponsor)




class UploadBusinessRegistrationFile(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()
    file = graphene.Field(FileUrl)

    @login_required
    def mutate(self, info, file, **kwargs):
        sponsor, _ = Sponsor.objects.get_or_create(creator=info.context.user)
        if sponsor.business_registration_file.name:
            sponsor.business_registration_file.delete()
        if not len(info.context.FILES):
            raise exceptions.ValidationError(message='File is not exists')
        if isinstance(file, str):
            file = info.context.FILES.get(file)
        sponsor.business_registration_file.save(file.name, file)

        return {
            'success':True,
            'file':sponsor.business_registration_file
        }

class DeleteBusinessRegistrationFile(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    success = graphene.Boolean()

    @login_required
    def mutate(self, info, id):
        sponsor = Sponsor.objects.get(pk=id)
        print(sponsor.creator, info.context.user)
        if sponsor.creator.id is not info.context.user.id:
            raise PermissionError()
        sponsor.business_registration_file.delete()
        return DeleteBusinessRegistrationFile(success=True)

class UploadLogoImage(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()
    image = graphene.Field(ImageUrl)

    @login_required
    def mutate(self, info, file, **kwargs):
        sponsor = Sponsor.objects.get_or_create(creator=info.context.user)
        if sponsor.logo_image.name:
            sponsor.logo_image.delete()
        sponsor.logo_image.save(file.filename, file)
        return UploadLogoImage(success=True, image=sponsor.logo_image)


class UploadLogoVector(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()
    image = graphene.Field(ImageUrl)

    @login_required
    def mutate(self, info, file, **kwargs):
        sponsor = Sponsor.objects.get_or_create(creator=info.context.user)
        if sponsor.logo_vector.name:
            sponsor.logo_vector.delete()
        sponsor.logo_vector.save(file.filename, file)
        return UploadLogoVector(success=True, image=sponsor.logo_vector)


class Mutations(graphene.ObjectType):
    create_or_update_sponsor = CreateOrUpdateSponsor.Field()
    upload_business_registration_file = UploadBusinessRegistrationFile.Field()
    delete_business_registration_file = DeleteBusinessRegistrationFile.Field()
    upload_logo_image = UploadLogoImage.Field()
    upload_logo_vector = UploadLogoVector.Field()


class Query(graphene.ObjectType):
    ticketUsers = graphene.List(UserNode)
    level = graphene.List(SponsorLevelNode)

    sponsor = graphene.Field(SponsorNode)
    sponsors = graphene.List(SponsorNode)

    def resolve_sponsors(self, info):
        condition = Q()
        user = info.context.user
        if user.is_authenticated:
            condition = condition | Q(owner=user)
        return Sponsor.objects.filter(condition)

    @login_required
    def resolve_my_sponsor(self, info):
        user = info.context.user
        return user.presentation

    def resolve_level(self, info):
        return SponsorLevel.objects.filter(visible=True)
