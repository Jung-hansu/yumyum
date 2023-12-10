from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.measure import D
from django.db.models import Q
from django.db import transaction
from datetime import datetime

from .serializers import RestaurantSerializer
from .models import Restaurant, Reservation
from reviews.models import Review
from users.models import User


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
    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()
        if restaurant:
            return Response({
                "name": restaurant.name,
                "category": restaurant.category,
                "latitude": restaurant.location[0],
                "longitude": restaurant.location[1],
                "waiting": len(restaurant.queue.all()),
                }, status=status.HTTP_200_OK,)
        return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

############## 시간 기준 필터링 기능 추가 필요 ###############
############## 크롤링으로 키워드 기반 필터링 기능(분위기, 가격 등) 추가 필요 ###############
############## 그 식당이 문을 닫으면 같은 카테고리 식당을 거리기반 정렬해서 추천 #############
class RestaurantFilterView(APIView):
    def get(self, request):
        user_restaurant_name = request.GET.get('restaurant_name')
        user_category = request.GET.getlist('category')
        user_longitude = request.GET.get('longitude')
        user_latitude = request.GET.get('latitude')
        if not (user_longitude and user_latitude):
            return Response({"error": "Invalid request. Please check your input data"}, status=status.HTTP_400_BAD_REQUEST)
        user_location = Point((float(user_longitude), float(user_latitude)), srid=4326)

        # 요청에 해당하는 query 작성
        query = Q(name__contains=user_restaurant_name) # 이름 검색
        query &= Q(location__distance_lte=(user_location, D(km=1)))  # 반경 1km
        for category_id in user_category:
            query &= Q(category__contains=[category_id])
        now = datetime()
        print(now)

        restaurant_infos = []
        restaurants = Restaurant.objects.filter(query)
        for restaurant in restaurants:
            restaurant_info = {
                "restaurant_id": restaurant.restaurant_id,
                "name": restaurant.name,
                "category_ids": restaurant.category,
                "longitude": restaurant.location[0],
                "latitude": restaurant.location[1],
                "waiting": len(restaurant.queue.all()),
            }
            restaurant_infos.append(restaurant_info)
        return Response({
            "message": "Nearby restaurants retrieved successfully",
            "restaurant": restaurant_infos,
            },status=status.HTTP_200_OK)
    

class RestaurantWaitingView(APIView):
    # 식당 웨이팅 조회(유저)
    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()
        if not restaurant:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        waiting_list = []
        for waiting in restaurant.queue.all():
            user = waiting.user
            waiting_list.append({
                "reservation_id":waiting.reservation_id,
                "restaurant":waiting.restaurant.name,
                "user":user.name if user else 'Anonymous user',
                "phone_number":waiting.phone_number})
        return Response({
            "message":"Restaurant waiting retrieved successfully",
            "waitings": waiting_list,
            }, status=status.HTTP_200_OK)

    # 예약 등록(유저)
    @transaction.atomic
    def post(self, request, restaurant_id):
        user = request.user
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()
        if not restaurant:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

        # 회원 처리
        if user.is_authenticated:
            if restaurant.queue.filter(user=user).exists():
                return Response({"error":"Waiting already exists"}, status=status.HTTP_409_CONFLICT)
            new_reservation = Reservation.objects.create(restaurant=restaurant, user=user, phone_number=user.phone_number)
            restaurant.queue.add(new_reservation)
        # 비회원 처리
        else:
            phone_number = request.data.get('phone_number')
            if not phone_number:
                return Response({"error": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)
            if restaurant.queue.filter(phone_number=phone_number).exists():
                return Response({"error":"Waiting already exists"}, status=status.HTTP_409_CONFLICT)
            new_reservation = Reservation.objects.create(restaurant=restaurant, phone_number=phone_number)
            restaurant.queue.add(new_reservation)

        restaurant.save()
        position = len(restaurant.queue.all())
        return Response({
            "message": "Joined the queue successfully.",
            "position": position
            }, status=status.HTTP_200_OK)

    # 예약 입장(매니저)
    @transaction.atomic
    def patch(self, request, restaurant_id):
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()
        if not restaurant:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        
        queue = restaurant.queue
        if not queue.exists():
            return Response({"error": "Waiting does not exist"}, status=status.HTTP_400_BAD_REQUEST)
       
        next = queue.first()
        queue.remove(next)
        restaurant.save()

        if next.user:
            next_name = next.user.name
            next.user.reservations.remove(restaurant)
        else:
            next_name = 'Anonymous user'
        return Response({
            "message": "Queuing successful",
            "name":next_name,
            "phone_number":next.phone_number,
            }, status=status.HTTP_200_OK)

class RestaurantManagerView(APIView):
    # 매니저 추가
    def post(self, request):
        pass

class RestaurantManagementView(APIView):
    # 식당 정보 변경
    @transaction.atomic
    def put(self, request, restaurant_id):
        user = request.user
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()
        if not user.is_staff: # 매니저 존재시 매니저 여부로 확인
            return Response({"error":"Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
        if not restaurant:
            return Response({"error":"Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        
        day_of_week = request.data.get('day_of_week')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        etc_reason = request.data.get('etc_reason')
        restaurant.operating_hour = {
            "day_of_week":day_of_week,
            "start_time":start_time,
            "end_time":end_time,
            "etc_reason":etc_reason,
        }
        restaurant.save()
        return Response({
            "message":"Update restaurant operating hour successful",
            "operating_hour":restaurant.operating_hour,
            }, status=status.HTTP_200_OK)
    
    
class RestaurantReviewListView(APIView):
    def get(self, request, restaurant_id, user_id):
        user = request.user
        if user.is_authenticated:
            if restaurant_id is not None:
                restaurant = Restaurant.objects.filter(pk = restaurant_id).first() #Restaurant 가져오기
                user = User.objects.filter(user_id=user_id).first()
                if not restaurant:
                    return Response({"error":"Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
                review_infos = []
                reviews = Review.objects.filter(restaurant_id = restaurant)
                for review in reviews:
                    review_info = {
                        "review_id": review.review_id,
                        "stars": review.stars,
                        "user_id" : user.user_id,
                        "use_name" : user.name,
                        "menu" : review.menu,
                        "contents": review.contents,
                        "created_at": review.created_at,
                        "updated_at": review.updated_at,
                    }
                    review_infos.append(review_info)
                    
                responst_data = {
                    "restaurant_id" : restaurant.restaurant_id,
                    "restaurant_name" : restaurant.name,
                    "reviews" : review_infos
                }
                return Response({"ReviewList" : responst_data}, status=status.HTTP_200_OK)
            return Response({"error" : "Review not found"}, status = status.HTTP_404_NOT_FOUND)
        
class WriteReivew(APIView):   
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            restaurant_id = request.data.get('restaurant_id')
            restaurant_name = request.data.get('restaurant_name')
            stars = request.data.get('stars')
            menu = request.data.get('menu')
            contents = request.data.get('contents')
            if not (restaurant_id,restaurant_name,stars,menu,contents):
                return Response({"error": "평점과 리뷰 내용이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
            except Restaurant.DoesNotExist:
                return Response({"error": "레스토랑을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

            Review.objects.get_or_create(restaurant=restaurant, restaurant_name=restaurant_name, user=user, stars=stars, menu=menu, contents=contents)
            return Response({"message":"Review regists successfully"}, status=status.HTTP_200_OK)
        return Response({"error":"Session expired or not found"}, status=status.HTTP_400_BAD_REQUEST)