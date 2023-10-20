from django.contrib.postgres.fields import ArrayField
from django.contrib.gis.db import models


class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=30)
    category = ArrayField(models.IntegerField())
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    location = models.GeometryField(srid=4326)
    waiting = models.IntegerField(default=0) #blank 옵션이 뭔지 찾아보기, DB 데이터 0 들어가는지 확인

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = "Restaurant"


class Manager(models.Model):
    manager_id = models.AutoField(primary_key=True)
    restaurant_id = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = "Manager"


class OperatingHours(models.Model):
    operating_id = models.AutoField(primary_key=True)
    restaurant_id = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    etc_reason = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = "Operating_hours"
