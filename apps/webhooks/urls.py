from django.urls import path
from .views import RecallWebhookView

urlpatterns = [
    path("recall/", RecallWebhookView.as_view(), name="webhook-view"),
]
