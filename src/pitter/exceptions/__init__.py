from typing import Type

from rest_framework import serializers
from rest_framework.exceptions import APIException


class ExceptionResponse(serializers.Serializer):
    code = serializers.CharField(required=True)
    title = serializers.CharField(required=False, allow_null=True)
    message = serializers.CharField(required=True)
    payload = serializers.DictField(required=False, allow_null=True)
    debug = serializers.CharField(required=False, allow_null=True)


class PitterException(APIException):
    default_detail = 'Что-то пошло не так'
    default_code = 'ServerError'

    def __init__(self, message, error_code, status_code=500) -> None:
        detail = message
        super().__init__(detail, error_code)
        self.status_code = status_code

    @staticmethod
    def get_exception_serializer() -> Type[ExceptionResponse]:
        """

        :return:
        """
        return ExceptionResponse


class ValidationError(PitterException):
    default_detail = 'Ошибка валидации'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 422
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code, self.status_code)


class TicketNotFound(PitterException):
    default_detail = 'Тикет не найден'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 404
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code, self.status_code)


class InternalRequestError(PitterException):
    default_detail = 'Некоторые внутренние запросы вернули ошибку'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 401
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code)


class UserNotFound(PitterException):
    default_detail = 'Пользователь не найден'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 404
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code, self.status_code)


class UserDuplicateError(PitterException):
    default_detail = 'Такой пользователь уже существует'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 409
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code, self.status_code)


class InvalidToken(PitterException):
    default_detail = 'Неверный токен авторизации'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 401
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code, self.status_code)


class ExpiredToken(PitterException):
    default_detail = 'Токен авторизации просрочен'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 401
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code, self.status_code)


class Forbidden(PitterException):
    default_detail = 'Доступ запрещен'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 403
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code, self.status_code)


class PittNotFound(PitterException):
    default_detail = 'Питт не найден'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 404
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code, self.status_code)
