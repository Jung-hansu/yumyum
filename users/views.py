from rest_framework.views import APIView, Http404
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import User
from .serializers import UserSerializer
from .forms import UserForm, LoginForm

# Create your views here.
def index(request):
    return render(request, 'users/index.html')

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = User.objects.create_user(**request.data)
            if new_user is None:
                return Response({"error":"User already exists"}, status=status.HTTP_400_BAD_REQUEST)
            token, created = Token.objects.get_or_create(user=new_user)
            return Response({"Token":token.key}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, username=serializer.data['id'], password=serializer.data['password'])
            if user is None:
                return Response({"error":"User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            auth_login(request, user)
            token = Token.objects.get(user=user)
            return Response({"Token":token.key}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutView(APIView):
    def get(self, request):
        auth_logout(request)
        token = Token.objects.get() # 여기 고치기
        return Response({"Token":token.key})