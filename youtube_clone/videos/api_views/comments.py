from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

# Importa los modelos y serializadores necesarios
from youtube_clone.videos.models import Video, Comment
from youtube_clone.videos.serializers.comment import CommentSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Filtra los comentarios para devolver solo los del video especificado en la URL.
        """
        video_pk = self.kwargs["pk"]
        return Comment.objects.filter(video__pk=video_pk)

    def perform_create(self, serializer):
        """
        Asocia el comentario con el video de la URL y el usuario autenticado.
        """
        video = get_object_or_404(Video, pk=self.kwargs["pk"])
        # Guarda el comentario, asignando el video y el usuario automáticamente.
        serializer.save(user=self.request.user, video=video)
