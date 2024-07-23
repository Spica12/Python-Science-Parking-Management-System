from django.db import models
from users.models import CustomUser


# Create your models here.
class Vehicle(models.Model):
    plate_number = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    is_blocked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    # TODO Додати що засіб заблокований
