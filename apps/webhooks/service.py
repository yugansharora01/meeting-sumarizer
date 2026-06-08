from asgiref.sync import async_to_sync, sync_to_async
from apps.bots.models import BotProvider
from apps.integrations.bot.factory import get_bot
from .models import WebhookLog
from apps.bots.models import BotStatus, Bot
from apps.recordings.models import Recording
from django.utils import timezone

class WebhookService():
    @classmethod
    def create_log(cls, url, method, body, headers = None, status_code=None, response_body=None):
        WebhookLog.objects.create(
            url=url,
            method=method,
            headers=headers,
            body=body,
            status_code=status_code,
        )

    @classmethod
    def handle_webhook(cls, event, data, provider, url):
        cls.create_log(
            url=url,
            method="POST",
            body=data,
            headers={"event": event},
            status_code=200
        )
        if provider == BotProvider.RECALL:
            async_to_sync(RecallWebhookService.handle_webhook)(event, data)


class RecallWebhookService():
    @classmethod
    async def handle_webhook(cls, event, data):
        if event == "bot.joining_call":
            await sync_to_async(cls.handle_joining_call)(data)
        elif event == "bot.in_waiting_room":
            await sync_to_async(cls.handle_in_waiting_room)(data)
        elif event == "bot.in_call_not_recording":
            await sync_to_async(cls.handle_in_call_not_recording)(data)
        elif event == "bot.in_call_recording":
            await sync_to_async(cls.handle_in_call_recording)(data)
        elif event == "bot.call_ended":
            await sync_to_async(cls.handle_call_ended)(data)
        elif event == "recording.done":
            await cls.handle_recording_done(data)
        elif event == "video_mixed.done":
            await sync_to_async(cls.handle_video_mixed_done)(data)
        elif event == "participant_events.done":
            await sync_to_async(cls.handle_participant_events_done)(data)
        elif event == "bot.done":
            await sync_to_async(cls.handle_done)(data)

    @classmethod
    def handle_joining_call(cls, data):
        bot = Bot.objects.get(provider_bot_id=data["bot"]["id"])
        bot.status = BotStatus.JOINING_CALL
        bot.joined_at = timezone.now()
        bot.save()
    
    @classmethod
    def handle_in_waiting_room(cls, data):
        bot = Bot.objects.get(provider_bot_id=data["bot"]["id"])
        bot.status = BotStatus.IN_WAITING_ROOM
        bot.save()
    
    @classmethod
    def handle_in_call_not_recording(cls, data):
        bot = Bot.objects.get(provider_bot_id=data["bot"]["id"])
        bot.status = BotStatus.IN_CALL_NOT_RECORDING
        bot.save()
    
    @classmethod
    def handle_in_call_recording(cls, data):
        bot = Bot.objects.get(provider_bot_id=data["bot"]["id"])
        bot.status = BotStatus.IN_CALL_RECORDING
        bot.save()
    
    @classmethod
    def handle_call_ended(cls, data):
        bot = Bot.objects.get(provider_bot_id=data["bot"]["id"])
        bot.status = BotStatus.CALL_ENDED
        bot.sub_status = data["data"]["sub_code"]
        bot.save()
    
    @classmethod
    def handle_done(cls, data):
        bot = Bot.objects.get(provider_bot_id=data["bot"]["id"])
        bot.status = BotStatus.DONE
        bot.save()
    
    @classmethod
    async def handle_recording_done(cls, data):
        bot = get_bot()
        recording_data = await bot.get_recording(data["bot"]["id"])

        def save_recordings():
            try:
                bot_obj = Bot.objects.get(provider_bot_id=data["bot"]["id"])
            except Bot.DoesNotExist:
                bot_obj = None

            if recording_data:
                for rec in recording_data:
                    Recording.objects.create(
                        bot=bot_obj,
                        s3_key=rec["s3_key"],
                        type=rec["type"],
                        provider_recording_id=rec["provider_recording_id"],
                        provider_media_id=rec["provider_media_id"],
                    )

        await sync_to_async(save_recordings)()
    
    @classmethod
    def handle_video_mixed_done(cls, data):
        pass
    
    @classmethod
    def handle_participant_events_done(cls, data):
        pass