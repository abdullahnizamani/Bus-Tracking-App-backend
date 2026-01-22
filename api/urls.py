from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('index/', views.index, name='index'),
    # path('login/', views.obtain_auth_token),
    # path('auth/', include('knox.urls')), # Includes knox login/logout views
    path('auth/login/', views.login_view),
    path('auth/logout/', views.logout_view),
    path('auth/users/<str:role>', views.users, name='users'),
    path('auth/me/', views.me_view, name='me'),
    path("student/bus/", views.student_bus_view, name="student-bus"),
    path("driver/bus/", views.driver_bus_view, name="driver-bus"),
    path("buses/<int:id>/", views.bus_info, name="buses"),
    path("buses_info/", views.bus_list, name="buses_list"),
]
