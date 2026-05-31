from django.shortcuts import render
from rest_framework.views import APIView
from apps.core.utils import response

# Create your views here.
class MeetingView(APIView):
    def post(self,request):
        url = request.data.get("url")
        print(url)
        return response.success({"url":url})