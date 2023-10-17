from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import Q

from .models import *
from .serializers import *

# Create your views here.
class RestaurantView(APIView):
    def get(self, request, **kwargs):
        restaurant_id = kwargs.get('restaurant_id')
        if restaurant_id is not None:
            try:
                restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
                return Response({"name": restaurant.name,
                                 "category": restaurant.category,
                                 "latitude": restaurant.location[0],
                                 "longitude": restaurant.location[1],
                                 "waiting": restaurant.waiting},
                                 status=status.HTTP_200_OK)
            except Restaurant.DoesNotExist: pass
        return Response({"error":"Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

class RestaurantFilterView(APIView):
    def get(self, request):
        serializer = RestaurantFilterSerializer(data=request.data)
        if serializer.is_valid():
            longitude = serializer.validated_data.get('longitude')
            latitude = serializer.validated_data.get('latitude')
            category = serializer.validated_data.get('category')

            # location query 작성 -> models.py의 Restaurant.save() 확인하기 
            user_location = Point((longitude, latitude)) # srid는 사용하는 좌표 시스템에 따라 달라질 수 있음
            print(user_location)
            query_pos = Q(location__distance_lte=(user_location, D(km=1))) # 유저 좌표 기준 반경 1km 검색

            # category query 작성
            query_cat = Q()
            for category_id in category:
                query_cat |= Q(category__contains=[category_id])

            restaurant_infos = []
            restaurants = Restaurant.objects.filter(query_pos, query_cat)
            for restaurant in restaurants:
                restaurant_info = {"restaurant_id":restaurant.restaurant_id,
                                   "name":restaurant.name,
                                   "category_ids":restaurant.category,
                                   "latitude":restaurant.location[0],
                                   "longitude":restaurant.location[1],
                                   "waiting":restaurant.waiting}
                restaurant_infos.append(restaurant_info)
            return Response({"message":"Nearby restaurants retrieved successfully", "restaurant":restaurant_infos},
                            status=status.HTTP_200_OK)
        return Response({"error":"Invalid request. Please check your input data"}, status=status.HTTP_400_BAD_REQUEST)
    
# Superuser용 식당 추가 메소드
class CreateRestaurantView(APIView):
    def post(self, request):
        if request.user.is_admin:
            serializer = RestaurantSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Create restaurant successful"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":"Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)