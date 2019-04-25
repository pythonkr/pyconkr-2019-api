import graphene
from graphene_django import DjangoObjectType
from graphql_extensions.auth.decorators import login_required
from graphql_extensions.exceptions import GraphQLError

from api.models.schedule import Schedule
from iamporter import Iamporter
from django.utils import timezone
from django.conf import settings

class PaymentInput(graphene.InputObjectType):
    card_number = graphene.String()
    expiry = graphene.String()
    birth = graphene.String()
    pwd_2digit = graphene.String()


class BuyEarlyBirdTicket(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        payment = PaymentInput(required=True)

    @login_required
    def mutate(self, info, payment):
        user = info.context.user
        permitted_settings = settings.PERMITTED_SETTINGS
        if not permitted_settings:
            raise GraphQLError(f'{settings.PERMITTED_SETTINGS_PATH}가 설정되어 있지 않습니다.')
        client = Iamporter(imp_key=permitted_settings['IMP_KEY'],
                           imp_secret=permitted_settings['IMP_SECRET'])
        now = timezone.now()
        merchant_uid = f'merchant_{now.timestamp()}'
        client.create_payment(
            merchant_uid=merchant_uid,
            name="PyConKorea_EarlyBirdTicket",
            amount=1000,
            **payment
        )
        return BuyEarlyBirdTicket(success=True)


class Mutations(graphene.ObjectType):
    buy_early_bird_ticket = BuyEarlyBirdTicket.Field()


class Query(graphene.ObjectType):
    pass
