from django.contrib import admin
from django.urls import path, include
from users.views import *

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('<int:user_id>/', UserInfoView.as_view()),
    path('waitings/', UserWaitingView.as_view()),
    path('<int:user_id>/reviews/', UserReviewListView.as_view()),           #유저 리뷰 조회
    path('<int:user_id>/reviews/<int:review_id>', DeleteReview.as_view()),  #리뷰 삭제
]
