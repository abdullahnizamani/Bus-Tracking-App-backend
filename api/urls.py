from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('index/', views.index, name='index'),
    # path('login/', views.obtain_auth_token),
    # path('auth/', include('knox.urls')), # Includes knox login/logout views
    path('login/', views.login_view),
    path('logout/', views.logout_view),

]
