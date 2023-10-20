from django.contrib.postgres.fields import ArrayField
from django.contrib.gis.db import models
from users.models import User


class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    category = ArrayField(models.IntegerField())
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    location = models.GeometryField(srid=4326)
    waiting = models.IntegerField(default=0)

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


class WaitingUser(models.Model):
    waiting_user_id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, models.CASCADE)
    restaurant_id = models.ForeignKey(Restaurant, models.CASCADE)
    position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = "Waiting_User"
