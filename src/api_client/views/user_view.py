import datetime
from typing import Dict
from uuid import uuid4

from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.openapi import Parameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers.feed_serializers import PittsData
from api_client.validation_serializers.user_serializers import (
    UserPostRequest,
    UserPostResponse,
    UserDeleteResponse,
    UserPatchResponse,
    UserPatchRequest,
    UserGetResponse,
)
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer
from pitter.models.pitt import Pitt
from pitter.models.subscription import Subscription
from pitter.models.user import User
from pitter.utils.auth import access_token_required
from pitter.utils.password import gen_password

PITTS_PAGE_PARAM = Parameter(in_=openapi.IN_QUERY, name='page', required=False, type=openapi.TYPE_INTEGER,)

USER_ID_PARAM = Parameter(in_=openapi.IN_QUERY, name='id', required=True, type=openapi.TYPE_STRING,)

PITTS_ON_PAGE = 25


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
        res = User.create_user(login=login, password=password, salt=salt,)
        return dict(id=res.id,)

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
        :return:
        """
        user_id: str = getattr(request, 'user_id', None)
        user = User.get_user(user_id=user_id)
        if not user:
            raise exceptions.UserNotFound
        user.delete()
        return dict(deleted_id=user_id,)

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
        update_info: dict = request.data
        user_id: str = getattr(request, 'user_id', None)
        user = User.get_user(user_id=user_id)
        if update_info.get('password', None):
            update_info['password'] = gen_password(update_info.get('password'), user.salt)
        update_info['updated_at'] = timezone.now() + datetime.timedelta(hours=2)
        User.objects.filter(id=user_id).update(**update_info)
        return dict(updated_fields=str(list(update_info)))

    @classmethod
    @response_dict_serializer(UserGetResponse)
    @swagger_auto_schema(
        tags=['Pitter: User'],
        manual_parameters=[USER_ID_PARAM, PITTS_PAGE_PARAM],
        responses={
            200: UserGetResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Страница пользователя с питтами',
        operation_description='Страница пользователя с питтами в сервисе Pitter',
    )
    @access_token_required
    def get(cls, request) -> Dict[str, str]:
        """
        Показывает страницу пользователя
        :param request:
        :return:
        """
        res = {}
        logged_user_id: str = getattr(request, 'user_id', None)
        logged_user = User.get_user(user_id=logged_user_id)
        user_id: str = request.GET.get('id')
        user = User.get_user(user_id=user_id)
        all_pitts = Pitt.objects.filter(user=user).order_by('-created_at')
        current_page = Paginator(all_pitts, PITTS_ON_PAGE)
        page: int = request.GET.get('page')
        res['id'] = user.id
        res['profile'] = user.profile
        if user != logged_user:
            res['flag'] = bool(Subscription.objects.filter(follower=logged_user, followed=user,))
        try:
            res['pitts'] = PittsData(current_page.page(page).object_list, many=True).data
        except PageNotAnInteger:
            res['pitts'] = PittsData(current_page.page(1).object_list, many=True).data
        except EmptyPage:
            res['pitts'] = PittsData(current_page.page(current_page.num_pages).object_list, many=True).data
        return res
