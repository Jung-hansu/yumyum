from django.contrib import admin
from django.urls import path
from restaurants.views import *

urlpatterns = [
    path('create/', CreateRestaurantView.as_view()), # 관리자용 식당 추가 기능
    path('<int:restaurant_id>/', RestaurantView.as_view()), # 식당 조회
    path('filtered/', RestaurantFilterView.as_view()), # 필터링
]
