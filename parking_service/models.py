from enum import Enum, auto
from django.db import models
from users.models import CustomUser

# Create your models here.

class LicensePlate(models.Model):
    plate_number = models.CharField(max_length=10)
    # accuracy = models.FloatField()
    image = models.ImageField(upload_to='license_plates/')
    detected_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.plate_number


class Vehicle(models.Model):
    plate_number = models.CharField(max_length=10)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    is_blocked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    # TODO Додати що засіб заблокований


class StatusEnum(Enum):
    UNDEFINED = 'UNDEFINED'
    PARKING = 'PARKING'
    FINISHED = 'FINISHED'


STATUS_CHOICES = [(status.name, status.name) for status in StatusEnum]


class ParkingSession(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, default=1)
    status = models.CharField(choices=STATUS_CHOICES, default=StatusEnum.UNDEFINED.name)
    started_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(blank=True, null=True)
    parking_duration = models.DurationField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.end_at and self.started_at:
            self.duration = self.end_at - self.started_at
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
