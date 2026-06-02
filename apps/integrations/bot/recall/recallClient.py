from apps.core.exceptions import ExternalServiceError
from django.conf import settings
import httpx
from tenacity import ( retry, stop_after_attempt, wait_exponential)


class RecallClient:
    BASE_URL = "https://ap-northeast-1.recall.ai/api/v1"

    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                "Authorization":f"Token {settings.RECALL_API_KEY}",
                "Content-Type": "application/json"
                },
            )
    
    @retry(
       stop=stop_after_attempt(3),
       wait=wait_exponential(multiplier=1),
       reraise=True,
    )
    async def create_bot(self, payload: dict):
        try:
            response = await self.client.post(
                "/bot/",
                json=payload,
            )

            response.raise_for_status()

            return response.json()

        except httpx.TimeoutException:
            raise ExternalServiceError("Recall API timeout")

        except httpx.HTTPStatusError as e:
            raise ExternalServiceError(
                f"Recall API returned {e.response.status_code}"
            )

        except httpx.RequestError:
            raise ExternalServiceError(
                "Failed to connect to Recall API"
            )