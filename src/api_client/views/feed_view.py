from typing import Dict

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.openapi import Parameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers.feed_serializers import PittsResponse, PittsData
from pitter.decorators import response_dict_serializer
from pitter import exceptions
from pitter.models.pitt import Pitt
from pitter.models.user import User
from pitter.utils.auth import access_token_required

PITTS_PAGE_PARAM = Parameter(
    in_=openapi.IN_QUERY,
    name='page',
    required=True,
    type=openapi.TYPE_INTEGER,
)

PITTS_ON_PAGE = 25


class FeedView(APIView):
    @classmethod
    @response_dict_serializer(PittsResponse)
    @swagger_auto_schema(
        tags=['Pitter: Feed'],
        manual_parameters=[PITTS_PAGE_PARAM],
        responses={
            200: PittsResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Список всех питов пользователя и его подписок',
        operation_description='Список всех питов пользователя и его подписок в сервисе Pitter',
    )
    @access_token_required
    def get(cls, request) -> Dict[str, str]:
        """
        Показывает список всех питтов постранично
        :param request:
        :return:
        """
        res = {}
        user_id = getattr(request, 'user_id', None)
        follower = User.get_user(user_id=user_id)
        all_pitts = Pitt.objects.filter(Q(user__followed__follower=follower) | Q(user=follower)).order_by('-created_at')
        current_page = Paginator(all_pitts, PITTS_ON_PAGE)
        page = request.GET.get('page')
        try:
            res['feed'] = PittsData(current_page.page(page).object_list, many=True).data
        except PageNotAnInteger:
            res['feed'] = PittsData(current_page.page(1).object_list, many=True).data
        except EmptyPage:
            res['feed'] = PittsData(current_page.page(current_page.num_pages).object_list, many=True).data
        return res
