import graphene

import api.schemas.user
import api.schemas.presentation
import api.schemas.conference


class Mutations(api.schemas.conference.Mutations,
                api.schemas.user.Mutations,
                api.schemas.presentation.Mutations,
                graphene.ObjectType):
    pass


class Query(api.schemas.conference.Query,
            api.schemas.user.Query,
            api.schemas.presentation.Query,
            graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
