from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import get_backends, authenticate, login as auth_login, logout as auth_logout
from .models import User
from .forms import UserForm, LoginForm

# Create your views here.
def index(request):
    return render(request, 'users/index.html')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
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
        user = authenticate(request, id=id, password=password)
        # user = None
        # for users in User.objects.all():
        #     if id == users.id and User.check_password(users, password):
        #         user = users
        #         break

        if user is not None:
            auth_login(request, user)
            # return redirect('/users')
            return render(request, 'users/login.html', {'user':user})
        wrong_input = True
    form = LoginForm()
    return render(request, 'users/login.html', {'wrong_input':wrong_input, 'form':form})

def logout(request):
    auth_logout(request)
    # return redirect('users:login')
    return render(request, 'users/index.html', {'is_authenticated':False})