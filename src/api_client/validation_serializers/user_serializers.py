from rest_framework import serializers


class UserPostRequest(serializers.Serializer):
    login = serializers.CharField(required=True, label='Логин', max_length=256)
    password = serializers.CharField(required=True, label='Пароль', max_length=256)


class UserPostResponse(serializers.Serializer):
    id = serializers.CharField(required=True, label='id пользователя')


class UserDeleteResponse(serializers.Serializer):
    deleted_id = serializers.CharField(required=True, label='id пользователя')


class UserPatchRequest(serializers.Serializer):
    login = serializers.CharField(required=False, label='Логин', max_length=256)
    password = serializers.CharField(required=False, label='Пароль', max_length=256)
    profile = serializers.CharField(required=False, label='Профиль', max_length=256)
    email = serializers.CharField(required=False, label='Почта', max_length=256)
    email_notification = serializers.BooleanField(required=False, label='Уведомления по почте')


class UserPatchResponse(serializers.Serializer):
    updated_fields = serializers.CharField(required=True, label='Логин', max_length=256)
