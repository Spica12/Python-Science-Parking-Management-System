from django.db import models

class LicensePlate(models.Model):
    image = models.ImageField(upload_to='plate_images') 
    plate_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
