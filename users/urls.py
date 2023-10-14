from django.contrib import admin
from django.urls import path
from users.views import *

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('<int:user_id>/', UnregisterView.as_view()),
    # path('threads/', ThreadView.as_vie()),
]
