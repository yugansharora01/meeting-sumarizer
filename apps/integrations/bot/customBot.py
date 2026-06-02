from typing import Optional
from apps.integrations.bot.base import BaseBotProvider

class CustomBotProvider(BaseBotProvider):
    async def create_bot(self,meeting_url,join_at:Optional[str]=None):
        pass

    async def remove_bot(self,bot_id):
        pass

    async def get_bots(self):
        pass

    async def get_transcript(self):
        pass

    async def get_recording(self):
        pass

    async def get_status(self):
        pass