from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import DriverProfile, DeliveryJob

User = get_user_model()


class DriverProfileSerializer(serializers.ModelSerializer):
    # FIX: provide queryset for related field
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DriverProfile
        fields = ['id', 'user', 'user_id', 'license_number', 'vehicle_type', 'status']


class DeliveryJobSerializer(serializers.ModelSerializer):
    driver = DriverProfileSerializer(read_only=True)
    driver_id = serializers.PrimaryKeyRelatedField(
        queryset=DriverProfile.objects.all(),
        source='driver',
        write_only=True
    )

    class Meta:
        model = DeliveryJob
        fields = [
            'id',
            'driver',
            'driver_id',
            'order',
            'pickup_location',
            'delivery_location',
            'status',
            'scheduled_time',
            'completed_at',
        ]
