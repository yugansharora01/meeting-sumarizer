from .models import WebhookLog
from apps.bots.models import BotStatus, Bot
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
    def handle_webhook(cls, event, data):
        cls.create_log(
            url="webhooks/recall",
            method="POST",
            body=data,
            headers={"event": event},
            status_code=200
        )
        if event == "bot.joining_call":
            cls.handle_joining_call(data)
        if event == "bot.in_waiting_room":
            cls.handle_in_waiting_room(data)
        if event == "bot.in_call_not_recording":
            cls.handle_in_call_not_recording(data)
        if event == "bot.in_call_recording":
            cls.handle_in_call_recording(data)
        if event == "bot.call_ended":
            cls.handle_call_ended(data)
        if event == "bot.done":
            cls.handle_done(data)

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