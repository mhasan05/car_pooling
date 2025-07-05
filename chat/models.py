from django.db import models
from django.conf import settings

class ChatRoom(models.Model):
    room_id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_user1')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room: {self.user1} & {self.user2}"

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    images = models.ImageField(upload_to='chat/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class MessageImage(models.Model):
    image = models.ImageField(upload_to='chat/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
