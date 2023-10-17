from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .models import User
from .serializers import UserSerializer

# Create your views here.
class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # 근데 여기에 걸릴 일이 없음. 추후 수정할 것
            if None in serializer.validated_data:
                return Response({"error":"All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
            
            phone_number = serializer.validated_data['phone_number']
            if User.objects.filter(phone_number=phone_number).exists():
                return Response({"error":"Phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)

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
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                token = Token.objects.get(user=user)
                token.delete()
                return Response({"message": "Logout Success"}, status=status.HTTP_200_OK)
            except Token.DoesNotExist: pass
        return Response({"error":"Session Expired or Not Found"}, status=status.HTTP_401_UNAUTHORIZED)


class UnregisterView(APIView):
    def delete(self, request, **kwargs):
        user_id = kwargs.get('user_id')
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
                Response({"error":"User not found"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"error":"Session Expired or Not Found"}, status=status.HTTP_400_BAD_REQUEST)
