from __future__ import annotations
from hashlib import sha1
from django.db import models
from rest_framework.response import Response

from pitter.models.base import BaseModel


class User(BaseModel):
    login = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    salt = models.CharField(max_length=256)
    profile = models.CharField(max_length=256, blank=True)
    email = models.CharField(max_length=256, blank=True)
    email_notification = models.BooleanField(default=False)

    @staticmethod
    def gen_password(password: str, salt: str) -> str:
        """
        Шифрует пароль с солью
        :param password: Пароль
        :param salt: Соль
        :return:
        """
        hashed_password = sha1((password + salt).encode()).hexdigest()
        return '%s$%s' % (salt, hashed_password)

    @staticmethod
    def check_password(raw_password, enc_password):
        """
        Проверяет достоверность пароля
        :param raw_password: Пароль
        :param enc_password: Зашифрованный пароль
        :return:
        """
        salt, hsh = enc_password.split('$')
        return hsh == sha1((raw_password + salt).encode()).hexdigest()

    @staticmethod
    def create_user(login: str, password: str, salt: str) -> User:
        """
        Создает нового пользователя
        :param salt: Соль
        :param login: Логин
        :param password: Пароль
        :return:
        """
        return User.objects.create(
            login=login,
            salt=salt,
            password=User.gen_password(password, salt),
        )

    @staticmethod
    def delete_user(user_id: str) -> Response:
        """
        Удаляет пользователя
        :param user_id: Идентификатор пользователя
        :return:
        """
        try:
            user_to_delete = User.objects.get(id=user_id)
            user_to_delete.delete()
            dummy = Response(status=204)
        except User.DoesNotExist:
            dummy = Response(status=404)
        return dummy

    @staticmethod
    def get_user(login: str, password: str) -> User:
        """
        Находит пользователя по логину и паролю
        :param login: Логин
        :param password: Пароль
        :return:
        """
        dummy = None
        for user in User.objects.all():
            if login == user.login and User.check_password(password, user.password):
                dummy = user
                break
        return dummy
