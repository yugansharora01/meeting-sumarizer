from django.contrib import admin
from .models import Transcript

@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    list_display = ('id', 'meeting', 'provider_transcript_id', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('meeting__title', 'content', 'provider_transcript_id')

