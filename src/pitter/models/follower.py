from django.db import models


class FollowerModel(models.Model):
    follower_id = models.CharField(max_length=256)
    user_id = models.CharField(max_length=256)
