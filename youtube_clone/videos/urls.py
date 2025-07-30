from django.urls import path
from .api_views.videos import VideoListCreateAPIView, VideoRetrieveUpdateDestroyAPIView
from .api_views.home_videos import home_view

app_name = "videos"

urlpatterns = [
    # Ruta para la página de inicio
    path("", home_view, name="home"),
    # Rutas para la API de videos
    path(
        "api/videos/", VideoListCreateAPIView.as_view(), name="video-list-create"
    ),  # Listar y crear videos
    path(
        "api/videos/<int:pk>/",
        VideoRetrieveUpdateDestroyAPIView.as_view(),
        name="video-detail",
    ),  # Detalle, actualizar y eliminar videos
]
