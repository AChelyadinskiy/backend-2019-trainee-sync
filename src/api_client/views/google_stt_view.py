from base64 import b64encode
from typing import Dict

import requests
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from api_client.validation_serializers.google_stt_serializer import SpeechToTextPostRequest
from api_client.validation_serializers.google_stt_serializer import SpeechToTextPostResponse
from pitter import exceptions
from pitter.decorators import request_post_serializer
from pitter.decorators import response_dict_serializer
from pitter.exceptions import ValidationError
from pitter.settings import GOOGLE_STT_API_URL
from pitter.utils.auth import access_token_required


class SpeechToTextView(APIView):
    parser_classes = [MultiPartParser]

    @classmethod
    @request_post_serializer(SpeechToTextPostRequest)
    @response_dict_serializer(SpeechToTextPostResponse)
    @swagger_auto_schema(
        tags=["Pitter: recognizer"],
        request_body=SpeechToTextPostRequest,
        responses={
            200: SpeechToTextPostResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            415: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Преобразование речи в текст',
        operation_description='Преобразование аудиофайла с речью в текст',
    )
    def post(cls, request) -> Dict[str, str]:
        """
        Преобразование речи в текст
        :param request:
        :return:
        """
        audio_file = b64encode(request.data['audio_file'].read())
        request_to_google = {'speech': audio_file}
        request = requests.post(GOOGLE_STT_API_URL, request_to_google)
        try:
            result = request.json()['result']
        except KeyError:
            raise ValidationError(message="Неподдерживаемый формат аудиофайла")
        return dict(result=result, )
