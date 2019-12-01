from typing import Dict
from uuid import uuid4

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers.user_serializers import UserPostRequest, UserPostResponse, \
    UserDeleteResponse
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer
from pitter.models.user import User
from pitter.utils.auth import access_token_required


class UserView(APIView):
    @classmethod
    @request_post_serializer(UserPostRequest)
    @response_dict_serializer(UserPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: add_user'],
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


class UserDeleteView(APIView):
    @classmethod
    @response_dict_serializer(UserDeleteResponse)
    @swagger_auto_schema(
        tags=['Pitter: delete_user'],
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
    def delete(cls, request, user_id) -> Dict[str, str]:
        """
        Удаляет пользователя по id
        :param request:
        :param user_id:
        :return:
        """
        user = User.get_user(user_id=user_id)
        if not user:
            raise exceptions.UserNotFound
        user.delete()
        return dict(deleted_id=user_id, )
