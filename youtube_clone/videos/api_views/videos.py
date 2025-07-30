from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from youtube_clone.videos.models import Video
from youtube_clone.videos.serializers.videos import VideoSerializer


class VideoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Video.objects.all().order_by("-upload_date")
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VideoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
