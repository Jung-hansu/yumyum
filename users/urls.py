from django.contrib import admin
from django.urls import path
from users.views import *

urlpatterns = [
    path('login/', login),
    path('logout/', logout),
    path('signup/', createusers),
    # path('{user_id}', ), #?
    # path('threads/', ),
]
