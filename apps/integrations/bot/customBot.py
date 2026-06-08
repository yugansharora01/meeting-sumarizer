from typing import Optional
from apps.integrations.bot.base import BaseBotProvider


class CustomBotProvider(BaseBotProvider):
    async def create_bot(self, meeting_url, join_at: Optional[str] = None):
        pass

    async def remove_bot(self, bot_id):
        pass

    async def get_bots(self):
        pass

    async def get_transcript(self, bot_id: str):
        pass

    async def get_recording(self, bot_id: str) -> list:
        return []

    async def get_status(self, bot_id: str):
        pass
