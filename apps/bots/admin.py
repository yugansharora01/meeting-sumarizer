from django.contrib import admin
from .models import Bot

@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('meeting', 'provider', 'provider_bot_id', 'status', 'created_at')
    list_filter = ('status', 'provider')
    search_fields = ('provider_bot_id', 'meeting_url')

