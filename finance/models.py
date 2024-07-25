from datetime import datetime
from django.db import models
from parking_service.models import ParkingSession


CURRENCY = 'UAH'

# Create your models here.
class Payment(models.Model):
    parking_session_pk = models.ForeignKey(ParkingSession, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.pk} on {self.datetime} for {self.parking_session_pk} by {self.amount}"


class Tariff(models.Model):
    description = models. CharField(max_length=255, blank=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(
        default=datetime.strptime("2999-12-31", "%Y-%m-%d")
    )

    def __str__(self):
        return f'Tariff: {self.price_per_hour} {CURRENCY} per hour'
