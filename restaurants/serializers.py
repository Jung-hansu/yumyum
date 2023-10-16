from rest_framework import serializers
from django.contrib.gis.geos import Point, GEOSGeometry
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'category', 'latitude', 'longitude']

    # def create(self, validated_data):
    #     longitude = validated_data.pop('longitude')
    #     latitude = validated_data.pop('latitude')
    #     location = Point((longitude, latitude), srid=4326)
    #     validated_data['location'] = location
    #     return Restaurant.objects.create(**validated_data)

class RestaurantFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['longitude', 'latitude', 'category']