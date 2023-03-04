import json
import openai
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY
def chatbot_response(user_input):
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=user_input,
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response["choices"][0]["text"]
    
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['user'].username
        self.room_group_name = 'chat_%s' % self.username

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "user_message", "message": message}
        )
    
    async def user_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message , "type": "human"}))
        try:
            response = await asyncio.wait_for(sync_to_async(chatbot_response)(message), timeout=10.0)
        except asyncio.TimeoutError:
            response = "Sorry, I couldn't respond within 10 seconds. Please try an easier question."
        await self.send(text_data=json.dumps({"message": response, "type": "bot"}))
        
        
        