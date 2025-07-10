# chat/serializers.py

from rest_framework import serializers
from .models import *

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'content', 'images', 'timestamp']  # include 'room'


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['room_id', 'user1', 'user2', 'created_at']
