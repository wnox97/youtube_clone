from rest_framework import serializers
from youtube_clone.videos.models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["id", "title", "embed_url", "user", "date_post"]
