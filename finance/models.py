from datetime import datetime
from decimal import Decimal
import math
from django.db import models
from parking_service.models import ParkingSession


CURRENCY = 'UAH'

# Create your models here.
class Payment(models.Model):
    parking_session_pk = models.ForeignKey(ParkingSession, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        session = ParkingSession.objects.filter(pk=self.parking_session_pk.pk).first()
        if session and session.started_at and session.parking_duration:
            current_tariff = Tariff.objects.filter(
                start_date__lte=session.started_at,
                end_date__gte=session.started_at
            ).first()

            if current_tariff:
                # Припустимо, у Tariff є поле `rate` або аналогічне
                duration_in_hours = session.parking_duration.total_seconds() / 3600  # Перетворення тривалості в години
                hours_to_charge = Decimal(math.ceil(duration_in_hours))
                self.amount = current_tariff.price_per_hour * hours_to_charge
                print(f'AMOUNT: {self.amount}')
            else:
                # Обробка випадку, коли тариф не знайдено
                print('Tariff not found for the given session time.')
                self.amount = 0
        else:
            # Обробка випадку, коли session або її поля не визначені
            print('Invalid parking session or duration.')
            self.amount = 0

        super().save(*args, **kwargs)




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
