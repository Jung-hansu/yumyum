from django.contrib import admin
from django.urls import path
from users.views import *

urlpatterns = [
    path('', index),
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    # path('{user_id}', index),
    # path('threads/', ),
]
