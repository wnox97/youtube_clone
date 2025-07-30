from django.db import models
from django.conf import settings
from .video import Video


class History(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="history",
        verbose_name="Usuario",
    )
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name="viewed_by", verbose_name="Video"
    )
    watched_at = models.DateTimeField(
        auto_now=True, verbose_name="Visto por última vez"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Añadido al historial"
    )

    class Meta:

        unique_together = ("user", "video")
        ordering = ["-watched_at"]
        verbose_name = "Registro de Historial"
        verbose_name_plural = "Registros de Historial"

    def __str__(self):
        return f"{self.user.username} vio '{self.video.title}'"
