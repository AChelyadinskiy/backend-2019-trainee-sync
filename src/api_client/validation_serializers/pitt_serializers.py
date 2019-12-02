from rest_framework import serializers


class PittPostRequest(serializers.Serializer):
    audio_file = serializers.FileField(required=True)


class PittPostResponse(serializers.Serializer):
    id = serializers.CharField(required=True, label='Питт')


class PittDeleteResponse(serializers.Serializer):
    deleted_id = serializers.CharField(required=True, label='Питт')
