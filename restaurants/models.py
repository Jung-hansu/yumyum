from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField

class Manager(models.Model):
    manager_id = models.AutoField(primary_key=True)
    restaurant_id = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'Manager'


class OperatingHours(models.Model):
    operating_id = models.AutoField(primary_key=True)
    restaurant_id = models.IntegerField(unique=True)
    day_of_week = models.IntegerField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    etc_reason = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'Operating_hours'


class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True) # 이게 맞지않나? 원투원 매핑이 잘못된거같다
    # restaurant_id = models.OneToOneField(OperatingHours, models.DO_NOTHING, primary_key=True)
    name = models.CharField(max_length=30)
    category = ArrayField(models.IntegerField())
    location = models.PointField(srid=4326) # latitude, longitude 통합
    # latitude = models.DecimalField(max_digits=65535, decimal_places=65535)    # 삭제
    # longitude = models.DecimalField(max_digits=65535, decimal_places=65535)   # 삭제
    waiting = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'Restaurant'
