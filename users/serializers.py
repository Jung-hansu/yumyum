from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    # views.py에서 따로 null 검사
    name = serializers.CharField(allow_null=True)
    phone_number = serializers.CharField(allow_null=True)
    id = serializers.CharField(allow_null=True)
    password = serializers.CharField(allow_null=True)

    class Meta:
        model = User
        fields = ['name', 'phone_number', 'id', 'password']
        extra_kwargs = {"password": {"write_only":True}}