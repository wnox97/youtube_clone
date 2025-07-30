from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from youtube_clone.videos.models import Video
from youtube_clone.videos.serializers.videos import VideoSerializer


class VideoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Video.objects.all().order_by("-upload_date")
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)


class VideoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RandomVideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.order_by("?")
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
