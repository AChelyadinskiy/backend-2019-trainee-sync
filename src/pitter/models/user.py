from __future__ import annotations

from typing import Optional

from django.db import models

from pitter.models.base import BaseModel
from pitter.utils.password import gen_password, check_password


class User(BaseModel):
    login = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    salt = models.CharField(max_length=256)
    profile = models.CharField(max_length=256, blank=True)
    email = models.CharField(max_length=256, blank=True)
    email_notification = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_user(login: str, password: str, salt: str) -> User:
        """
        Создает нового пользователя
        :param salt: Соль
        :param login: Логин
        :param password: Пароль
        :return:
        """
        return User.objects.create(login=login, salt=salt, password=gen_password(password, salt),)

    @staticmethod
    def get_user(login: str = '', password: str = '', user_id: str = '') -> Optional[User]:
        """
        Находит пользователя по логину или по id или по логину и паролю
        :param user_id: Идентификатор пользователя
        :param login: Логин
        :param password: Пароль
        :return:
        """
        user = None
        if login:
            try:
                user = User.objects.get(login=login)
            except User.DoesNotExist:
                user = None
            if user and password:
                user = user if check_password(password, user.password) else None
        elif user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                user = None
        return user
