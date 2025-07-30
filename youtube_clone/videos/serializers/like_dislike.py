from rest_framework import serializers
from youtube_clone.videos.models.like_dislike import LikeDislike


class LikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = ["is_like"]
