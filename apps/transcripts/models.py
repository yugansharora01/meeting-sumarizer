from apps.meetings.models import Meeting
from django.db import models


class TranscriptStatus(models.TextChoices):
    PENDING = "pending"
    GENERATED = "generated"
    FAILED = "failed"


class Transcript(models.Model):
    meeting = models.OneToOneField(Meeting, on_delete=models.CASCADE)
    provider_transcript_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=TranscriptStatus.choices)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.meeting.title} Transcript"
