from django.urls import path 
from .views import MeetingView

urlpatterns = [
    path('', MeetingView.as_view(), name='meeting-view'),
]