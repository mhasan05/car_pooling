from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChildrenSerializer
from .models import Children

class ChildrenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        user = request.user
        if pk:
            try:
                children = Children.objects.get(pk=pk,user=user)
                serializer = ChildrenSerializer(children)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            except Children.DoesNotExist:
                return Response({"status": "error", "message": "Child not found"}, status=status.HTTP_404_NOT_FOUND)

        children = Children.objects.filter(user=user)
        serializer = ChildrenSerializer(children, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user  # Authenticated user object
        data = request.data.dict()  # Create a mutable copy of request.data
        data['user'] = user.id  # Assign the user's ID (primary key) instead of the object
        serializer = ChildrenSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        user = request.user
        if not pk:
            return Response({"status": "error", "message": "Child ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            children = Children.objects.get(pk=pk,user=user)
        except Children.DoesNotExist:
            return Response({"status": "error", "message": "Child not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChildrenSerializer(children, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user= request.user
        try:
            children = Children.objects.get(pk=pk,user=user)
            children.delete()
            return Response({"status": "success", "message": "Child deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Children.DoesNotExist:
            return Response({"status": "error", "message": "Child not found"}, status=status.HTTP_404_NOT_FOUND)