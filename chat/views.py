from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Message
from .serializers import ViewMessageSerializer


# APIs
class MessageView(APIView):
    def get(self, request):
        messages = Message.objects.filter(user = request.user.id)
        serializer = ViewMessageSerializer(messages, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)


# FRONTEND
class ChatView(LoginRequiredMixin,APIView):
    login_url = 'login'
    def get(self, request):
        messages = Message.objects.filter(user = request.user.id)
        serializer = ViewMessageSerializer(messages, many=True)
        context = {"messages": serializer.data}
        return render(request, 'chat/chat-view.html', context)