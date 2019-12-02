from rest_framework import serializers


class UserSearchPostRequest(serializers.Serializer):
    login = serializers.CharField(required=True, label='Логин', max_length=256)


class UserSearchPostResponse(serializers.Serializer):
    login = serializers.CharField(required=True, label='Логин', max_length=256)
    profile = serializers.CharField(required=True, label='Профиль', max_length=256, allow_blank=True)
    email = serializers.CharField(required=True, label='Почта', max_length=256, allow_blank=True)
    created_at = serializers.DateTimeField(required=True, label='Дата создания')
    updated_at = serializers.DateTimeField(required=True, label='Дата изменения')
