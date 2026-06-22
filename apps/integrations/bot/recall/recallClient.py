from apps.core.exceptions import ExternalServiceError
from apps.core.utils.logger import applog
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

            applog.api("recall.create_bot", status=response.status_code,
                       request=payload, response=response.json())
            return response.json()

        except httpx.TimeoutException:
            applog.error("api", "recall.create_bot timeout", request=payload)
            raise ExternalServiceError("Recall API timeout")

        except httpx.HTTPStatusError as e:
            applog.error("api", "recall.create_bot", status=e.response.status_code,
                         request=payload, response=e.response.text)
            raise ExternalServiceError(
                f"Recall API returned {e.response.status_code}"
            )

        except httpx.RequestError:
            applog.error("api", "recall.create_bot connection_error", request=payload)
            raise ExternalServiceError(
                "Failed to connect to Recall API"
            )

    async def get_recording(self, bot_id: str):
        result = await self.client.get(f"/bot/{bot_id}")
        return result.json()["recordings"]

    async def get_transcript(self, transcript_id: str):
        result = await self.client.get(f"/transcript/{transcript_id}")
        return result.json()

    async def create_transcript(self, recording_id: str):
        result = await self.client.post(
            f"/recording/{recording_id}/create-transcript",
            data={
                "provider": {"recallai_async": {"language_code": "auto"}},
                "diarization": {
                    "use_separate_streams_when_available": "true",
                },
            },
        )
        applog.api("recall.create_transcript", status=result.status_code,
                   recording_id=recording_id, response=result.json())
        return result.json()