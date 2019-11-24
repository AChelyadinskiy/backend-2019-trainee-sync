from rest_framework import serializers


class SpeechToTextPostRequest(serializers.Serializer):
    audio_file = serializers.FileField(required=True)


class SpeechToTextPostResponse(serializers.Serializer):
    result = serializers.CharField(required=True, label='Распознанный текст')
