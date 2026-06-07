from django.db import models


class WebhookLog(models.Model):
    url = models.URLField()
    method = models.CharField(max_length=10)
    headers = models.JSONField(default=dict)
    body = models.JSONField(default=dict)
    status_code = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} {self.url} - {self.created_at}"
