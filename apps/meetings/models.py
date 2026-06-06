from django.db import models
from apps.accounts.models import Profile


class MeetingStatus(models.TextChoices):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


class Meeting(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="meetings")
    meeting_url = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20, choices=MeetingStatus.choices, default=MeetingStatus.PENDING
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
