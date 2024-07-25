from django.db import models
from django.conf import settings

class Photo(models.Model):
    photo = models.BinaryField(null=True)
    recognized_car_number = models.CharField(null=True, max_length=16)
    accuracy = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.recognized_car_number
