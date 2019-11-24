from django.db import models

from pitter.models.base import BaseModel


class PittModel(BaseModel):
    user_id = models.CharField(max_length=256)
    audio_file_path = models.CharField(max_length=256)
    audio_file_transcription = models.TextField()
