from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'category', 'longitude', 'latitude']

    def create(self, validated_data):
        name = validated_data['name']
        category = validated_data['category']

        longitude = validated_data['longitude']
        latitude = validated_data['latitude']
        location = Point((longitude, latitude), srid=4326)
        validated_data['location'] = location
        # return Restaurant.objects.create(**validated_data)
        return Restaurant.objects.create(name=name, category=category, longitude=longitude, latitude=latitude, location=location)

class RestaurantFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['longitude', 'latitude', 'category']