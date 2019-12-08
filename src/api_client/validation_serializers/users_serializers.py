from rest_framework import serializers


class UsersResponse(serializers.Serializer):
    users = serializers.ListField(required=True, label='Пользователи')


class UsersData(serializers.Serializer):
    id = serializers.CharField(required=True, label='id пользователя')
    login = serializers.CharField(required=False, label='Логин', max_length=256)
    profile = serializers.CharField(required=False, label='Профиль', max_length=256)


class UsersSearchResponse(serializers.Serializer):
    users = serializers.ListField(required=True, label='Cписок пользователей')


class UsersSearchData(serializers.Serializer):
    id = serializers.CharField(required=True, label='Идентификатор пользователя', max_length=256)
    login = serializers.CharField(required=True, label='Логин', max_length=256)
    profile = serializers.CharField(required=True, label='Профиль', max_length=256)
