from rest_framework import serializers
from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["name", "category", "longitude", "latitude", "location"]

class RestaurantFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["longitude", "latitude", "category"]
