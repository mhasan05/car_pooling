from rest_framework import serializers
from .models import User
from vehicle.models import Vehicle
from vehicle.serializers import VehicleSerializer
from children.serializers import ChildrenSerializer

class UserSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    children = ChildrenSerializer(many=True, read_only=True)
    vehicles = VehicleSerializer(many=True, read_only=True)  # Include vehicles

    class Meta:
        model = User
        fields = [
            'id', 'full_name', 'email', 'contact_number', 'profile_picture',
            'subscription_plan', 'total_rides', 'role',
            'children', 'vehicles', 'location'
        ]

    def get_location(self, obj):
        return [
            {
                "id": location.id,
                "pickup_location": location.pickup_location,
                "created_on": location.created_on,
                "updated_on": location.updated_on
            }
            for location in obj.pickup_location.all()
        ]
