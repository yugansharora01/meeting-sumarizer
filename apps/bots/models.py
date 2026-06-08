from django.db import models
from apps.meetings.models import Meeting


class BotStatus(models.TextChoices):
    PENDING = "pending"
    JOINING_CALL = "joining_call"
    IN_WAITING_ROOM = "in_waiting_room"
    IN_CALL_NOT_RECORDING = "in_call_not_recording"
    RECORDING_PERMISSION_ALLOWED = "recording_permission_allowed"
    RECORDING_PERMISSION_DENIED = "recording_permission_denied"
    IN_CALL_RECORDING = "in_call_recording"
    CALL_ENDED = "call_ended"
    DONE = "done"
    FATAL = "fatal"


class BotProvider(models.TextChoices):
    RECALL = "recall", "Recall"
    CUSTOM = "custom", "Custom"


# Create your models here.
class Bot(models.Model):
    meeting = models.OneToOneField(Meeting, on_delete=models.CASCADE, primary_key=True)
    provider = models.CharField(
        max_length=50, choices=BotProvider.choices, default=BotProvider.RECALL
    )
    provider_bot_id = models.CharField(max_length=50)
    status = models.CharField(
        max_length=30, choices=BotStatus.choices, default=BotStatus.PENDING
    )
    sub_status = models.CharField(max_length=50, null=True, blank=True)
    meeting_url = models.CharField(max_length=100)
    joined_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.meeting.title} Bot"
