from django.conf import settings
from apps.core.utils.verifyRecall import verify_request_from_recall
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from apps.core.utils import response

class RecallWebhookView(APIView):
    authentication_classes: list = []
    permission_classes = [AllowAny]

    def post(self, request:Request):
        verify_request_from_recall(
            secret=settings.RECALL_VERIFICATION_SECRET,
            headers={k.lower(): v for k, v in request.headers.items()},
            payload=request.body.decode("utf-8"),
        )
        print("Verified webhook")
        print(request.body.decode("utf-8"))

        return response.success({"message": "Webhook received"})

    def get(self, request:Request):
        print(request.body)
        return response.success({"message": "Webhook received"})