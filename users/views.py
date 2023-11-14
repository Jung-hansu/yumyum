from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db import transaction
from django.db.models import F
from datetime import time

from .models import User
from restaurants.models import Restaurant, Reservation
from .serializers import UserSerializer

# Create your views here.
class SignupView(APIView):
    @transaction.atomic
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # 근데 여기에 걸릴 일이 없음. 추후 수정할 것
            if None in serializer.validated_data:
                return Response({"error":"All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
            
            phone_number = serializer.validated_data['phone_number']
            if User.objects.filter(phone_number=phone_number).exists():
                return Response({"error":"Phone number already exists"}, status=status.HTTP_409_CONFLICT)

            min_id_len = 4
            min_password_len = 4
            id_len = len(serializer.validated_data['id'])
            password_len = len(serializer.validated_data['password'])
            if id_len < min_id_len:
                return Response({"error":f"ID must contain at least {min_id_len} characters"}, status=status.HTTP_400_BAD_REQUEST)
            if password_len < min_password_len:
                return Response({"error":f"Password must contain at least {min_password_len} characters"}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "Signup successful", "Token": token.key}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @transaction.atomic
    def post(self, request):
        # 중복 로그인 검사
        if request.user.is_authenticated:
            return Response({"error":"User is already logged in"}, status=status.HTTP_409_CONFLICT)

        # 로그인
        user = authenticate(request, username=request.data.get('id'), password=request.data.get('password'))
        if user is None:
            return Response({"error":"Invalid ID or PW"}, status=status.HTTP_401_UNAUTHORIZED)
        token, created = Token.objects.get_or_create(user=user)
        user.last_login = time()
        return Response({"Token":token.key, "messages":"Login successful"}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                token = Token.objects.get(user=user)
                token.delete()
                return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
            except Token.DoesNotExist: pass
        return Response({"error":"Session expired or not found"}, status=status.HTTP_401_UNAUTHORIZED)


class UserInfoView(APIView):
    # 유저 조회
    def get(self, request, user_id):
        user = User.objects.filter(user_id=user_id).first()
        if request.user.is_authenticated and request.user == user:
            name = user.name
            phone_number = user.phone_number
            return Response({
                	"message":"User information retrieved successfully",
                    "name": name,
                    "phone_number": phone_number
                }, status=status.HTTP_200_OK)
        return Response({"error":"User has no authorization"}, status=status.HTTP_401_UNAUTHORIZED)

    # 유저 삭제
    @transaction.atomic
    def delete(self, request, user_id):
        user = request.user
        if user.is_authenticated:
            token = Token.objects.filter(user_id=user_id).first()
            if not token :
                Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)
            if user != token.user:
                return Response({"error":"User has no authorization"}, status=status.HTTP_401_UNAUTHORIZED)
            user.delete()
            token.delete()
            return Response({"message":"User successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error":"Session expired or not found"}, status=status.HTTP_400_BAD_REQUEST)


class UserWaitingView(APIView):
    # 예약한 식당
    def get(self, request):
        user = request.user
        reservation_list = []
        # 회원 처리(비회원 처리는 프론트에서)
        if user.is_authenticated:
            for restaurant in user.reservations.all():
                queue = restaurant.queue
                position = queue.filter(reservation_id__lte=F('reservation_id')).count()
                reservation_list.append({
                    "restaurant": restaurant.name,
                    "position": position,
                })
            return Response({
                "message": "User position retrieved successfully",
                "waitings":reservation_list
            }, status=status.HTTP_200_OK)
        return Response({"error":"Session expired or not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    # 예약 취소
    @transaction.atomic
    def delete(self, request):
        user = request.user
        restaurant_id = request.data.get('restaurant_id')
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()
        if not restaurant:
            return Response({"error":"Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # 회원
        if user.is_authenticated:
            reservation = Reservation.objects.filter(restaurant=restaurant, user=user).first()
            if not reservation:
                return Response({"error":"Reservation not found"}, status=status.HTTP_404_NOT_FOUND)
        # 비회원
        else:
            phone_number = request.data.get('phone_number')
            if not phone_number:
                return Response({"error":"Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)
            
            reservation = Reservation.objects.filter(restaurant=restaurant, phone_number=phone_number).first()
            if not reservation:
                return Response({"error":"Reservation not found"}, status=status.HTTP_404_NOT_FOUND)
        
        reservation.delete()
        return Response({"message":"Reservation cancels successful"}, status=status.HTTP_200_OK)
