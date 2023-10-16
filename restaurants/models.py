from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField

class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True) # 이게 맞지않나? 원투원 매핑이 잘못된거같다
    # restaurant_id = models.OneToOneField(OperatingHours, models.DO_NOTHING, primary_key=True)
    name = models.CharField(max_length=30)
    category = ArrayField(models.IntegerField())
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    location = models.PointField(srid=4326, null=True) # latitude, longitude 통합
    waiting = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'Restaurant'

    # latitude와 longitude가 저장되면 location 자체 생성
    # def save(self, *args, **kwargs):
    #     if None not in (self.latitude, self.longitude):
    #         self.location = Point(self.longitude, self.latitude, srid=4326)
    #     super(Restaurant, self).save(*args, **kwargs)

class Manager(models.Model):
    manager_id = models.AutoField(primary_key=True)
    # restaurant_id = models.IntegerField(unique=True)
    restaurant_id = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'Manager'


class OperatingHours(models.Model):
    operating_id = models.AutoField(primary_key=True)
    # restaurant_id = models.IntegerField(unique=True)
    restaurant_id = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    etc_reason = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'Operating_hours'
