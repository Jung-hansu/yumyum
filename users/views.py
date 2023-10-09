from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate

# Create your views here.
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

def logout(request):
    auth_logout(request)
    return redirect('users:login')