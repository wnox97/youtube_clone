from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from youtube_clone.users.models import User
from youtube_clone.videos.models import Video, Comment, LikeDislike

class PopularVideosAPITest(APITestCase):
    """
    Test para el ViewSet de videos populares.
    Verifica que el ordenamiento basado en el algoritmo de popularidad sea correcto.
    """

    def setUp(self):
        """
        Crea un conjunto de datos controlado para el test.
        - 3 usuarios
        - 3 videos con diferentes fechas y niveles de interacción.
        """
        # Crear usuarios
        self.user1 = User.objects.create_user(email='user1@gmail.com', password='password123')
        self.user2 = User.objects.create_user(email='user2@gmail.com', password='password123')
        self.user3 = User.objects.create_user(email='user3@gmail.com', password='password123')

        # Fechas de referencia
        today = timezone.now()
        yesterday = today - timedelta(days=1)
        last_week = today - timedelta(days=7)

        # --- Video 1: El más popular (subido hoy) ---
        # Puntuación esperada: 100 (hoy) + 20 (2 likes) - 5 (1 dislike) + 3 (3 comments) = 118
        self.video_most_popular = Video.objects.create(
            title="Video de Hoy",
            uploader=self.user1,
        )
        LikeDislike.objects.create(video=self.video_most_popular, user=self.user1, is_like=True)
        LikeDislike.objects.create(video=self.video_most_popular, user=self.user2, is_like=True)
        LikeDislike.objects.create(video=self.video_most_popular, user=self.user3, is_like=False)
        Comment.objects.create(video=self.video_most_popular, user=self.user1, text="Comentario 1")
        Comment.objects.create(video=self.video_most_popular, user=self.user2, text="Comentario 2")
        Comment.objects.create(video=self.video_most_popular, user=self.user3, text="Comentario 3")

        # --- Video 2: Popularidad media (subido ayer) ---
        # Puntuación esperada: 0 (ayer) + 100 (10 likes) + 5 (5 comments) = 105
        self.video_medium_popular = Video.objects.create(
            title="Video de Ayer",
            uploader=self.user2,
        )
        self.video_medium_popular.upload_date = yesterday
        self.video_medium_popular.save(update_fields=['upload_date'])

        # Creamos 10 usuarios y 10 likes para este video
        for i in range(10):
            user = User.objects.create_user(email=f'liker{i}@gmail.com', password=f'password{i}' )
            LikeDislike.objects.create(video=self.video_medium_popular, user=user, is_like=True)
        # Creamos 5 comentarios
        for i in range(5):
            Comment.objects.create(video=self.video_medium_popular, user=self.user1, text=f"Comentario extra {i}")

        # --- Video 3: El menos popular (subido la semana pasada) ---
        # Puntuación esperada: 0 (antiguo) + 10 (1 like) - 25 (5 dislikes) + 1 (1 comment) = -14
        self.video_least_popular = Video.objects.create(
            title="Video Antiguo",
            uploader=self.user3,
        )
        self.video_least_popular.upload_date = last_week
        self.video_least_popular.save(update_fields=["upload_date"])
        LikeDislike.objects.create(video=self.video_least_popular, user=self.user1, is_like=True)
        # Creamos 5 usuarios y 5 dislikes
        for i in range(5):
            user = User.objects.create_user(email=f'disliker{i}@gmail.com', password=f'password{i}')
            LikeDislike.objects.create(video=self.video_least_popular, user=user, is_like=False)
        Comment.objects.create(video=self.video_least_popular, user=self.user1, text="Único comentario")

    def test_popular_videos_ordering(self):
        """
        Verifica que la API devuelva los videos en el orden de popularidad correcto.
        """
        url = reverse('videos:popular-videos-list')

        # Hacemos la petición a la API
        response = self.client.get(url)

        # 1. Verificamos que la respuesta sea exitosa (200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2. Verificamos que se devuelvan los 3 videos que creamos
        self.assertEqual(len(response.data), 3)

        # 3. Verificamos el orden de los videos por su título
        response_titles = [video['title'] for video in response.data]
        expected_order = [
            self.video_most_popular.title,   # Puntuación: 118
            self.video_medium_popular.title, # Puntuación: 105
            self.video_least_popular.title,  # Puntuación: -14
        ]

        self.assertEqual(response_titles, expected_order)
        print("\nTest de popularidad exitoso: El orden de los videos es el correcto.")
