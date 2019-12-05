from typing import Dict

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers.all_users_serializers import AllUsersResponse, UsersData
from pitter.decorators import response_dict_serializer, request_post_serializer
from pitter import exceptions
from pitter.models.user import User
from pitter.utils.auth import access_token_required


class AllUsersView(APIView):
    @classmethod
    @response_dict_serializer(AllUsersResponse)
    @swagger_auto_schema(
        tags=['Pitter: All users'],
        responses={
            200: AllUsersResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Показывает список всех пользователей',
        operation_description='Показывает список всех пользователей в сервисе Pitter',
    )
    # @access_token_required
    def get(cls, request) -> Dict[str, str]:
        res = {}
        all_users = User.objects.all().order_by('login')
        current_page = Paginator(all_users, 2)
        page = request.GET.get('page')
        try:
            res['users'] = UsersData(current_page.page(page).object_list, many=True).data
        except PageNotAnInteger:
            res['users'] = UsersData(current_page.page(1).object_list, many=True).data
        except EmptyPage:
            res['users'] = UsersData(current_page.page(current_page.num_pages).object_list, many=True).data
        return res
