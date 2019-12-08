from __future__ import annotations
from django.db import models

from pitter.models.base import BaseModel
from pitter.models.user import User


class Subscription(BaseModel):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followed', on_delete=models.CASCADE)

    @staticmethod
    def create_subscription(follower: User, followed: User) -> Subscription:
        """
        Создает подписку на follower на followed
        :param follower: Пользователь, который подписывается
        :param followed: Пользователь, на которого подписываются
        :return:
        """
        return Subscription.objects.create(follower=follower, followed=followed,)
