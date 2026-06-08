from apps.bots.models import Bot
from django.db import models

class Summary(models.Model):
    content = models.TextField()
    bot = models.OneToOneField(Bot,on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.bot} Summary"