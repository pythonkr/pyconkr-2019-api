import time

import graphene

import api.schemas.auth
import api.schemas.presentation
import api.schemas.schedule
import api.schemas.sponsor
import api.schemas.user
import api.schemas.sprint
import ticket.schemas


class SleepPingQuery(graphene.ObjectType):
    sleep_ping = graphene.Boolean()

    def resolve_sleep_ping(self, info):
        time.sleep(2)

        return True


class Mutations(api.schemas.schedule.Mutations,
                api.schemas.auth.Mutations,
                api.schemas.user.Mutations,
                api.schemas.presentation.Mutations,
                api.schemas.sponsor.Mutations,
                api.schemas.tutorial.Mutations,
                api.schemas.sprint.Mutations,
                ticket.schemas.Mutations,
                graphene.ObjectType):
    pass


class Query(api.schemas.schedule.Query,
            api.schemas.auth.Query,
            api.schemas.user.Query,
            api.schemas.presentation.Query,
            api.schemas.sponsor.Query,
            api.schemas.tutorial.Query,
            api.schemas.sprint.Query,
            ticket.schemas.Query,
            SleepPingQuery,
            graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
