from rest_framework import serializers


class UserPostRequest(serializers.Serializer):
    login = serializers.CharField(required=True, label='Логин', max_length=256)
    password = serializers.CharField(required=True, label='Пароль', max_length=256)


class UserPostResponse(serializers.Serializer):
    id = serializers.CharField(required=True, label='id пользователя')


class UserDeleteRequest(serializers.Serializer):
    id = serializers.CharField(required=True, label='id пользователя')
