from rest_framework import serializers
from youtube_clone.videos.models import Video
from django.contrib.auth import get_user_model

User = get_user_model()

class UploaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "username","last_name"]


class VideoSerializer(serializers.ModelSerializer):
    uploader = UploaderSerializer(read_only=True)

    class Meta:
        model = Video
        fields = ["id", "title", "embed_url", "uploader", "upload_date"]


class VideoPopularSerializer(VideoSerializer):
    popularity_score = serializers.IntegerField()

    class Meta:
        model = Video
        fields = VideoSerializer.Meta.fields + ["popularity_score"]
