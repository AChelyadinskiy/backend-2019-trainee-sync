import datetime
from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers.sign_in_serializers import SignInPostRequest, SignInPostResponse
from pitter.exceptions import UserNotFound
from pitter.settings import TOKEN_LIFE_TIME_SEC
from pitter.decorators import request_post_serializer, response_dict_serializer
from pitter import exceptions
from pitter.models.user import User
from pitter.utils.auth import create_token


class SignInView(APIView):
    @classmethod
    @request_post_serializer(SignInPostRequest)
    @response_dict_serializer(SignInPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: SignIn'],
        request_body=SignInPostRequest,
        responses={
            200: SignInPostResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Авторизация',
        operation_description='Авторизация пользователя в сервисе Pitter',
    )
    def post(cls, request) -> Dict[str, str]:
        """
        Возвращает токен авторизации
        :param request:
        :return:
        """
        login = request.data['login']
        password = request.data['password']
        user = User.get_user(login=login, password=password)
        if not user:
            raise UserNotFound
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=TOKEN_LIFE_TIME_SEC),
            'user_id': user.id
        }
        token = create_token(payload).decode("utf-8")
        return dict(login=login, token=token, )
