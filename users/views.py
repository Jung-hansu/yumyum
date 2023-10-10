from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import User
from .forms import UserForm
from datetime import datetime

# Create your views here.
def index(request):
    return render(request, 'users/index.html')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('index')
    else:
        form = UserForm()
        return render(request, 'users/signup.html', {'form': form})

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
            auth_login(request, user)
            # return redirect('users:login')
            return render(request, 'users/login.html', {'is_authenticated':True, 'user':user})
        wrong_input = True
    return render(request, 'users/login.html', {'wrong_input':wrong_input})

def logout(request):
    auth_logout(request)
    # return redirect('users:login')
    return render(request, 'users/index.html', {'is_authenticated':False})