from rest_framework import serializers
from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = [
            'id', 'user', 'make_model', 'color', 'vehicle_type',
            'seats', 'license_plate'
        ]


