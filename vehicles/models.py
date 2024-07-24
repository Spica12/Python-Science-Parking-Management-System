from enum import Enum
from django.db import models
from users.models import CustomUser


class StatusVehicleEnum(Enum):
    ACTIVE = 'ACTIVE'
    BLOCKED = 'BLOCKED'
    UNREGISTERED = 'UNREGISTERED'


STATUS_VEHICLE_CHOICES = [(status.name, status.name) for status in StatusVehicleEnum]

# Create your models here.
class Vehicle(models.Model):
    plate_number = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(choices=STATUS_VEHICLE_CHOICES, default=StatusVehicleEnum.ACTIVE.name)

    created_at = models.DateTimeField(auto_now_add=True)
    # TODO Додати що засіб заблокований
