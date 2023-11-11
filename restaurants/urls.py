from django.urls import path
from restaurants.views import *

urlpatterns = [
    path('', CreateRestaurantView.as_view()),                       # 관리자용 식당 추가 기능
    path('<int:restaurant_id>/', RestaurantInfoView.as_view()),     # 식당 조회
    path('filtered/', RestaurantFilterView.as_view()),              # 필터링
    path('<int:restaurant_id>/waitings/', RestaurantWaitingView.as_view()),   # 예약
]
