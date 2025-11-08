import graphene

import products.schema


class Query(
    products.schema.Query,
):
    ...

class Mutation(
    products.schema.Mutation,
):
    ...

schema = graphene.Schema(query=Query, mutation=Mutation)