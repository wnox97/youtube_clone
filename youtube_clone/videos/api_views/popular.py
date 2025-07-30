from django.utils import timezone
from django.db.models import Count, Q, Case, When, Value, IntegerField
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from youtube_clone.videos.models import Video
from youtube_clone.videos.serializers import VideoPopularSerializer

class PopularVideosViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Un ViewSet para listar los videos más populares basado en un
    algoritmo de puntuación personalizado.

    La puntuación se calcula como:
    - +100 puntos si el video es de hoy.
    - +10 puntos por cada 'like'.
    - -5 puntos por cada 'dislike'.
    - +1 punto por cada comentario.
    """
    serializer_class = VideoPopularSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Construye un queryset que anota cada video con un 'popularity_score'
        y lo ordena de mayor a menor.
        """
        today = timezone.now().date()

        today_factor = Case(
            When(upload_date__date=today, then=Value(100)),
            default=Value(0),
            output_field=IntegerField()
        )

        likes_score = 10 * Count(
            "likedislike", filter=Q(likedislike__is_like=True), distinct=True
        )
        dislikes_score = -5 * Count(
            "likedislike", filter=Q(likedislike__is_like=False), distinct=True
        )
        comments_score = Count("comment", distinct=True)

        queryset = Video.objects.annotate(
            popularity_score=(
                today_factor + likes_score + dislikes_score + comments_score
            )
        ).order_by('-popularity_score')

        return queryset
