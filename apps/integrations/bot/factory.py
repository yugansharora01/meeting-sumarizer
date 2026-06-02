from apps.integrations.bot.recall.recallClient import RecallClient
from apps.integrations.bot.customBot import CustomBotProvider
from apps.integrations.bot.recall.recallBot import RecallBotProvider
from django.conf import settings

def get_bot():
    provider = getattr(settings, "BOT_PROVIDER", "recall")
    if provider:
        provider = provider.lower().strip()

    if provider == "recall":
        return RecallBotProvider(RecallClient())
    elif provider == "custom":
        return CustomBotProvider()
    
    raise ValueError(f"Unknown or unsupported BOT_PROVIDER: {provider}")

