from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from youtube_clone.videos.models import History, Video
from youtube_clone.videos.serializers import HistorySerializer

class HistoryViewSet(viewsets.ModelViewSet):
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return History.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        video_id = request.data.get('video_id')
        if not video_id:
            return Response(
                {"error": "El campo 'video_id' es requerido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        video = get_object_or_404(Video, pk=video_id)
        user = request.user

        history_entry, created = History.objects.get_or_create(
            user=user,
            video=video
        )

        if not created:
            history_entry.save()

        serializer = self.get_serializer(history_entry)

        response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK

        return Response(serializer.data, status=response_status)
