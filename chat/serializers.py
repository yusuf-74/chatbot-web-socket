from rest_framework import serializers
from .models import Message, Response


        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        
class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'
        
class ResponseSerializerForMessage(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['text','createdAt']
        
class ViewMessageSerializer(serializers.ModelSerializer):
    response = ResponseSerializerForMessage()
    class Meta:
        model = Message
        fields = ['text','response','createdAt']
        
