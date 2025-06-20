from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import VehicleSerializer
from .models import Vehicle

class VehicleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                vehicle = Vehicle.objects.get(pk=pk)
                serializer = VehicleSerializer(vehicle)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            except Vehicle.DoesNotExist:
                return Response({"status": "error", "message": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)

        vehicle = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicle, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if not pk:
            return Response({"status": "error", "message": "Vehicle ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            vehicle = Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return Response({"status": "error", "message": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = VehicleSerializer(vehicle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
            vehicle.delete()
            return Response({"status": "success", "message": "Vehicle deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Vehicle.DoesNotExist:
            return Response({"status": "error", "message": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)