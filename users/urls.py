from django.contrib import admin
from django.urls import path
from users.views import *

urlpatterns = [
    path('', index),
    path('login/', login),
    path('logout/', logout),
    path('signup/', signup),
    # path('{user_id}', ), #?
    # path('threads/', ),
]
