from django.contrib.gis.db import models

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
    restaurant = models.OneToOneField(OperatingHours, models.DO_NOTHING, primary_key=True)
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    longitude = models.DecimalField(max_digits=65535, decimal_places=65535)
    latitude = models.DecimalField(max_digits=65535, decimal_places=65535)
    waiting = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'Restaurant'
