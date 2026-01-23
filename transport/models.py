from django.db import models
# Create your models here.


class Bus(models.Model):
    name = models.CharField(null=False, max_length=200)
    registration_number = models.CharField(null=False, max_length=200)
    driver_id = models.OneToOneField('users.Driver', null=True, on_delete=models.SET_NULL, related_name='bus')
    capacity = models.IntegerField(null=True)
    is_active = models.BooleanField()
    
    def __str__(self):
        return f"{self.name} ({self.registration_number})"


class Route(models.Model):
    bus = models.OneToOneField(
        Bus,
        on_delete=models.CASCADE,
        related_name="route"
    )
    path = models.JSONField()
    route_str = models.CharField(max_length=200, default="")

    def __str__(self):
        return f"Route for {self.bus.name}"
