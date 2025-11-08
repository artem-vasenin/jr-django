import graphene
import base64
from django.core.files.base import ContentFile
from graphene_django.types import DjangoObjectType

from .models import Category, Product, Review


class CategoryType(DjangoObjectType):
    """Тип категорий"""
    class Meta:
        model = Category
        fields = '__all__'


class ProductType(DjangoObjectType):
    """Тип товаров"""
    class Meta:
        model = Product
        fields = '__all__'


class ReviewType(DjangoObjectType):
    """Тип отзывов"""
    class Meta:
        model = Review
        fields = '__all__'


class Query(graphene.ObjectType):
    all_cats = graphene.List(CategoryType)
    cat_by_id = graphene.Field(CategoryType, pk=graphene.Int(required=True))
    all_products = graphene.List(ProductType)
    product_by_id = graphene.Field(ProductType, pk=graphene.Int(required=True))
    all_reviews = graphene.List(ReviewType)

    @staticmethod
    def resolve_all_cats(root, info):
        """Получение всех категорий"""
        return Category.objects.all()

    @staticmethod
    def resolve_cat_by_id(root, info, pk):
        """Получение категории по PK"""
        return Category.objects.filter(pk=pk).first()

    @staticmethod
    def resolve_all_products(root, info):
        """Получение всех товаров"""
        return Product.objects.all()

    @staticmethod
    def resolve_product_by_id(root, info, pk):
        """Получение товара по PK"""
        return Product.objects.filter(pk=pk).first()

    @staticmethod
    def resolve_all_reviews(root, info):
        """Получение всех отзывов"""
        return Review.objects.all()


class CreateCategory(graphene.Mutation):
    """Создание категории"""
    class Arguments:
        name = graphene.String(required=True)
        slug = graphene.String(required=False)
        parent_id = graphene.Int(required=False)

    result = graphene.Field(CategoryType)

    def mutate(self, info, name, slug=None, parent_id=None):
        user = info.context.user
        if not user.is_authenticated and not user.is_superuser:
            raise Exception("Access denied")
        obj = Category.objects.create(name=name, slug=slug, parent_id=parent_id)
        return CreateCategory(result=obj)


class UpdateCategory(graphene.Mutation):
    """Обновление категории"""
    class Arguments:
        pk = graphene.Int(required=True)
        name = graphene.String(required=False)
        slug = graphene.String(required=False)
        parent_id = graphene.Int(required=False)

    result = graphene.Field(CategoryType)

    def mutate(self, info, pk, name=None, slug=None, parent_id=None):
        user = info.context.user
        if not user.is_authenticated and not user.is_superuser:
            raise Exception("Access denied")

        try:
            obj = Category.objects.get(pk=pk)
            obj.name = name if name else obj.name
            obj.slug = slug if slug else obj.slug
            obj.parent_id = parent_id if parent_id else obj.parent_id
            obj.save()
            return UpdateCategory(result=obj)
        except Category.DoesNotExist:
            return UpdateCategory(result=None)


class DeleteCategory(graphene.Mutation):
    """Удаление категории"""
    class Arguments:
        pk = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, pk):
        if not info.context.user.is_authenticated and not info.context.user.is_superuser:
            raise Exception("Access denied")

        try:
            obj = Category.objects.get(pk=pk)
            obj.delete()
            return DeleteCategory(ok=True)
        except Category.DoesNotExist:
            return DeleteCategory(ok=False)


class CreateProduct(graphene.Mutation):
    """Создание товара"""
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

    result = graphene.Field(ProductType)

    def mutate(
            self, info, name, unit, price, category_id, stock=None,
            slug=None, description=None, is_active=True, image=None
    ):
        user = info.context.user
        if not user.is_authenticated and not user.is_superuser:
            raise Exception("Access denied")
        obj = Product.objects.create(
            name=name, slug=slug, unit=unit, price=price, category_id=category_id,
            stock=stock, description=description, is_active=is_active,
        )
        if image:
            format, imgstr = image.split(';base64,') if ';base64,' in image else (None, image)
            ext = format.split('/')[-1] if format else 'jpg'
            obj.image.save(f'{obj.pk}.{ext}', ContentFile(base64.b64decode(imgstr)), save=True)

        return CreateProduct(result=obj)


class UpdateProduct(graphene.Mutation):
    """Обновление товара"""
    class Arguments:
        pk = graphene.Int(required=True)
        name = graphene.String(required=False)
        slug = graphene.String(required=False)
        description = graphene.String(required=False)
        unit = graphene.String(required=False)
        price = graphene.Decimal(required=False)
        category_id = graphene.Int(required=False)
        stock = graphene.Int(required=False)
        is_active = graphene.Boolean(required=False)
        image = graphene.String(required=False)

    result = graphene.Field(ProductType)

    def mutate(
            self, info, pk, name=None, unit=None, price=None, category_id=None, stock=None,
            slug=None, description=None, is_active=None, image=None
    ):
        user = info.context.user

        if not user.is_authenticated and not user.is_superuser:
            raise Exception("Access denied")

        try:
            obj = Product.objects.get(pk=pk)
            obj.name = name if name else obj.name
            obj.slug = slug if slug else obj.slug
            obj.unit = unit if unit else obj.unit
            obj.price = price if price else obj.price
            obj.category_id = category_id if category_id else obj.category_id
            obj.stock = stock if stock else obj.stock
            obj.description = description if description else obj.description
            obj.is_active = is_active if is_active is not None else obj.is_active
            obj.save()

            if image:
                format, imgstr = image.split(';base64,') if ';base64,' in image else (None, image)
                ext = format.split('/')[-1] if format else 'jpg'
                obj.image.save(f'{obj.pk}.{ext}', ContentFile(base64.b64decode(imgstr)), save=True)

            return UpdateProduct(result=obj)
        except Product.DoesNotExist:
            return UpdateProduct(result=None)


class DeleteProduct(graphene.Mutation):
    """Удаление товара"""
    class Arguments:
        pk = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, pk):
        if not info.context.user.is_authenticated and not info.context.user.is_superuser:
            raise Exception("Access denied")

        try:
            obj = Product.objects.get(pk=pk)
            obj.delete()
            return DeleteProduct(ok=True)
        except Product.DoesNotExist:
            return DeleteProduct(ok=False)


class CreateReview(graphene.Mutation):
    """Создание отзыва"""
    class Arguments:
        comment = graphene.String(required=True)
        user_id = graphene.Int(required=True)
        product_id = graphene.Int(required=True)
        rating = graphene.Int(required=True)
        is_active = graphene.Boolean(required=False)

    result = graphene.Field(ReviewType)

    def mutate(self, info, comment, user_id, product_id, rating, is_active=True):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Access denied")
        obj = Review.objects.create(
            comment=comment, user_id=user_id, product_id=product_id, rating=rating, is_active=is_active,
        )
        return CreateReview(result=obj)


class UpdateReview(graphene.Mutation):
    """Обновление отзыва"""
    class Arguments:
        pk = graphene.Int(required=True)
        is_active = graphene.Boolean(required=True)

    result = graphene.Field(ReviewType)

    def mutate(self, info, pk, is_active):
        user = info.context.user
        if not user.is_authenticated and not user.is_superuser:
            raise Exception("Access denied")

        try:
            obj = Review.objects.get(pk=pk)
            obj.is_active = is_active if is_active else obj.is_active
            obj.save()

            return UpdateReview(result=obj)
        except Review.DoesNotExist:
            return UpdateReview(result=None)


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()
    create_review = CreateReview.Field()
    update_review = UpdateReview.Field()
