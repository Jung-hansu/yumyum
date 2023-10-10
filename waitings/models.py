from django.contrib.gis.db import models
from users.models import User
from restaurants.models import Restaurant

class WaitingUser(models.Model):
    waiting_user_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    restaurant = models.ForeignKey(Restaurant, models.DO_NOTHING)
    position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'Waiting_User'
