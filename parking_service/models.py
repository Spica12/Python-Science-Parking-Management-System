from enum import Enum
from django.db import models
from random import choice
from users.models import CustomUser
from vehicles.models import Vehicle

# Create your models here.

class LicensePlate(models.Model):
    plate_number = models.CharField(max_length=10)
    # accuracy = models.FloatField()
    image = models.ImageField(upload_to='license_plates/')
    detected_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.plate_number


class StatusParkingEnum(Enum):
    UNDEFINED = 'UNDEFINED'
    ACTIVE = 'ACTIVE'
    FINISHED = 'FINISHED'


STATUS_PARKING_CHOICES = [(status.name, status.name) for status in StatusParkingEnum]


class ParkingSpot(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.id)
    class Meta:
        ordering = ['id'] 
    
class ParkingSession(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    vehicle_plate_number = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=STATUS_PARKING_CHOICES, default=StatusParkingEnum.UNDEFINED.name)
    started_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(blank=True, null=True)
    parking_duration = models.DurationField(blank=True, null=True)
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status == StatusParkingEnum.ACTIVE.name and self.parking_spot is None:
            available_spots = ParkingSpot.objects.filter(vehicle__isnull=True)
            if available_spots.exists():
                self.parking_spot = choice(available_spots)
                self.parking_spot.vehicle = self.vehicle
                self.parking_spot.save()

        if self.end_at and self.started_at:
            self.parking_duration = self.end_at - self.started_at

        if self.status == StatusParkingEnum.FINISHED.name and self.parking_spot:
            self.parking_spot.vehicle = None
            self.parking_spot.save()

        super().save(*args, **kwargs)

    def formatted_duration(self):
        if self.parking_duration:
            total_seconds = int(self.parking_duration.total_seconds())
            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            result = []
            if days > 0:
                result.append(f"{days} д.")
            if hours > 0:
                result.append(f"{hours} год.")
            if minutes > 0:
                result.append(f"{minutes} хв.")
            if seconds > 0:
                result.append(f"{seconds} сек.")

            return ", ".join(result)
        return ""

      def formatted_pk(self):
        return f"S-{str(self.pk).zfill(5)}"


# from enum import Enum, auto

# from django.urls import reverse
# from django.conf import settings
# from django.db import models
# from django.utils import timezone

# from photos.models import Photo


# # class Car(models.Model):
#     car_number = models.CharField(max_length=16, null=True)
#     photo_car = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True)
#     predict = models.FloatField(null=True)
#     PayPass = models.BooleanField(default=False)
#     blocked = models.BooleanField(default=False)

#     def __str__(self):
#         return self.car_number

#     def __str__(self):
#         return self.car_number

#     def save(self, *args, **kwargs):
#         if self.photo_car:
#             self.car_number = self.photo_car.recognized_car_number
#             self.predict = self.photo_car.accuracy
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.car_number

#     def get_absolute_url(self):
#         return reverse("car_list", kwargs={"pk": self.pk})


# class ItemTypesEnum(Enum):
#     UNDEFINED = auto()
#     CAR = auto()
#     USER = auto()
#     REGISTRATION = auto()


# class StatusEnum(Enum):
#     UNDEFINED = auto()
#     BLOCKED = auto()
#     UNBLOCKED = auto()
#     PASSED = auto()
#     UNPASSED = auto()
#     DELETED = auto()
#     REPLACED = auto()
#     ARCHIVED = auto()


# STATUS_CHOICES = [(status.name, status.name) for status in StatusEnum]
# TYPES_CHOICES = [(type.name, type.name) for type in ItemTypesEnum]


# class Log(models.Model):
#     item = models.CharField(max_length=32)
#     item_type = models.CharField(
#         choices=TYPES_CHOICES, default=ItemTypesEnum.UNDEFINED.name
#     )
#     status = models.CharField(choices=STATUS_CHOICES, default=StatusEnum.UNDEFINED.name)
#     comment = models.TextField(max_length=255)
#     username = models.CharField(max_length=32)
#     location = models.CharField(max_length=32, null=True, blank=True)
#     datetime = models.DateTimeField(default=timezone.now)

# def __str__(self):
#         return f"{self.datetime} {self.item} {self.status}  {self.comment}"
