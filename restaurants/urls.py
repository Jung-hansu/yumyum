from django.contrib import admin
from django.urls import path
from restaurants.views import *

urlpatterns = [
    path('<int:restaurant_id>/', RestaurantView.as_view()), #식당 조회
    path('filtered/', RestaurantFilterView.as_view()),
]
