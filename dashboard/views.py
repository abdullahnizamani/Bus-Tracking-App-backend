from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from users.serializers import LoginSerializer
from users.models import User
from django.contrib import messages
# Create your views here.

@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "The user does not exist")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('index')
        else:
            messages.error(request, "Incorrect username or password")
            return redirect('login')


    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')



def buses(request):
    return render(request, 'buses.html')