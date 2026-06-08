from django.contrib import admin
from .models import Transcript

@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    list_display = ('id', 'recording', 'provider_transcript_id', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('recording__bot__meeting__title', 'content', 'provider_transcript_id')

