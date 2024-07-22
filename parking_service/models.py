from django.db import models
from users.models import CustomUser

# Create your models here.

class LicensePlate(models.Model):
    plate_number = models.CharField(max_length=10)
    accuracy = models.FloatField()
    image = models.ImageField(upload_to='license_plates/')
    detected_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.plate_number


class Vehicle(models.Model):
    plate_number = models.CharField(max_length=10)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
