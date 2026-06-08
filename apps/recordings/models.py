from apps.bots.models import Bot
from django.db import models


class RecordingType(models.TextChoices):
    AUDIO = "audio_mixed"
    VIDEO = "video_mixed"


# Create your models here.
class Recording(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, null=True, blank=True)
    provider_recording_id = models.CharField(max_length=100)
    provider_media_id = models.CharField(max_length=100)
    s3_key = models.CharField(max_length=100)
    type = models.CharField(
        max_length=20, choices=RecordingType.choices, default=RecordingType.VIDEO
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bot} Recording"
