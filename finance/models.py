from datetime import datetime
from django.db import models
from parking_service.models import ParkingSession


CURRENCY = 'UAH'

# Create your models here.
class Payment(models.Model):
    parking_session_id = models.ForeignKey(ParkingSession, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} on {self.datetime} for {self.parking_session_id} by {self.amount}"


class Tariff(models.Model):
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(
        default=datetime.strptime("2999-12-31 23:59:59", "%Y-%m-%d %H:%M:%S")
    )

    def __str__(self):
        return f'Tariff: {self.price_per_hour} {CURRENCY} per hour'
