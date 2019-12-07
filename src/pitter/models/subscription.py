from __future__ import annotations
from django.db import models

from pitter.models.base import BaseModel
from pitter.models.user import User


class Subscription(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower_id = models.CharField(max_length=256)

    @staticmethod
    def create_subscription(user: User, follower_id: str) -> Subscription:
        """
        Создает подписку на follower_id
        :param user: Пользователь, который подписывается
        :param follower_id: Пользователь, на которого подписываются
        :return:
        """
        return Subscription.objects.create(
            user=user,
            follower_id=follower_id,
        )
