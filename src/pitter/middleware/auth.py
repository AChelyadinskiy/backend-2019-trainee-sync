from typing import Optional
import jwt
from django.http import JsonResponse
from pitter.exceptions import InvalidToken, Forbidden, ExpiredToken
from pitter.settings import RSA_PUBLIC_KEY


def check_token(auth_type: str, token: str) -> tuple:
    """
    Проверяет JWT токен
    :param auth_type:
    :param token:
    :return:
    """
    if auth_type != 'JWT':
        res = (False, InvalidToken)
    else:
        try:
            payload = jwt.decode(token, RSA_PUBLIC_KEY, algorithms='RS256')
            res = (True, payload['user_id'])
        except jwt.exceptions.InvalidSignatureError:
            res = (False, InvalidToken)
        except jwt.exceptions.ExpiredSignature:
            res = (False, ExpiredToken)
    return res


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(self.process_response(request))
        return response

    def process_response(self, request) -> Optional[JsonResponse]:
        """
        Проверяет токен в запросе
        :param request:
        :return:
        """
        auth = request.headers.get('Authorization', '').split()
        if not auth:
            setattr(request, 'exception', Forbidden)
        elif len(auth) != 2:
            setattr(request, 'exception', InvalidToken)
        else:
            auth_type = auth[0]
            token = auth[1]
            check, data = check_token(auth_type, token)
            if check:
                setattr(request, 'user_id', data)
            else:
                setattr(request, 'exception', data)
        return request
