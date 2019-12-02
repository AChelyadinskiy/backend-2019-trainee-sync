from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers.user_serach_serializers import UserSearchPostRequest, UserSearchPostResponse
from pitter.decorators import request_post_serializer, response_dict_serializer
from pitter import exceptions
from pitter.exceptions import UserNotFound
from pitter.models.user import User
from pitter.utils.auth import access_token_required


class UserSearchView(APIView):
    @classmethod
    @request_post_serializer(UserSearchPostRequest)
    @response_dict_serializer(UserSearchPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: Search_user'],
        request_body=UserSearchPostRequest,
        responses={
            200: UserSearchPostResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Поиск пользователя по логину',
        operation_description='Поиск пользователя по логину в сервисе Pitter',
    )
    @access_token_required
    def post(cls, request) -> Dict[str, str]:
        """
        Ищет пользователя по логину
        :param request:
        :return:
        """
        login: str = request.data['login']
        user = User.get_user(login=login)
        if not user:
            raise UserNotFound
        res = dict(
            login=user.login,
            profile=user.profile,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        return res
