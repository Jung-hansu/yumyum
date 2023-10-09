from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.
def index(request):
    return render(request, 'users/index.html')

def signup(request):
    return HttpResponse("추후 개발 예정")

def login(request):
    if request.method == "POST":
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        user = authenticate(id=id, pw=pw)
        if user is not None:
            auth_login(request, user)
    return render(request, 'users/login.html')

def authenticate(id, pw):
    for users in User.objects.all():
        if users.id == id and users.pw == pw:
            return users
    return None

def logout(request):
    auth_logout(request)
    return redirect('users:login')