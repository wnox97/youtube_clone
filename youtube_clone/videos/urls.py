from django.urls import path
from rest_framework.routers import DefaultRouter

from .api_views.videos import VideoListCreateAPIView, VideoRetrieveUpdateDestroyAPIView, RandomVideoViewSet
from .api_views.home_videos import home_view


app_name = "videos"
router = DefaultRouter()

router.register(
    r"api/videos/random", RandomVideoViewSet , basename="random-videos"
)

urlpatterns = [

    path(
        "api/videos/", VideoListCreateAPIView.as_view(), name="video-list-create"
    ),
    path(
        "api/videos/<int:pk>/",
        VideoRetrieveUpdateDestroyAPIView.as_view(),
        name="video-detail",
    ),
]

urlpatterns += router.urls

