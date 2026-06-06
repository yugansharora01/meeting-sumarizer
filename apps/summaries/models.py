from django.db import models
from apps.meetings.models import Meeting

class Summary(models.Model):
    content = models.TextField()
    meeting = models.OneToOneField(Meeting,on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.meeting.title} Summary"