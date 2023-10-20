from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.measure import D
from django.db.models import Q

from .models import *
from .serializers import *


# Create your views here.


# Superuser용 식당 추가 메소드
class CreateRestaurantView(APIView):
    def post(self, request):
        if request.user.is_admin:
            longitude = request.data.get("longitude")
            latitude = request.data.get("latitude")
            if None in (longitude, latitude):
                return Response({"error":"Invalid input error"}, status=status.HTTP_400_BAD_REQUEST)
            
            location = GEOSGeometry(f'POINT({longitude} {latitude})', srid=4326)
            request.data["location"] = location
            serializer = RestaurantSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Create restaurant successful"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED
        )

class RestaurantView(APIView):
    def get(self, request, **kwargs):
        restaurant_id = kwargs.get("restaurant_id")
        if restaurant_id is not None:
            try:
                restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
                return Response(
                    {
                        "name": restaurant.name,
                        "category": restaurant.category,
                        "latitude": restaurant.location[0],
                        "longitude": restaurant.location[1],
                        "waiting": restaurant.waiting,
                    },
                    status=status.HTTP_200_OK,
                )
            except Restaurant.DoesNotExist:
                pass
        return Response(
            {"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND
        )

class RestaurantFilterView(APIView):
    def get(self, request):
        serializer = RestaurantFilterSerializer(data=request.data)
        if serializer.is_valid():
            user_category = serializer.validated_data.get("category")
            user_longitude = serializer.validated_data.pop('longitude')
            user_latitude = serializer.validated_data.pop('latitude')
            user_location = Point((user_longitude, user_latitude), srid=4326)

            # 요청에 해당하는 query 작성
            query = Q(location__distance_lte=(user_location, D(km=1))) # 반경 1km
            for category_id in user_category:
                query &= Q(category__contains=[category_id])

            restaurant_infos = []
            restaurants = Restaurant.objects.filter(query)
            for restaurant in restaurants:
                restaurant_info = {
                    "restaurant_id": restaurant.restaurant_id,
                    "name": restaurant.name,
                    "category_ids": restaurant.category,
                    "latitude": restaurant.location[0],
                    "longitude": restaurant.location[1],
                    "waiting": restaurant.waiting,
                }
                restaurant_infos.append(restaurant_info)
            return Response(
                {
                    "message": "Nearby restaurants retrieved successfully",
                    "restaurant": restaurant_infos,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid request. Please check your input data"},
            status=status.HTTP_400_BAD_REQUEST,
        )
