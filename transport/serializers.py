# buses/serializers.py
from rest_framework import serializers
from .models import Bus, Route
from users.serializers import DriverSerializer  # import from users app

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'route_str']

class BusSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = Bus
        fields = ['id', 'name', 'registration_number', 'capacity', 'is_active', 'route', 'driver']

