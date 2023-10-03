from django.contrib import admin
from django.urls import path
from reviews.views import *

urlpatterns = [
    # path('', ), #리뷰 남기기
    # path('restaurant/{restaurant_id}/', ), #리뷰 조회
    # path('{review_id}', ), #리뷰 삭제

    # path('stars/', views.starAverage),
    # path('stars/input', views.inputData),
    # path('category/', views.getCategory),
    # path('mood/', views.getMood),
]
