from typing import Dict

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from drf_yasg import openapi
from drf_yasg.openapi import Parameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers.users_serializers import (
    UsersResponse,
    UsersData,
    UsersSearchResponse,
    UsersSearchData,
)
from pitter.decorators import response_dict_serializer
from pitter import exceptions
from pitter.models.user import User
from pitter.utils.auth import access_token_required

USERS_PAGE_PARAM = Parameter(in_=openapi.IN_QUERY, name='page', required=False, type=openapi.TYPE_INTEGER,)

USERS_LOGIN_PARAM = Parameter(in_=openapi.IN_QUERY, name='login', required=True, type=openapi.TYPE_STRING,)

USERS_ON_PAGE = 5


class UsersView(APIView):
    @classmethod
    @response_dict_serializer(UsersResponse)
    @swagger_auto_schema(
        tags=['Pitter: Users'],
        manual_parameters=[USERS_PAGE_PARAM],
        responses={
            200: UsersResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Список всех пользователей',
        operation_description='Список всех пользователей в сервисе Pitter',
    )
    @access_token_required
    def get(cls, request) -> Dict[str, str]:
        """
        Показывает список всех пользователей постранично
        :param request:
        :return:
        """
        res = {}
        all_users = User.objects.all().order_by('login')
        current_page = Paginator(all_users, USERS_ON_PAGE)
        page = request.GET.get('page')
        try:
            res['users'] = UsersData(current_page.page(page).object_list, many=True).data
        except PageNotAnInteger:
            res['users'] = UsersData(current_page.page(1).object_list, many=True).data
        except EmptyPage:
            res['users'] = UsersData(current_page.page(current_page.num_pages).object_list, many=True).data
        return res


class UsersSearchView(APIView):
    @classmethod
    @response_dict_serializer(UsersSearchResponse)
    @swagger_auto_schema(
        tags=['Pitter: Users'],
        manual_parameters=[USERS_LOGIN_PARAM],
        responses={
            200: UsersSearchResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Поиск пользователей по логину',
        operation_description='Поиск пользователей по логину в сервисе Pitter',
    )
    @access_token_required
    def get(cls, request) -> Dict[str, str]:
        """
        Ищет пользователей по логину
        :param request:
        :return:
        """
        res = {}
        login: str = request.GET.get('login')
        users = User.objects.filter(login__icontains=login).all()
        res['users'] = UsersSearchData(users, many=True).data
        return res
