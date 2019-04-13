import graphene

import api.schemas.auth
import api.schemas.user
import api.schemas.presentation
import api.schemas.pyconkorea
import api.schemas.sponsor


class Mutations(api.schemas.pyconkorea.Mutations,
                api.schemas.auth.Mutations,
                api.schemas.user.Mutations,
                api.schemas.presentation.Mutations,
                api.schemas.sponsor.Mutations,
                graphene.ObjectType):
    pass


class Query(api.schemas.pyconkorea.Query,
            api.schemas.auth.Query,
            api.schemas.user.Query,
            api.schemas.presentation.Query,
            api.schemas.sponsor.Query,
            graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
