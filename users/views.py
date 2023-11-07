from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db import transaction

from .models import User
from .serializers import UserSerializer
from restaurants.models import WaitingUser

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
        return Response({"Token":token.key, "messages":"Login successful"}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                token = Token.objects.get(user=user)
                token.delete()
                return Response({"message": "Logout Success"}, status=status.HTTP_200_OK)
            except Token.DoesNotExist: pass
        return Response({"error":"Session Expired or Not Found"}, status=status.HTTP_401_UNAUTHORIZED)


class UserInfoView(APIView):
    # 유저 조회
    def get(self, request, user_id):
        user = User.objects.filter(user_id=user_id).first()
        if request.user.is_authenticated and request.user == user:
            name = user.name
            phone_number = user.phone_number
            return Response({"name": name, "phone_number": phone_number}, status=status.HTTP_200_OK)
        return Response({"error":"User has no authorization"}, status=status.HTTP_401_UNAUTHORIZED)

    # 유저 삭제
    @transaction.atomic
    def delete(self, request, user_id):
        user = request.user
        if user.is_authenticated:
            try:
                token = Token.objects.get(user_id=user_id)
                if user != token.user:
                    return Response({"error":"User has no authorization"}, status=status.HTTP_401_UNAUTHORIZED)
                user.delete()
                token.delete()
                return Response({"message":"User successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
            except Token.DoesNotExist:
                Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error":"Session Expired or Not Found"}, status=status.HTTP_400_BAD_REQUEST)


class UserWaitingView(APIView):
    def get(self, request):
        user = request.user
        waiting_list = []
        if user.is_authenticated:
            waitings = WaitingUser.objects.filter(user_id=user.user_id)
        else:
            name = request.GET.get('name')
            phone_number = request.GET.get('phone_number')
            if not (name and phone_number):
                return Response({"error":"Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)
            waitings = WaitingUser.objects.filter(name=name, phone_number=phone_number)
        for waiting in waitings:
            waiting_list.append(
                {
                    "restaurant_id":waiting.restaurant_id,
                    "position":waiting.position,
                })
        return Response({"waitings":waiting_list}, status=status.HTTP_200_OK)