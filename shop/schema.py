import graphene

from products.schema import Mutation as ProductsMutation
from products.schema import Query as ProductsQuery
from accounts.schema import Mutation as AuthMutation
from accounts.schema import Query as AuthQuery


class Query(
    ProductsQuery,
    AuthQuery,
):
    ...

class Mutation(
    ProductsMutation,
    AuthMutation,
):
    ...

schema = graphene.Schema(query=Query, mutation=Mutation)