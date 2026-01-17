from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
import uuid, os
def avatar_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join(
        'profiles',
        f"{uuid.uuid4()}.{ext}"
    )


class User(AbstractUser):
    avatar = models.ImageField(default='avatar.svg', upload_to=avatar_upload_path)
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('driver', 'Driver'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    def __str__(self):
        return self.username
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(null=False, max_length=200)
    home_lat = models.DecimalField(null=True, max_digits=9, decimal_places=6)
    home_lon = models.DecimalField(null=True, max_digits=9, decimal_places=6)
    bus_id = models.ForeignKey('transport.Bus', null=True, on_delete=models.SET_NULL)
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    employee_id = models.CharField(null=False, max_length=200)
    license_id = models.CharField(null=False, max_length=200)

    def __str__(self):
        return f"{self.user.first_name} ({self.license_id})"