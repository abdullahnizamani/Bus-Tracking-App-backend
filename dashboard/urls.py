from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='dashboard'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('buses/', views.buses, name='buses'),
    path('add_bus/', views.add_bus, name='add_bus'),
    path('delete_bus/', views.delete_bus, name='delete_bus'),
    path('students/', views.students, name='students'),

]

