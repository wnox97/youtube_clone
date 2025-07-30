from django.db import models
from django.contrib.auth import get_user_model
from youtube_clone.videos.models.video import Video

User = get_user_model()


class LikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    is_like = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "user",
            "video",
        )  # Un usuario solo puede dar like/dislike una vez por video

    def __str__(self):
        return f"{self.user.username} {'likes' if self.is_like else 'dislikes'} {self.video.title}"
