from django.contrib import admin
from .models import Recording

@admin.register(Recording)
class RecordingAdmin(admin.ModelAdmin):
    list_display = ('meeting', 's3_key', 'type', 'created_at')
    list_filter = ('type',)
    search_fields = ('meeting__title', 's3_key')

