from django.contrib import admin
from .models import WebhookLog

@admin.register(WebhookLog)
class WebhookLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'method', 'url', 'status_code', 'created_at')
    list_filter = ('method', 'status_code')
    search_fields = ('url', 'method', 'body')

