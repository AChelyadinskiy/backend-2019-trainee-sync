from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers.subscription_serializers import SubscriptionPostResponse, SubscriptionPostRequest
from pitter.decorators import request_post_serializer, response_dict_serializer
from pitter import exceptions
from pitter.exceptions import UserNotFound
from pitter.models.subscription import Subscription
from pitter.models.user import User
from pitter.utils.auth import access_token_required


class SubscriptionView(APIView):
    @classmethod
    @request_post_serializer(SubscriptionPostRequest)
    @response_dict_serializer(SubscriptionPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: Subscription'],
        request_body=SubscriptionPostRequest,
        responses={
            200: SubscriptionPostResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Управление подпиской',
        operation_description='Управление подпиской в сервисе Pitter',
    )
    @access_token_required
    def post(cls, request) -> Dict[str, str]:
        """
        Запрос на подписку/удаление подписки
        :param request:
        :return:
        """
        follower_id = getattr(request, 'user_id', None)
        follower = User.get_user(user_id=follower_id)
        followed_id = request.data['followed_id']
        followed = User.get_user(user_id=followed_id)
        if not followed:
            raise UserNotFound
        try:
            sub = Subscription.objects.get(follower=follower, followed=followed,)
        except Subscription.DoesNotExist:
            sub = None
        if sub:
            sub.delete()
            flag = False
        else:
            Subscription.create_subscription(
                follower=follower, followed=followed,
            )
            flag = True
        return dict(followed_id=followed_id, flag=flag,)
