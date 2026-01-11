from django.db import models
# Create your models here.

class Route(models.Model):
    path = models.JSONField(null=True)

    # def __str__(self):
    #     return f"Route {self.id}"
class Bus(models.Model):
    name = models.CharField(null=False, max_length=200)
    registration_number = models.CharField(null=False, max_length=200)
    route_id = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True)

    driver_id = models.OneToOneField('users.Driver', null=True, on_delete=models.SET_NULL)
    capacity = models.IntegerField(null=True)
    is_active = models.BooleanField()
    
    # def __str__(self):
    #     return self.id