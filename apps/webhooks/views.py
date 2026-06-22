from apps.bots.models import BotProvider
from apps.webhooks.service import WebhookService
import json
from django.conf import settings
from apps.core.utils.verifyRecall import verify_request_from_recall
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from apps.core.utils import response
from apps.core.utils.logger import applog

class RecallWebhookView(APIView):
    authentication_classes: list = []
    permission_classes = [AllowAny]

    def post(self, request:Request):
        verify_request_from_recall(
            secret=settings.RECALL_VERIFICATION_SECRET,
            headers={k.lower(): v for k, v in request.headers.items()},
            payload=request.body.decode("utf-8"),
        )

        data = request.body.decode("utf-8")
        data = json.loads(data)

        applog.webhook("recall", event=data.get("event"), path=request.path, data=data.get("data"))

        WebhookService.handle_webhook(data["event"], data["data"],BotProvider.RECALL, request.path)

        return response.success({"message": "Webhook received"})

    def get(self, request:Request):
        applog.webhook("recall", event="get_ping", path=request.path)
        return response.success({"message": "Webhook received"})