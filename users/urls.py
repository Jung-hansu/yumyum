from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from users.views import *

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('auth/', AuthView.as_view()),
    # path('auth/', TokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('<int:user_id>/', UserInfoView.as_view()),
    path('waitings/', UserWaitingView.as_view()),
]
