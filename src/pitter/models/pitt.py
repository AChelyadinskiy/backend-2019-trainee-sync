from __future__ import annotations
from django.db import models
from pitter.models.base import BaseModel


class Pitt(BaseModel):
    user_id = models.CharField(max_length=256)
    audio_file = models.FileField(upload_to='uploads/')
    audio_file_transcription = models.CharField(max_length=256)

    @staticmethod
    def create_pitt(user_id: str, audio_file: str, audio_file_transcription: str) -> Pitt:
        """
        Создает новый питт
        :param user_id: Идентификатор ользователя
        :param audio_file: Путь к аудиофайлу
        :param audio_file_transcription: Распознанный текст
        :return:
        """
        return Pitt.objects.create(
            user_id=user_id,
            audio_file=audio_file,
            audio_file_transcription=audio_file_transcription,
        )

    @staticmethod
    def get_pitt(pitt_id: str) -> Pitt:
        """
        Возвращает питт по его id
        :param pitt_id: Идентификатор питта
        :return:
        """
        try:
            res = Pitt.objects.get(id=pitt_id)
        except Pitt.DoesNotExist:
            res = None
        return res
