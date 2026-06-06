from django.db import models
from apps.meetings.models import Meeting

class RecordingType(models.TextChoices):
    AUDIO = "audio"
    VIDEO = "video"

# Create your models here.
class Recording(models.Model):
    meeting = models.OneToOneField(
        Meeting, on_delete=models.DO_NOTHING, primary_key=True
    )
    s3_key = models.CharField(max_length=100)
    type = models.CharField(max_length=20,choices=RecordingType.choices,default=RecordingType.AUDIO)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.meeting.title} Recording"