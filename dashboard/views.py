from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST #
from django.db.models import Q
from users.serializers import LoginSerializer
from users.models import User, Driver
from transport.models import Bus, Route
from django.contrib import messages
from .forms import BusForm
import json
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
            return redirect('dashboard')
        else:
            messages.error(request, "Incorrect username or password")
            return redirect('login')


    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')



def buses(request):
    busObj = Bus.objects.all()
    return render(request, 'buses.html', {"busObj":busObj})

def add_bus(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        route_json = request.POST.get('coordinates')  # JSON from Mapbox
        route_str = request.POST.get('route_str')      # Optional: descriptive route string
        if form.is_valid():
            bus = form.save()
            Route.objects.create(
                    bus=bus,
                    path=json.loads(route_json),
                    route_str=route_str
                )
        return redirect('buses')
    else:
        form = BusForm()
        return render(request, "add_bus.html", {"form": form})
    
@require_POST
def delete_bus(request):
        id = request.POST.getlist('checkbox-delete')
        if not id:
            messages.error(request, "No buses selected")

            return redirect('buses')
        else:
            deleted_objs, details= Bus.objects.filter(id__in=id).delete()
            buses_deleted = details.get('transport.Bus', 0)
            if buses_deleted >= 1:
                messages.success(request, f'Successfully deleted {buses_deleted} buses')
                return redirect('buses')
            else:
                messages.error(request, "there was an error deleting the buses")

                return redirect('buses')
            


def students(request):
    return render(request, 'students.html')

# @login_required
# def users(request, role):
#     obj = User.objects.filter(role=role).values('id', 'first_name', 'last_name', 'email')
#     return JsonResponse({'users': list(obj)})

