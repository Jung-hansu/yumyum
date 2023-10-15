from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import Q

from .models import Manager, Restaurant, OperatingHours
from .serializers import RestaurantFilterSerializer

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
        serializer = RestaurantFilterSerializer()
        if serializer.is_valid():
            latitude = serializer.validated_data.get('latitude')
            longitude = serializer.validated_data.get('longitude')
            category = serializer.validated_data.get('category')

            # location query 작성            
            user_location = Point(latitude, longitude, srid=4326) # srid는 사용하는 좌표 시스템에 따라 달라질 수 있음
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
    