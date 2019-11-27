import jwt
from rest_framework.response import Response

from pitter.settings import RSA_PRIVATE_KEY, RSA_PUBLIC_KEY


def create_token(payload: dict) -> str:
    return jwt.encode(payload, RSA_PRIVATE_KEY, algorithm='RS256')


def get_token_payload(token: str) -> dict:
    return jwt.decode(token, RSA_PUBLIC_KEY, algorithms='RS256')


def authorization(f):
    def wrapped_f(cls, request):
        payload = request.headers.get('Authorization').split()[-1]
        if not payload:
            return Response({'error': 'Отсутствует токен авторизации'}, status=400)
        else:
            try:
                get_token_payload(payload)
            except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.ExpiredSignature):
                return Response({'error': 'Вы не авторизованы'}, status=403)
        return f(cls, request)

    return wrapped_f
