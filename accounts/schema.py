import base64
import logging
import graphene
import graphql_jwt
from graphql import GraphQLError
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from django.core.files.base import ContentFile
from graphql_jwt.decorators import login_required, superuser_required

from .models import Profile


logger = logging.getLogger('api_logs')


class UserType(DjangoObjectType):
    """Тип пользователя"""
    class Meta:
        model = User
        exclude = ('password',)


class ProfileType(DjangoObjectType):
    """Тип профиля"""
    class Meta:
        model = Profile
        fields = '__all__'


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, pk=graphene.Int(required=True))
    profile_by_user_id = graphene.Field(ProfileType, pk=graphene.Int(required=True))

    @staticmethod
    @login_required
    def resolve_all_users(root, info):
        """Получение всех пользователей"""
        return User.objects.prefetch_related('profile')

    @staticmethod
    @login_required
    def resolve_user_by_id(root, info, pk):
        """Получение пользователя по PK"""
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            logger.error('Пользователь не найден')
            raise GraphQLError('Пользователь с таким ID не найден.')

    @staticmethod
    @login_required
    def resolve_profile_by_user_id(root, info, pk):
        """Получение профиля по PK"""
        profile = Profile.objects.filter(user_id=pk).first()
        if not profile:
            logger.error('Профиль не найден')
            raise GraphQLError('Профиль с таким ID не найден.')


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class Registration(graphene.Mutation):
    """Регистрация пользователя"""
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)

    result = graphene.Field(UserType)

    def mutate(self, info, username, email, password1, password2):
        if password1 != password2:
            logger.error('Пароли не совпадают')
            raise GraphQLError('Пароли не совпадают')
        if User.objects.filter(username=username).exists():
            logger.error('Такой пользователь уже есть')
            raise GraphQLError('Такой пользователь уже есть')
        if User.objects.filter(email=email).exists():
            logger.error('Email уже существует')
            raise GraphQLError('Email уже существует')
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            logger.info(f'Пользователь {user.get_username()} зарегистрирован')

            return Registration(result=user)
        except Exception as e:
            logger.error(f'Ошибка регистрации: {e}')
            raise GraphQLError(f'Ошибка регистрации: {e}')


class UpdateProfile(graphene.Mutation):
    """Изменение профиля пользователя"""
    class Arguments:
        username = graphene.String(required=False)
        email = graphene.String(required=False)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        city = graphene.String(required=False)
        address = graphene.String(required=False)
        phone = graphene.String(required=False)
        image = graphene.String(required=False)

    result = graphene.Field(UserType)

    @login_required
    def mutate(
            self, info, username=None, email=None, first_name=None,
            last_name=None, city=None, address=None, phone=None, image=None,
    ):
        user = info.context.user
        profile = user.profile

        if username:
            if username != user.username and User.objects.filter(username=username).exists():
                logger.error(f'Такое имя пользователя ({username}) уже занято')
                raise GraphQLError(f'Такое имя пользователя ({username}) уже занято')
            user.username = username
        if email:
            if email != user.email and User.objects.filter(email=email).exists():
                logger.error(f'Такой Email ({email}) уже занят')
                raise GraphQLError(f'Такой Email ({email}) уже занят')
            user.email = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if city:
            profile.city = city
        if address:
            profile.address = address
        if phone:
            profile.phone = phone
        if image:
            if ';base64,' in image:
                format, imgstr = image.split(';base64,')
                ext = format.split('/')[-1]
            else:
                imgstr = image
                ext = 'jpg'

            profile.image.save(f'{user.pk}.{ext}', ContentFile(base64.b64decode(imgstr)), save=True)
        try:
            user.save()
            logger.info(f'Пользователь ({username}) зарегистрирован')
            return UpdateProfile(result=user)
        except Exception as e:
            logger.error(f'Ошибка регистрации ({e})')
            raise GraphQLError(f'Registration failed: {e}')


class DeleteUser(graphene.Mutation):
    """Удаление пользователя"""
    class Arguments:
        pk = graphene.Int(required=True)

    ok = graphene.Boolean()

    @superuser_required
    def mutate(self, info, pk):
        try:
            obj = User.objects.get(pk=pk)
            name = obj.username
            obj.delete()
            logger.info(f'Пользователь ({name}) удален')
            return DeleteUser(ok=True)
        except User.DoesNotExist:
            logger.error('Пользователь не найден')
            return DeleteUser(ok=False)


class Mutation(graphene.ObjectType):
    registration = Registration.Field()
    update_profile = UpdateProfile.Field()
    delete_user = DeleteUser.Field()
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
