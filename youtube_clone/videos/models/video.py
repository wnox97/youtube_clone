from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Video(models.Model):
    title = models.CharField(max_length=255)
    embed_url = models.URLField(
        help_text="Pega aquí el enlace de embed de YouTube (ej. https://www.youtube.com/embed/VIDEO_ID)"
    )
    upload_date = models.DateTimeField(auto_now_add=True)
    # Otros campos si se necesitan, como el usuario que lo subió
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
