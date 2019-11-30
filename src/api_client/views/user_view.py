from typing import Dict
from uuid import uuid4

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from api_client.validation_serializers.user_serializers import UserPostRequest, UserDeleteRequest, UserPostResponse
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

        try:
            User.objects.get(login=login)
            raise exceptions.UserDuplicateError
        except User.DoesNotExist:
            res = User.create_user(
                login=login,
                password=password,
                salt=salt,
            )
            return dict(id=res.id, )

    @classmethod
    @request_post_serializer(UserDeleteRequest)
    @swagger_auto_schema(
        tags=['Pitter: delete_user'],
        request_body=UserDeleteRequest,
        responses={
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Удаление пользователя',
        operation_description='Удаление пользователя в сервисе Pitter',
    )
    @access_token_required
    def delete(cls, request) -> Response:
        """
        Удаляет пользователя из БД
        :param request:
        :return:
        """

        user_id: str = request.data['id']
        result = User.delete_user(user_id)

        return result
