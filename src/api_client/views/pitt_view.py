from base64 import b64encode
from typing import Dict

import requests
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from api_client.validation_serializers.pitt_serializers import PittPostRequest, PittDeleteResponse
from api_client.validation_serializers.pitt_serializers import PittPostResponse
from pitter import exceptions
from pitter.decorators import request_post_serializer
from pitter.decorators import response_dict_serializer
from pitter.exceptions import ValidationError, Forbidden
from pitter.models.pitt import Pitt
from pitter.models.user import User
from pitter.settings import GOOGLE_STT_API_URL
from pitter.utils.auth import access_token_required


class PittView(APIView):
    parser_classes = [MultiPartParser]

    @classmethod
    @request_post_serializer(PittPostRequest)
    @response_dict_serializer(PittPostResponse)
    @swagger_auto_schema(
        tags=["Pitter: Pitt"],
        request_body=PittPostRequest,
        responses={
            200: PittPostResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            415: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Добавление питта',
        operation_description='Добавление питта в сервисе Pitter',
    )
    @access_token_required
    def post(cls, request) -> Dict[str, str]:
        """
        Добавление питта
        :param request:
        :return:
        """
        user_id = getattr(request, 'user_id', None)
        audio_file = b64encode(request.data['audio_file'].read())
        payload = {'speech': audio_file}
        request_to_service = requests.post(GOOGLE_STT_API_URL, payload)
        try:
            result = request_to_service.json()['result']
        except KeyError:
            raise ValidationError(message="Неподдерживаемый формат аудиофайла")
        user = User.get_user(user_id=user_id)
        if not user:
            raise Forbidden(message="Вы не авторизованы")
        pitt = Pitt.create_pitt(
            user=user,
            audio_file=request.data['audio_file'],
            audio_file_transcription=result,
        )
        return dict(id=pitt.id, )


class PittDeleteView(APIView):
    @classmethod
    @response_dict_serializer(PittDeleteResponse)
    @swagger_auto_schema(
        tags=["Pitter: Pitt"],
        responses={
            200: PittDeleteResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            415: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Удаление питта',
        operation_description='Удаление питта в сервисе Pitter',
    )
    @access_token_required
    def delete(cls, request, pitt_id) -> Dict[str, str]:  # pylint: disable=unused-argument
        """
        Удаление питта
        :param request:
        :param pitt_id:
        :return:
        """
        pitt = Pitt.get_pitt(pitt_id)
        pitt.delete()
        return dict(deleted_id=pitt_id, )
