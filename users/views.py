from rest_framework.views import APIView, Http404
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import User
from .forms import UserForm, LoginForm

# Create your views here.
def index(request):
    return render(request, 'users/index.html')

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        new_user = None
        print(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            print(new_user.id)
            if new_user is None:
                return Http404("User already exists.")
                    # return render(request, 'users/signup.html', {'is_exist':True})
            
        token, created = Token.objects.get_or_create(user=new_user)
        return Response({"Token":token.key})

class SignupView(APIView):
    # def get(self, request):
    #     form = UserForm()
    #     return render(request, 'users/signup.html', {'form': form})
    
    def post(self, request):
        form = UserForm(request.POST)
        new_user = None
        print(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            print(new_user.id)
            if new_user is None:
                return Http404("User already exists.")
                    # return render(request, 'users/signup.html', {'is_exist':True})
            
        token, created = Token.objects.get_or_create(user=new_user)
        return Response({"Token":token.key})
        # return redirect('/users')/

class LoginView(APIView):
    # def get(self, request):
    #     form = LoginForm()

    def post(self, request):
        form = LoginForm()
        # id = request.POST.get('id')
        # password = request.POST.get('password')
        return HttpResponse(form.data['id'])
        user = authenticate(request, username=form.data['id'], password=form.data['password'])
        if user is None:
            return Http404("Wrong input")
        
        auth_login(request, user)

        token = Token.objects.get(user=user)
        return Response({"Token":token.key})
        # return render(request, 'users/login.html', {'form':form})

class LogoutView(APIView):
    def get(self, request):
        auth_logout(request)
        token = Token.get(request)
        return Response({"Token":token.key})
        return redirect('/users')