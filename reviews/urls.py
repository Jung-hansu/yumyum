from django.urls import path
from reviews.views import *

urlpatterns = [
    path('restaurant/<int:restaurant_id>/', ReviewListView.as_view()),  #리뷰 조회
    path('write/', WriteReivew.as_view()),   #리뷰 남기기
    path('<int:review_id>/', DeleteReview.as_view()),   #리뷰 삭제
    path('thread/', ReviewThread.as_view()),   #스레드

    # path('category/', views.getCategory),
    # path('mood/', views.getMood),
]
