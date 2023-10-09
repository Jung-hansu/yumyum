from django.contrib import admin
from django.urls import path
from users.views import *

urlpatterns = [
    path('', index),
    path('signup/', signup),
    path('login/', login),
    path('logout/', logout),
    # path('{user_id}', index),
    # path('threads/', ),
]
