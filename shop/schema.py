import graphene

from products.schema import Mutation as ProductsMutation
from products.schema import Query as ProductsQuery
from accounts.schema import Mutation as AuthMutation
from accounts.schema import Query as AuthQuery
from orders.schema import Query as OrdersQuery
from orders.schema import Mutation as OrdersMutation


class Query(
    ProductsQuery,
    AuthQuery,
    OrdersQuery,
):
    ...


class Mutation(
    ProductsMutation,
    AuthMutation,
    OrdersMutation,
):
    ...


schema = graphene.Schema(query=Query, mutation=Mutation)
