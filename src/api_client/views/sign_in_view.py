import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from api_client.validation_serializers.user_serializers import UserPostRequest
from pitter.settings import TOKEN_LIFE_TIME_SEC
from pitter.decorators import request_post_serializer
from pitter import exceptions
from pitter.models.user import User
from pitter.utils.auth import create_token


class SignInView(APIView):
    @classmethod
    @request_post_serializer(UserPostRequest)
    @swagger_auto_schema(
        tags=['Pitter: SignIn'],
        request_body=UserPostRequest,
        responses={
            200: exceptions.ExceptionResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Авторизация',
        operation_description='Авторизация пользователя в сервисе Pitter',
    )
    def post(cls, request) -> Response:
        login = request.data['login']
        password = request.data['password']
        user = User.get_user(login=login, password=password)
        if user:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=TOKEN_LIFE_TIME_SEC),
                'id': user.id
            }
            token = create_token(payload)
            user_details = {'login': login, 'token': token}
            return Response(user_details, status=200)
        else:
            res = {'error': 'Пользователя с таким логином или паролем не существует'}
            return Response(res, status=403)
