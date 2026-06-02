from abc import ABC,abstractmethod
from typing import Any, Dict, Optional

class BaseBotProvider(ABC):
    @abstractmethod
    async def create_bot(self,meeting_url:str, join_at:Optional[str]=None) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def remove_bot(self,bot_id:str):
        pass

    @abstractmethod
    async def get_bots(self):
        pass

    @abstractmethod
    async def get_transcript(self):
        pass

    @abstractmethod
    async def get_recording(self):
        pass

    @abstractmethod
    async def get_status(self):
        pass