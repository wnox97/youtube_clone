from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q

from youtube_clone.videos.models import Video, LikeDislike
from youtube_clone.videos.serializers import LikeDislikeSerializer

class VideoInteractionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.all()

    @action(detail=True, methods=['post'], url_path='vote')
    def vote(self, request, pk=None):
        video = self.get_object()
        user = request.user

        serializer = LikeDislikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_like_action = serializer.validated_data['is_like']

        vote, created = LikeDislike.objects.update_or_create(
            user=user, video=video,
            defaults={'is_like': is_like_action}
        )

        return Response(data={"message": "Vote successful"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='likes-dislikes')
    def count_likes_dislikes(self, request, pk=None):
        video = self.get_object()
        likes_count = LikeDislike.objects.filter(video=video, is_like=True).count()
        dislikes_count = LikeDislike.objects.filter(video=video, is_like=False).count()
        return Response(data={
            "likes": likes_count,
            "dislikes": dislikes_count
        }, status=status.HTTP_200_OK)

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs['pk'])
