import graphene

import api.schemas.user
import api.schemas.presentation
import api.schemas.conference
import api.schemas.sponsor


class Mutations(api.schemas.conference.Mutations,
                api.schemas.user.Mutations,
                api.schemas.presentation.Mutations,
                api.schemas.sponsor.Mutations,
                graphene.ObjectType):
    pass


class Query(api.schemas.conference.Query,
            api.schemas.user.Query,
            api.schemas.presentation.Query,
            api.schemas.sponsor.Query,
            graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
