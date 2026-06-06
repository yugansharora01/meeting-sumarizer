
from apps.meetings.services import MeetingService
from apps.core.exceptions import ValidationError
from rest_framework.views import APIView
from apps.core.utils import response

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
        result = MeetingService.create_meeting(request.user, url, join_at)
        
        return response.success({
            "id": result.id,
            "title": result.title,
            "meeting_url": result.meeting_url,
            "status": result.status,
            "start_time": result.start_time,
        })