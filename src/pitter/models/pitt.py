from __future__ import annotations

from typing import Optional

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from pitter.exceptions import PittNotFound
from pitter.models.base import BaseModel
from pitter.models.user import User


class Pitt(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='uploads/')
    audio_file_transcription = models.CharField(max_length=256)

    @staticmethod
    def create_pitt(user: User, audio_file: str, audio_file_transcription: str) -> Pitt:
        """
        Создает новый питт
        :param user: Владелец питта
        :param audio_file: Путь к аудиофайлу
        :param audio_file_transcription: Распознанный текст
        :return:
        """
        return Pitt.objects.create(user=user, audio_file=audio_file, audio_file_transcription=audio_file_transcription,)

    @staticmethod
    def get_pitt(pitt_id: str) -> Optional[Pitt]:
        """
        Возвращает питт по его id
        :param pitt_id: Идентификатор питта
        :return:
        """
        try:
            res = Pitt.objects.get(id=pitt_id)
        except Pitt.DoesNotExist:
            raise PittNotFound
        return res


@receiver(pre_delete, sender=Pitt)
def delete_audio_file(instance, **kwargs):  # pylint: disable=unused-argument
    """
    Физическое удаление аудиофайлов
    :param instance:
    :param kwargs:
    :return:
    """
    instance.audio_file.delete(False)
