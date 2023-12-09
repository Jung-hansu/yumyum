from django.contrib import admin
from django.urls import path, include
from users.views import *

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('<int:user_id>/', UserInfoView.as_view()),
    path('waitings/', UserWaitingView.as_view()),
    path('<int:user_id>/reviews/', include('reviews.urls')),    #리뷰로 연결
]
