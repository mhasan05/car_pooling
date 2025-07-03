# # chat/views.py

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from .models import ChatRoom, ChatMessage
# from .serializers import ChatRoomSerializer, ChatMessageSerializer
# from django.conf import settings
# from accounts.models import User  # Assuming you have a User model in accounts app
# from django.db.models import Q

# class ChatRoomView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         """
#         Get all chat rooms the current user is part of.
#         """
#         rooms = ChatRoom.objects.filter(user1=request.user) | ChatRoom.objects.filter(user2=request.user)
#         serializer = ChatRoomSerializer(rooms, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         """
#         Create a chat room between two users.
#         """
#         user1 = request.user
#         user2_id = request.data.get('user2')

#         if not user2_id:
#             return Response({"error": "user2 is required"}, status=status.HTTP_400_BAD_REQUEST)

#         if user1.id == user2_id:
#             return Response({"error": "You cannot create a room with yourself"}, status=status.HTTP_400_BAD_REQUEST)

#         user2 = User.objects.get(id=user2_id)

#         room, created = ChatRoom.objects.get_or_create(user1=user1, user2=user2)
#         serializer = ChatRoomSerializer(room)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class ChatMessageView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, room_id):
#         """
#         Get all messages in a chat room.
#         """
#         try:
#             room = ChatRoom.objects.filter(Q(id=room_id) & (Q(user1=request.user) | Q(user2=request.user))).first()
#             serializer = ChatMessageSerializer(room.messages, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except ChatRoom.DoesNotExist:
#             return Response({"error": "Chat room not found or access denied"}, status=status.HTTP_404_NOT_FOUND)

#     def post(self, request, room_id):
#         """
#         Send a message to a chat room.
#         """
#         try:
#             room = ChatRoom.objects.get(id=room_id)
#             data = {
#                 "room": room.id,
#                 "sender": request.user.id,
#                 "content": request.data.get("content")
#             }
#             serializer = ChatMessageSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except ChatRoom.DoesNotExist:
#             return Response({"error": "Chat room not found"}, status=status.HTTP_404_NOT_FOUND)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import MessageImage
from .serializers import MessageImageSerializer
from rest_framework.permissions import IsAuthenticated

class UploadImageView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        saved = []

        for img in images:
            obj = MessageImage.objects.create(image=img)
            saved.append(obj)

        serializer = MessageImageSerializer(saved, many=True)
        return Response(serializer.data)
