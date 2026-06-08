from django.contrib import admin
from .models import Summary

@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'bot', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('bot__meeting__title', 'content')

