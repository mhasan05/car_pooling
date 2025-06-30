from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *

class VehicleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        user = request.user
        if pk:
            try:
                vehicle = Vehicle.objects.get(pk=pk,user=user)
                serializer = VehicleSerializer(vehicle)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            except Vehicle.DoesNotExist:
                return Response({"status": "error", "message": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)

        vehicle = Vehicle.objects.filter(user=user)
        serializer = VehicleSerializer(vehicle, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user  # Authenticated user object
        data = request.data.copy()  # Create a mutable copy of request.data
        data['user'] = user.id  # Assign the user's ID (primary key) instead of the object
        serializer = VehicleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        user = request.user
        if not pk:
            return Response({"status": "error", "message": "Vehicle ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            vehicle = Vehicle.objects.get(pk=pk,user=user)
        except Vehicle.DoesNotExist:
            return Response({"status": "error", "message": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = VehicleSerializer(vehicle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user = request.user
        try:
            vehicle = Vehicle.objects.get(pk=pk,user=user)
            vehicle.delete()
            return Response({"status": "success", "message": "Vehicle deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Vehicle.DoesNotExist:
            return Response({"status": "error", "message": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)
        


# class VehicleColorTypeView(APIView):
#     def get(self, request, pk=None):
#         vehicle_types = VehicleType.objects.all()
#         vehicle_colors = VehicleColor.objects.all()
        
#         # Serialize the data
#         vehicle_type_serializer = VehicleColorTypeSerializer(vehicle_types, many=True)
#         vehicle_color_serializer = VehicleColorSerializer(vehicle_colors, many=True)
        
#         # Combine the data
#         data = {
#             "vehicle_types": vehicle_type_serializer.data,
#             "vehicle_colors": vehicle_color_serializer.data,
#         }
        
#         return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)
