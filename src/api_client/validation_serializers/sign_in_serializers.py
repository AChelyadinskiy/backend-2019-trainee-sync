from rest_framework import serializers


class SignInPostRequest(serializers.Serializer):
    login = serializers.CharField(required=True, label='Логин', max_length=256)
    password = serializers.CharField(required=True, label='Пароль', max_length=256)


class SignInPostResponse(serializers.Serializer):
    login = serializers.CharField(required=True, label='Логин', max_length=256)
    token = serializers.CharField(required=True, label='Токен')
