from rest_framework import serializers

from pitter.models.pitt import Pitt


class PittsResponse(serializers.Serializer):
    feed = serializers.ListField(required=True, label='Пользователи')


class PittsData(serializers.ModelSerializer):
    profile = serializers.CharField(source='user.profile')

    class Meta:
        model = Pitt
        fields = ('profile', 'audio_file', 'audio_file_transcription', 'created_at',)
