from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.measure import D
from django.db.models import Q
from django.db import transaction

from .serializers import RestaurantSerializer, RestaurantFilterSerializer
from .models import Restaurant, WaitingUser


# Create your views here.
class CreateRestaurantView(APIView):
    @transaction.atomic
    def post(self, request):
        if request.user.is_admin:
            longitude = request.data.get("longitude")
            latitude = request.data.get("latitude")
            try:
                float(longitude)
                float(latitude)
            except ValueError:
                return Response({"error": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)

            location = GEOSGeometry(f"POINT({longitude} {latitude})", srid=4326)
            request.data["location"] = location
            serializer = RestaurantSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Create restaurant successful"}, status=status.HTTP_201_CREATED,)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)


class RestaurantInfoView(APIView):
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
                    status=status.HTTP_200_OK,)
            except Restaurant.DoesNotExist:
                pass
        return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

############## 시간 기준 필터링 기능 추가 필요 ###############
############## 크롤링으로 키워드 기반 필터링 기능(분위기, 가격 등) 추가 필요 ###############
class RestaurantFilterView(APIView):
    def get(self, request):
        user_category = request.GET.getlist('category')
        user_longitude = request.GET.get('longitude')
        user_latitude = request.GET.get('latitude')
        if not (user_longitude and user_latitude):
            return Response({"error": "Invalid request. Please check your input data"}, status=status.HTTP_400_BAD_REQUEST)
        user_location = Point((float(user_longitude), float(user_latitude)), srid=4326)
        print(user_category, user_latitude, user_longitude)

        # 요청에 해당하는 query 작성
        query = Q(location__distance_lte=(user_location, D(km=1)))  # 반경 1km
        for category_id in user_category:
            query &= Q(category__contains=[category_id])

        restaurant_infos = []
        restaurants = Restaurant.objects.filter(query)
        for restaurant in restaurants:
            restaurant_info = {
                "restaurant_id": restaurant.restaurant_id,
                "name": restaurant.name,
                "category_ids": restaurant.category,
                "longitude": restaurant.location[0],
                "latitude": restaurant.location[1],
                "waiting": restaurant.waiting,
            }
            restaurant_infos.append(restaurant_info)
        return Response(
            {
                "message": "Nearby restaurants retrieved successfully",
                "restaurant": restaurant_infos,
            },
            status=status.HTTP_200_OK)
    

class RestaurantWaitingView(APIView):
    # 현재 식당의 대기 팀 수 파악
    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()
        if restaurant is None:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"waiting": restaurant.waiting}, status=status.HTTP_200_OK)

    # 비회원인 경우 정보 입력받음
    @transaction.atomic
    def post(self, request, restaurant_id):
        user = request.user
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()
        if restaurant is None:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

        restaurant.waiting += 1
        position = restaurant.waiting
        if user.is_authenticated:
            if WaitingUser.objects.filter(user=user):
                return Response({"error":"Waiting already exists"}, status=status.HTTP_409_CONFLICT)
            WaitingUser.objects.get_or_create(
                restaurant=restaurant,
                user=user,
                name=user.name,
                phone_number=user.phone_number,
                position=position,
            )
        else:
            name = request.data.get("name")
            phone_number = request.data.get("phone_number")
            if not (name and phone_number):
                return Response({"error": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)
            if WaitingUser.objects.filter(name=name, phone_number=phone_number):
                return Response({"error":"Waiting already exists"}, status=status.HTTP_409_CONFLICT)
            WaitingUser.objects.get_or_create(
                restaurant=restaurant,
                name=name,
                phone_number=phone_number,
                position=position,
            )
        restaurant.save()
        return Response({"message": "Joined the queue successfully.", "position": position}, status=status.HTTP_200_OK)

    # 웨이팅한 고객이 입장한 경우
    @transaction.atomic
    def put(self, request, restaurant_id):
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()
        if restaurant is None:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        if not WaitingUser.objects.exists():
            return Response({"error": "Waiting does not exist"}, status=status.HTTP_400_BAD_REQUEST)
       
       # 식당 waiting 감소
        restaurant.waiting -= 1
        restaurant.save()

        # 전체 웨이팅유저 포지션 감소
        WaitingUser.objects.filter(position=1).delete()
        for waitingUsers in WaitingUser.objects.all():
            waitingUsers.position -= 1
            waitingUsers.save()
        return Response({"message": "Queuing successful"}, status=status.HTTP_200_OK)
