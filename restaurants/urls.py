from django.urls import path, include
from restaurants.views import *

urlpatterns = [
    path('', CreateRestaurantView.as_view()),                               # 관리자용 식당 추가 기능
    path('filtered/', RestaurantFilterView.as_view()),                      # 필터링
    path('<int:restaurant_id>/', RestaurantInfoView.as_view()),             # 식당 조회
    path('<int:restaurant_id>/waitings/', RestaurantWaitingView.as_view()), # 예약
    path('<int:restaurant_id>/reviews/', include('reviews.urls')),
    path('manage/', RestaurantManagerView.as_view()),                       # 식당 매니저
    path('manage/<int:restaurant_id>/', RestaurantManagementView.as_view()),# 식당 관리
]
