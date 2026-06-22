from apps.recordings.models import Recording
from apps.integrations.bot.base import BaseBotProvider
from typing import Any, Dict, Optional


class RecallBotProvider(BaseBotProvider):
    PROVIDER_NAME = "recall"

    def __init__(self, recall_client):
        self.recall_client = recall_client

    async def create_bot(
        self, meeting_url: str, join_at: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        payload = {
            "meeting_url": meeting_url,
            "bot_name": "MeetPulse",
            "join_at": join_at,
        }

        bot = await self.recall_client.create_bot(payload)

        return {
            "provider": self.PROVIDER_NAME,
            "provider_bot_id": bot["id"],
            "recording_config": bot["recording_config"],
        }

    async def remove_bot(self, bot_id):
        pass

    async def get_bots(self):
        pass

    async def get_transcript(self, bot_id: str):
        pass

    async def create_transcript(self, recording_id: str):
        await self.recall_client.create_transcript(recording_id)

    async def get_recording(self, bot_id: str) -> list:
        recordings = await self.recall_client.get_recording(bot_id)
        if len(recordings) == 0:
            return []
        media = recordings[0]["media_shortcuts"]
        results = []
        provider_recording_id = recordings[0]["id"]
        if media.get("video_mixed"):
            results.append({
                "type": "video_mixed",
                "s3_key": media["video_mixed"]["data"]["download_url"],
                "provider_recording_id": provider_recording_id,
                "provider_media_id": media["video_mixed"].get("id"),
            })
        if media.get("audio_mixed"):
            results.append({
                "type": "audio_mixed",
                "s3_key": media["audio_mixed"]["data"]["download_url"],
                "provider_recording_id": provider_recording_id,
                "provider_media_id": media["audio_mixed"].get("id"),
            })
        return results

    async def get_status(self, bot_id: str):
        pass
