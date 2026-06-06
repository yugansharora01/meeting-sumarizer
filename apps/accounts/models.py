from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    role = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)