import jwt
from rest_framework.response import Response

from pitter.settings import RSA_PRIVATE_KEY, RSA_PUBLIC_KEY


def create_token(payload: dict) -> str:
    """
    Создает токен авторизации
    :param payload: данные
    :return:
    """
    return jwt.encode(payload, RSA_PRIVATE_KEY, algorithm='RS256')


def get_token_payload(token: str) -> dict:
    """
    Получает данные из токена
    :param token:
    :return:
    """
    return jwt.decode(token, RSA_PUBLIC_KEY, algorithms='RS256')


def access_token_required(func):
    """
    Валидация токена авторизации
    :param func:
    :return:
    """

    def wrapped_f(cls, request):
        payload = request.headers.get('Authorization')
        if not payload:
            return Response({'error': 'Отсутствует токен авторизации'}, status=400)
        else:
            try:
                get_token_payload(payload.split()[-1])
            except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.ExpiredSignature):
                return Response({'error': 'Вы не авторизованы'}, status=403)
        return func(cls, request)

    return wrapped_f
