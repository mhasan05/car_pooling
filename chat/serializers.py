from rest_framework import serializers
from .models import Message, ChatRoom, MessageImage

class MessageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageImage
        fields = ['id', 'image']

class MessageSerializer(serializers.ModelSerializer):
    images = MessageImageSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'images', 'timestamp']

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'user1', 'user2', 'created_at']
