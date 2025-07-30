from youtube_clone.videos.models import Comment
from rest_framework import serializers
from youtube_clone.videos.serializers.videos import UploaderSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UploaderSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "video", "text", "created_at"]
        read_only_fields = ["video"]
