from django.db import models
from django.contrib.auth import get_user_model
from youtube_clone.videos.models.video import Video

User = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]  # Ordenar comentarios por fecha de creación

    def __str__(self):
        return f"Comment by {self.user.username} on {self.video.title}"
