from django.urls import path
from rest_framework.routers import DefaultRouter

from youtube_clone.videos.api_views import (
    VideoInteractionViewSet,
    RandomVideoViewSet,
    CommentListCreateAPIView,
    VideoListCreateAPIView,
    VideoRetrieveUpdateDestroyAPIView,
    HistoryViewSet,
    PopularVideosViewSet
)

app_name = "videos"
router = DefaultRouter()

router.register(
    r"api/videos/random", RandomVideoViewSet , basename="random-videos"
)

router.register("api/video-interactions", VideoInteractionViewSet, basename="like-dislike")

router.register("api/videos/history", HistoryViewSet, basename="history")

router.register('api/videos/popular', PopularVideosViewSet, basename='popular-videos')


urlpatterns = [

    path(
        "api/videos/", VideoListCreateAPIView.as_view(), name="video-list-create"
    ),
    path(
        "api/videos/<int:pk>/",
        VideoRetrieveUpdateDestroyAPIView.as_view(),
        name="video-detail",
    ),

    path('api/videos/<int:pk>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
]

urlpatterns += router.urls

