
from apps.core.exceptions import ValidationError
from apps.integrations.bot.factory import get_bot
from rest_framework.views import APIView
from apps.core.utils import response
from asgiref.sync import async_to_sync

# Create your views here.
class MeetingView(APIView):
    def post(self,request):
        url = request.data.get("url")
        if not url:
            raise ValidationError("meeting url is required")
        
        join_at = request.data.get("joinAt")
        if not join_at:
            raise ValidationError("joinAt time is required")
        print(url)
        bot_provider = get_bot()
        result = async_to_sync(bot_provider.create_bot)(url,join_at)
        return response.success(result)