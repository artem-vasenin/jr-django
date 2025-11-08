import graphene
import base64
from django.core.files.base import ContentFile
from graphene_django.types import DjangoObjectType

from .models import Category, Product, Review


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = '__all__'


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewType(DjangoObjectType):
    class Meta:
        model = Review
        fields = '__all__'


class Query(graphene.ObjectType):
    all_cats = graphene.List(CategoryType)
    all_products = graphene.List(ProductType)
    all_reviews = graphene.List(ReviewType)

    @staticmethod
    def resolve_all_cats(root, info):
        return Category.objects.all()

    @staticmethod
    def resolve_all_products(root, info):
        return Product.objects.all()

    @staticmethod
    def resolve_all_reviews(root, info):
        return Review.objects.all()


class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        slug = graphene.String(required=False)
        parent_id = graphene.Int(required=False)

    obj = graphene.Field(CategoryType)

    def mutate(self, info, name, slug=None, parent_id=None):
        obj = Category.objects.create(name=name, slug=slug, parent_id=parent_id)
        return CreateCategory(obj=obj)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        slug = graphene.String(required=False)
        description = graphene.String(required=False)
        unit = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        category_id = graphene.Int(required=True)
        stock = graphene.Int(required=False)
        is_active = graphene.Boolean(required=False)
        image = graphene.String(required=False)

    obj = graphene.Field(ProductType)

    def mutate(
            self, info, name, unit, price, category_id, stock=None,
            slug=None, description=None, is_active=True, image=None
    ):
        obj = Product.objects.create(
            name=name, slug=slug, unit=unit, price=price, category_id=category_id,
            stock=stock, description=description, is_active=is_active,
        )
        if image:
            format, imgstr = image.split(';base64,') if ';base64,' in image else (None, image)
            ext = format.split('/')[-1] if format else 'jpg'
            obj.image.save(f'{obj.pk}.{ext}', ContentFile(base64.b64decode(imgstr)), save=True)

        return CreateProduct(obj=obj)


class CreateReview(graphene.Mutation):
    class Arguments:
        comment = graphene.String(required=True)
        user_id = graphene.Int(required=True)
        product_id = graphene.Int(required=True)
        rating = graphene.Int(required=True)
        is_active = graphene.Boolean(required=False)

    obj = graphene.Field(ReviewType)

    def mutate(self, info, comment, user_id, product_id, rating, is_active=True):
        obj = Review.objects.create(
            comment=comment, user_id=user_id, product_id=product_id, rating=rating, is_active=is_active,
        )
        return CreateReview(obj=obj)


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    create_product = CreateProduct.Field()
    create_review = CreateReview.Field()
