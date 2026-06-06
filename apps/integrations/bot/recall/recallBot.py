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

    async def get_transcript(self):
        pass

    async def get_recording(self):
        pass

    async def get_status(self):
        pass
