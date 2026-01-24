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
    path('drivers/', views.drivers, name='drivers'),
    path('add_students/', views.add_student, name='add_students'),
    path('add_drivers/', views.add_driver, name='add_drivers'),
    path("bulk-delete/", views.bulk_delete, name="bulk_delete_users"),
    path("bulk-assign/", views.bulk_assign, name="bulk_assign_bus"),
    path("bulk-remove/", views.bulk_remove_bus, name="bulk_remove_bus"),
    path("profile/", views.profile, name="profile"),
    path("password_reset/", views.password_reset, name="password_reset"),
    path("edit_driver/<str:id>", views.edit_driver, name="edit_driver"),
    path("edit_student/<str:id>", views.edit_student, name="edit_student"),
    path("live_map/", views.live_map, name="live_map"),
    path("edit_bus/<str:pk>", views.edit_bus, name="edit_bus"),

]

