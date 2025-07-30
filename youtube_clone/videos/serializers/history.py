from rest_framework import serializers
from ..models import History
from .videos import VideoSerializer  # Reutilizamos el serializador de Video

class HistorySerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)

    class Meta:
        model = History
        fields = ['id', 'video', 'watched_at']
