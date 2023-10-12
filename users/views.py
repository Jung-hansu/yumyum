from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import User
from .forms import UserForm, LoginForm

# Create your views here.
def index(request):
    return render(request, 'users/index.html')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # User.objects.create() 이거 잘 보기
            new_user = User.objects.create_user(**form.cleaned_data)
            if new_user is None:
                return render(request, 'users/signup.html', {'is_exist':True})
            auth_login(request, new_user)
            return redirect('/users')
    form = UserForm()
    return render(request, 'users/signup.html', {'form': form})

def login(request):
    wrong_input = False
    if request.method == "POST":
        id = request.POST.get('id')
        password = request.POST.get('password')
        
        # 이거 작동 안해서 인증 직접 구현함
        user = authenticate(request, username=id, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('/users')
        wrong_input = True
    form = LoginForm()
    # wrong_input은 추후 삭제
    return render(request, 'users/login.html', {'wrong_input':wrong_input, 'form':form})

def logout(request):
    auth_logout(request)
    return redirect('/users')