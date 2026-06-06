from apps.bots.models import Bot
from apps.integrations.bot.factory import get_bot
from django.db import transaction
from apps.meetings.models import Meeting
from apps.core.exceptions import ExternalServiceError
from asgiref.sync import async_to_sync

class MeetingService:

    @classmethod
    def create_meeting(cls, meeting_url, join_at):
        with transaction.atomic():
            meeting = Meeting.objects.create(
                meeting_url=meeting_url,
                title=meeting_url,
                start_time=join_at,
            )
            bot_provider = get_bot()
            result = async_to_sync(bot_provider.create_bot)(meeting_url, join_at)
            if not result:
                raise ExternalServiceError("Failed to create bot")
            Bot.objects.create(
                meeting_id=meeting.id,
                provider=result["provider"],
                provider_bot_id=result["provider_bot_id"],
                meeting_url=meeting_url,
            )
            return meeting