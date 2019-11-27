from uuid import uuid4

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from api_client.validation_serializers.user_serializers import UserPostRequest, UserDeleteRequest
from pitter import exceptions
from pitter.decorators import request_post_serializer
from pitter.models.user import User
from pitter.utils.auth import authorization


class UserView(APIView):
    @classmethod
    @request_post_serializer(UserPostRequest)
    @swagger_auto_schema(
        tags=['Pitter: add_user'],
        request_body=UserPostRequest,
        responses={
            200: exceptions.ExceptionResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Добавление нового пользователя',
        operation_description='Добавление нового пользователя в сервисе Pitter',
    )
    @authorization
    def post(cls, request) -> Response:
        """
        Создает нового пользователя
        :param request:
        :return:
        """

        login: str = request.data['login']
        password: str = request.data['password']
        salt: str = uuid4().hex

        if User.check_duplicate(login):
            dummy = Response({'error': 'Такой пользователь уже существует'}, status=409)
        else:
            res = User.create_user(
                login=login,
                password=password,
                salt=salt,
            )
            dummy = Response({'id': res.id}, status=200)

        return dummy

    @classmethod
    @request_post_serializer(UserDeleteRequest)
    @swagger_auto_schema(
        tags=['Pitter: delete_user'],
        request_body=UserDeleteRequest,
        responses={
            200: exceptions.ExceptionResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Удаление пользователя',
        operation_description='Удаление пользователя в сервисе Pitter',
    )
    def delete(cls, request) -> Response:
        """
        Удаляет пользователя из БД
        :param request:
        :return:
        """

        user_id: str = request.data['id']
        result = User.delete_user(user_id)

        return result
