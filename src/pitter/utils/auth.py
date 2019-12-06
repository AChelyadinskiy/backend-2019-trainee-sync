import jwt
from pitter.settings import RSA_PRIVATE_KEY


def create_token(payload: dict) -> bytes:
    """
    Создает токен авторизации
    :param payload: данные
    :return:
    """
    return jwt.encode(payload, RSA_PRIVATE_KEY, algorithm='RS256')


def access_token_required(func):
    """
    Проверка авторизации
    :param func:
    :return:
    """

    def wrapper(cls, request, *args, **kwargs):
        exception = getattr(request, 'exception', None)
        if exception:
            raise exception
        return func(cls, request, *args, **kwargs)

    return wrapper
