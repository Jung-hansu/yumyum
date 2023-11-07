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
        serializer = RestaurantFilterSerializer(data=request.data)
        if serializer.is_valid():
            user_category = serializer.validated_data.get("category")
            user_longitude = serializer.validated_data.pop("longitude")
            user_latitude = serializer.validated_data.pop("latitude")
            user_location = Point((user_longitude, user_latitude), srid=4326)

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
                status=status.HTTP_200_OK)
        return Response({"error": "Invalid request. Please check your input data"}, status=status.HTTP_400_BAD_REQUEST)


class RestaurantWaitingView(APIView):
    # 현재 식당의 대기 팀 수 파악
    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()
        if restaurant is None:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"waiting": restaurant.waiting}, status=status.HTTP_200_OK)

    # restaurant_id는 url로, user_id는 세션 정보로 파악 (request 입력값 없음)
    # user가 AnonymousUser일 경우 user_id = null
    @transaction.atomic
    def post(self, request, restaurant_id):
        user = request.user
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()
        if restaurant is None:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_400_BAD_REQUEST)

        restaurant.waiting += 1
        restaurant.save()
        position = restaurant.waiting

        if user.is_anonymous:
            name = request.data.get("name")
            phone_number = request.data.get("phone_number")
            if len(name) == 0 or len(phone_number) != 11:
                return Response({"error": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)
            WaitingUser.objects.create(
                restaurant_id=restaurant_id,
                name=name,
                phone_number=phone_number,
                position=position,
            )
        else:
            WaitingUser.objects.create(restaurant_id=restaurant_id, user_id=user.user_id, position=position)
        return Response({"message": "Joined the queue successfully.", "position": position}, status=status.HTTP_200_OK,)

    # 웨이팅한 고객이 입장한 경우
    def put(self, request, restaurant_id):
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()
        if restaurant is None:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_400_BAD_REQUEST)

        # 식당 waiting 수 감소
        restaurant.waiting -= 1
        restaurant.save()

        # 전체 웨이팅유저 포지션 감소
        for waitingUsers in WaitingUser.objects.all():
            waitingUsers.position -= 1
            waitingUsers.save()
        return Response({"message": "Queuing successful"}, status=status.HTTP_200_OK)
