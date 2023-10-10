from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import User
from datetime import datetime

# Create your views here.
def index(request):
    return render(request, 'users/index.html')

def signup(request):
    # 이미 존재하는 유저인지 파악
    # 전화번호가 일치하거나 id & pw가 일치하는 경우 존재하는 유저로 취급
    is_exist = False
    if request.method == 'POST':
        for user in User.objects.all():
            if  user.phone_number == request.POST['phone_number'] or \
                (user.id == request.POST['id'] and user.pw == request.POST['pw']):
                is_exist = True
                break
        if not is_exist:
            return add_user(request)
    return render(request, 'users/signup.html', {'is_exist':is_exist})

def add_user(request):
    if request.method == 'POST':
        User.objects.create(
            name = request.POST['name'],
            phone_number = request.POST['phone_number'],
            id = request.POST['id'],
            pw = request.POST['pw'],
            created_at = datetime.now.date(),
            updated_at = datetime.now.date(),
        )
    return render(request, 'users/login.html')

def login(request):
    wrong_input = False
    if request.method == "POST":
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        user = authenticate(id=id, pw=pw)
        if user is not None:
            # 페이크 로그인임. 세션 기능 추가해야함
            auth_login(request, user)
            # return redirect('/users', {'is_authenticated':True, 'user':user})
            return render(request, 'users/login.html', {'is_authenticated':True, 'user':user})
        wrong_input = True
    return render(request, 'users/login.html', {'wrong_input':wrong_input})

def my_authenticate(id, pw):
    for user in User.objects.all():
        if user.id == id and user.pw == pw:
            return user
    return None

def logout(request):
    auth_logout(request)
    # return redirect('users:login')
    return render(request, 'users/index.html', {'is_authenticated':False})