import datetime
from typing import Dict
from uuid import uuid4
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers.user_serializers import UserPostRequest, UserPostResponse, \
    UserDeleteResponse, UserPatchResponse, UserPatchRequest
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer
from pitter.models.user import User
from pitter.utils.auth import access_token_required
from pitter.utils.password import gen_password


class UserView(APIView):
    @classmethod
    @request_post_serializer(UserPostRequest)
    @response_dict_serializer(UserPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: User'],
        request_body=UserPostRequest,
        responses={
            200: UserPostResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Добавление нового пользователя',
        operation_description='Добавление нового пользователя в сервисе Pitter',
    )
    def post(cls, request) -> Dict[str, str]:
        """
        Создает нового пользователя
        :param request:
        :return:
        """

        login: str = request.data['login']
        password: str = request.data['password']
        salt: str = uuid4().hex

        user = User.get_user(login=login)
        if user:
            raise exceptions.UserDuplicateError
        res = User.create_user(
            login=login,
            password=password,
            salt=salt,
        )
        return dict(id=res.id, )



    @classmethod
    @response_dict_serializer(UserDeleteResponse)
    @swagger_auto_schema(
        tags=['Pitter: User'],
        responses={
            200: UserDeleteResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Удаление пользователя',
        operation_description='Удаление пользователя в сервисе Pitter',
    )
    @access_token_required
    def delete(cls, request) -> Dict[str, str]:
        """
        Удаляет учетную запись пользователя
        :param request:
        :param user_id:
        :return:
        """
        user_id = getattr(request, 'user_id', None)
        user = User.get_user(user_id=user_id)
        if not user:
            raise exceptions.UserNotFound
        user.delete()
        return dict(deleted_id=user_id, )


    @classmethod
    @request_post_serializer(UserPatchRequest)
    @response_dict_serializer(UserPatchResponse)
    @swagger_auto_schema(
        tags=['Pitter: User'],
        request_body=UserPatchRequest,
        responses={
            200: UserPatchResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Обновление данных пользователя',
        operation_description='Обновление данных пользователя в сервисе Pitter',
    )
    @access_token_required
    def patch(cls, request) -> Dict[str, str]:
        """
        Обновляет поля пользователя
        :param request:
        :return:
        """
        update_info = request.data
        user_id = getattr(request, 'user_id', None)
        user = User.get_user(user_id=user_id)
        if update_info.get('password', None):
            update_info['password'] = gen_password(update_info.get('password'), user.salt)
        update_info['updated_at'] = timezone.now() + datetime.timedelta(hours=2)
        User.objects.filter(id=user_id).update(**update_info)
        return dict(updated_fields=str(list(update_info)))
