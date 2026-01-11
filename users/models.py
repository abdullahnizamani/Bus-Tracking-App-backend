from django.contrib.auth.models import AbstractUser
from django.db import models
# from transport.models import Bus
# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(default='avatar.svg', upload_to='profiles/')
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('driver', 'Driver'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    def __str__(self):
        return self.login_id
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(null=False, max_length=200)
    home_lat = models.DecimalField(null=True, max_digits=9, decimal_places=6)
    home_lon = models.DecimalField(null=True, max_digits=9, decimal_places=6)
    bus_id = models.ForeignKey('transport.Bus', null=True, on_delete=models.SET_NULL)
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(null=False, max_length=200)
    license_id = models.CharField(null=False, max_length=200)