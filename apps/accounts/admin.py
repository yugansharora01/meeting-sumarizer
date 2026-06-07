from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'role', 'created_at')
    search_fields = ('email', 'name', 'role')

