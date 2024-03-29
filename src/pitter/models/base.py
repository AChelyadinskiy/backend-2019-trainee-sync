import uuid

from django.db import models


def default_uuid_id() -> str:
    """
    Генеририует уникальный идентификатор
    :return:
    """
    return str(uuid.uuid4()).replace('-', '')


class BaseModel(models.Model):
    id = models.CharField(default=default_uuid_id, primary_key=True, editable=False, max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
