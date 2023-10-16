from rest_framework import serializers
from django.contrib.gis.geos import Point, GEOSGeometry
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'category', 'location']
    
    def to_representation(self, instance):
        # Point 객체로 변환하여 시리얼라이즈
        data = super().to_representation(instance)
        data['location'] = Point(instance.location.x, instance.location.y)
        return data

    def to_internal_value(self, data):
        # 문자열로 변환된 Point 객체를 모델 필드와 호환되게 변환
        if 'location' in data:
            x = data['location']['x']
            y = data['location']['y']
            data['location'] = GEOSGeometry(f"POINT({x} {y})")
        return super().to_internal_value(data)


class RestaurantFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['longitude', 'latitude', 'category']