from rest_framework import serializers


class SubscriptionPostRequest(serializers.Serializer):
    followed_id = serializers.CharField(required=True, label='id пользователя')


class SubscriptionPostResponse(serializers.Serializer):
    followed_id = serializers.CharField(required=True, label='id пользователя')
    flag = serializers.BooleanField(required=True, label='Флаг подписки')
