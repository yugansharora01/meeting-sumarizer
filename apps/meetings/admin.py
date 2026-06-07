from django.contrib import admin
from .models import Meeting

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'status', 'start_time', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'meeting_url')

