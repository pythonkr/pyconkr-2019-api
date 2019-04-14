import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from graphql_extensions.auth.decorators import login_required

from api.models.sponsor import Sponsor, SponsorLevel
from api.schemas.common import SeoulDateTime, ImageUrl, FileUrl
from api.schemas.user import UserNode


class SponsorLevelNode(DjangoObjectType):
    class Meta:
        model = SponsorLevel
        description = """
        The level of sponsors, python conference in Korea.
        """
    current_remaining_number = graphene.Int()

    def resolve_current_remaining_number(self, info):
        return self.current_remaining_number


class SponsorNode(DjangoObjectType):
    class Meta:
        model = Sponsor
        description = """
        Sponsors which spon python conference in Korea.
        """

    creator = graphene.Field(UserNode)
    level = graphene.Field(SponsorLevelNode)
    paid_at = graphene.Field(SeoulDateTime)
    business_registration_file = graphene.Field(FileUrl)
    logo_image = graphene.Field(ImageUrl)
    logo_vector = graphene.Field(ImageUrl)


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
    submitted = graphene.Boolean()


class CreateOrUpdateSponsor(graphene.Mutation):
    sponsor = graphene.Field(SponsorNode)

    class Arguments:
        data = SponsorInput(required=True)

    @login_required
    def mutate(self, info, data):
        sponsor, _ = Sponsor.objects.get_or_create(creator=info.context.user)
        if 'level_id' in data:
            sponsor.level = SponsorLevel.objects.get(
                pk=data['level_id'])
            del data['level_id']

        for k, v in data.items():
            setattr(sponsor, k, v)

        sponsor.full_clean()
        sponsor.save()
        return CreateOrUpdateSponsor(sponsor=sponsor)


class SubmitSponsor(graphene.Mutation):
    class Arguments:
        submitted = graphene.Boolean(required=True)

    success = graphene.Boolean(default_value=False)
    submitted = graphene.Boolean()

    @login_required
    def mutate(self, info, submitted):
        try:
            sponsor = Sponsor.objects.get(creator=info.context.user)
        except Sponsor.DoesNotExist:
            return SubmitSponsor(success=False)
        sponsor.submitted = submitted
        sponsor.full_clean()
        sponsor.save()
        return SubmitSponsor(success=True, submitted=submitted)


class UploadBusinessRegistrationFile(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean(default_value=False)
    file = graphene.Field(FileUrl)

    @login_required
    def mutate(self, info, file, **kwargs):
        sponsor, _ = Sponsor.objects.get_or_create(creator=info.context.user)
        if sponsor.business_registration_file.name:
            sponsor.business_registration_file.delete()
        sponsor.business_registration_file.save(file.name, file)
        return UploadBusinessRegistrationFile(success=True, file=sponsor.business_registration_file)


class DeleteBusinessRegistrationFile(graphene.Mutation):
    class Arguments:
        sponsor_id = graphene.ID()

    success = graphene.Boolean(default_value=False)

    @login_required
    def mutate(self, info, sponsor_id):
        sponsor = Sponsor.objects.get(pk=sponsor_id)
        if sponsor.creator.id is not info.context.user.id:
            raise PermissionError()
        sponsor.business_registration_file.delete()
        return DeleteBusinessRegistrationFile(success=True)


class UploadLogoImage(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean(default_value=False)
    image = graphene.Field(ImageUrl)

    @login_required
    def mutate(self, info, file, **kwargs):
        sponsor, _ = Sponsor.objects.get_or_create(creator=info.context.user)
        if sponsor.logo_image.name:
            sponsor.logo_image.delete()
        sponsor.logo_image.save(file.name, file)
        return UploadLogoImage(success=True, image=sponsor.logo_image)


class UploadLogoVector(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean(default_value=False)
    image = graphene.Field(ImageUrl)

    @login_required
    def mutate(self, info, file, **kwargs):
        sponsor, _ = Sponsor.objects.get_or_create(creator=info.context.user)
        if sponsor.logo_vector.name:
            sponsor.logo_vector.delete()
        sponsor.logo_vector.save(file.name, file)
        return UploadLogoVector(success=True, image=sponsor.logo_vector)


class Mutations(graphene.ObjectType):
    create_or_update_sponsor = CreateOrUpdateSponsor.Field()
    submit_sponsor = SubmitSponsor.Field()
    upload_business_registration_file = UploadBusinessRegistrationFile.Field()
    delete_business_registration_file = DeleteBusinessRegistrationFile.Field()
    upload_logo_image = UploadLogoImage.Field()
    upload_logo_vector = UploadLogoVector.Field()


class Query(graphene.ObjectType):
    sponsor_levels = graphene.List(SponsorLevelNode)
    my_sponsor = graphene.Field(SponsorNode)
    sponsors = graphene.List(SponsorNode)

    def resolve_sponsors(self, info):
        return Sponsor.objects.exclude(paid_at=False, accepted=False).order_by('-paid_at')

    @login_required
    def resolve_my_sponsor(self, info):
        sponsor, _ = Sponsor.objects.get_or_create(creator=info.context.user)
        return sponsor

    def resolve_sponsor_levels(self, info):
        return SponsorLevel.objects.all()
