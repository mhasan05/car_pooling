from rest_framework import serializers
from .models import Pool,PoolMember
from vehicle.serializers import VehicleSerializer

class PoolSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)  # Include detailed vehicle info

    class Meta:
        model = Pool
        fields = [
            'id', 'user', 'name', 'departure_location', 'arrival_location', 
            'vehicle', 'repeat_type', 'scheduled_days', 'start_date', 
            'start_time', 'is_return_trip', 'return_time', 'created_at', 'updated_at'
        ]


class PoolJoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = PoolMember
        fields = [
            'id', 'user', 'pool', 'children', 
            'role','pickup_location', 'status', 'driving_days', 'joined_at'
        ]
