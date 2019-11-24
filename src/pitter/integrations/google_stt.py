from base64 import b64encode
import json
import requests

from pitter.exceptions import ValidationError
from pitter.settings import GOOGLE_STT_API_KEY, GOOGLE_STT_API_URL


class SpeechToText:
    LANGUAGE_CODE: str = 'ru-RU'
    AUDIO_CHANNEL_COUNT: int = 1

    @classmethod
    def decode(cls, audio_file: bytes) -> str:
        """
        Преобразует аудиофайл в текст с помощью GoogleSpeechToText
        :param audio_file: аудиофайл
        :return:
        """
        speech_content = b64encode(audio_file)
        request_body = {
            'config': {
                'audio_channel_count': cls.AUDIO_CHANNEL_COUNT,
                'languageCode': cls.LANGUAGE_CODE,
            },
            'audio': {
                'content': speech_content.decode('UTF-8'),
            },
        }
        result = requests.post(GOOGLE_STT_API_URL.format(GOOGLE_STT_API_KEY), data=json.dumps(request_body))
        try:
            res = result.json()['results'][0]['alternatives'][0]['transcript']
            return res
        except KeyError:
            raise ValidationError(message="Неподдерживаемый формат аудиофайла")
