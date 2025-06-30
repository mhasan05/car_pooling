from rest_framework import serializers
from .models import Pool,PoolMember
from vehicle.serializers import VehicleSerializer
from vehicle.models import Vehicle  # Import Vehicle model
from django.conf import settings

class PoolSerializer(serializers.ModelSerializer):
    vehicle_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(),
        source='vehicle',  # Map `vehicle_id` input to the `vehicle` field in the model
        write_only=True
    )
    vehicle = VehicleSerializer(read_only=True)  # Nested read-only details for output

    user = serializers.SerializerMethodField()

    class Meta:
        model = Pool
        fields = [
            'id', 'user', 'name', 'departure_location', 'arrival_location',
            'vehicle', 'vehicle_id', 'repeat_type', 'scheduled_days', 'start_date',
            'start_time', 'is_return_trip', 'return_time', 'created_at', 'updated_at'
        ]
    def get_user(self, obj):
        """
        Return full name and profile picture of the user.
        """
        return {
            "user_id": obj.user.id,
            "full_name": obj.user.full_name if obj.user.full_name else None,
            "profile_picture": obj.user.profile_picture.url if obj.user.profile_picture else None,
            "total_rides": obj.user.total_rides if obj.user.total_rides else 0
        }


class PoolJoinSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    profile_picture = serializers.SerializerMethodField()  # Use SerializerMethodField
    pool = PoolSerializer(read_only=True)  # Use the PoolSerializer for nested representation of the pool

    class Meta:
        model = PoolMember
        fields = [
            'id', 'user', 'full_name', 'profile_picture', 'pool', 'children',
            'role', 'pickup_location_lat', 'pickup_location_lng', 'status', 
            'driving_days', 'joined_at'
        ]

    def get_profile_picture(self, obj):
        """
        Return the full URL for the user's profile picture.
        """
        if obj.user.profile_picture:
            request = self.context.get('request')  # Use the request object to build a full URL
            if request:
                return request.build_absolute_uri(f"{settings.MEDIA_URL}{obj.user.profile_picture}")
            return f"{settings.MEDIA_URL}{obj.user.profile_picture}"
        return None  # Return None if there's no profile picture

