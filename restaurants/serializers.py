from rest_framework import serializers
from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["name", "category", "longitude", "latitude"]

class OperatingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["is_24_hours", "day_of_week", "start_time", "end_time", "etc_reason"]
        
    def validate_day_of_week(self, value :list):
        for i in value:
            if i < 0 or i > 6:
                raise serializers.ValidationError("Invalid day of the week")
        return value
        
    def validate_start_time(self, value):
        time = str(value).split(':')
        if int(time[0]) < 0 or int(time[0]) >= 24 or int(time[1]) < 0 or int(time[1]) >= 60:
            raise serializers.ValidationError("Invalid type of time value")
        return value
    
    def validate_end_time(self, value):
        time = str(value).split(':')
        if int(time[0]) < 0 or int(time[0]) >= 24 or int(time[1]) < 0 or int(time[1]) >= 60:
            raise serializers.ValidationError("Wrong type of time value")
        return value