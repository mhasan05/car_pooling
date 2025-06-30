from rest_framework import serializers
from .models import *

class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = [
            'id', 'user', 'make_model', 'color', 'vehicle_type',
            'seats', 'license_plate'
        ]
    


# class VehicleColorTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VehicleType
#         fields = ['id', 'name']

# class VehicleColorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VehicleColor
#         fields = ['id', 'name']