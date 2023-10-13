from django.contrib import admin
from django.urls import path
from users.views import *

urlpatterns = [
    path('', index),
    path('signup/', SignupView.as_view()),
    path('login/', login),
    path('logout/', logout),
    # path('{user_id}', index),
    # path('threads/', ),
]
