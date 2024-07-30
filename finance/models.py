from datetime import datetime
from decimal import Decimal
import math
from enum import Enum
from django.db import models
from parking_service.models import ParkingSession
from users.models import CustomUser
from django.db import transaction, IntegrityError


CURRENCY = 'UAH'
BALANCE_LIMIT = -100

class TypePaymentEnum(Enum):
    DEBIT = 'DEBIT'
    DEPOSIT = 'DEPOSIT'

TYPE_PAYMENT_CHOICES = [(type.name, type.name) for type in TypePaymentEnum]

class StatusPaymentEnum(Enum):
    CONFIRMED = 'CONFIRMED'
    UNCONFIRMED = 'UNCONFIRMED'

STATUS_PAYMENT_CHOICES = [(status.name, status.name) for status in StatusPaymentEnum]

# Create your models here.
class Payment(models.Model):
    payment_type = models.CharField(max_length=10, choices=TYPE_PAYMENT_CHOICES, default=TypePaymentEnum.DEBIT.name)
    parking_session_pk = models.ForeignKey(ParkingSession, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_tariff = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    full_hours = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    status  = models.CharField(max_length=12, choices=STATUS_PAYMENT_CHOICES, default=StatusPaymentEnum.UNCONFIRMED.name)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.payment_type == TypePaymentEnum.DEBIT.name:
            self.handle_debit()
        super().save(*args, **kwargs)

    def handle_debit(self):
        session = ParkingSession.objects.filter(pk=self.parking_session_pk.pk).first()
        if session and session.started_at and session.parking_duration:
            tariff = Tariff.objects.filter(
                start_date__lte=session.started_at,
                end_date__gte=session.started_at
            ).first()
            self.current_tariff = tariff.price_per_hour

            if self.current_tariff:
                duration_in_hours = session.parking_duration.total_seconds() / 3600  # Перетворення тривалості в години
                self.full_hours = Decimal(math.ceil(duration_in_hours))
                self.amount = -self.current_tariff * self.full_hours
                print(f'AMOUNT: {self.amount}')
            else:
                self.amount = 0
        else:
            self.amount = 0

        if session:
            try:
                with transaction.atomic():
                    user = session.vehicle.user
                    account = Account.objects.get(user=user)
                    account.withdraw(self.amount)
                    self.status = StatusPaymentEnum.CONFIRMED.name
                    # account.save()
            except IntegrityError:
                raise ValueError("Failed to withdraw the amount from the user's account.")

    def handle_confirm_deposit(self):
        if self.payment_type == TypePaymentEnum.DEPOSIT.name:
            account = Account.objects.get(user=self.user)
            with transaction.atomic():
                account.deposit(self.amount)
                self.status = StatusPaymentEnum.CONFIRMED.name
                self.save()


    def formatted_pk(self):
        return f"P-{str(self.pk).zfill(5)}"

    def __str__(self):
        return f"{self.amount:>10} {CURRENCY}"


class Tariff(models.Model):
    description = models. CharField(max_length=255, blank=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(
        default=datetime.strptime("2999-12-31", "%Y-%m-%d")
)

    def __str__(self):
        return f'Tariff: {self.price_per_hour} {CURRENCY} per hour'

class Account(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def view_balance(self):
        return f'{self.balance} {CURRENCY}'

    def deposit(self, amount):
        """
        Поповнює рахунок на вказану суму.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        try:
            with transaction.atomic():
                self.balance += amount
                self.save()
        except IntegrityError:
            raise ValueError("An error occurred while processing the withdrawal.")

        # payment = Payment(user=self.user, payment_type=TypePaymentEnum.DEPOSIT.name, amount=amount)
        # payment.save()
        # # self.balance += amount
        # self.save()

    def withdraw(self, amount):
        if amount >= 0:
            raise ValueError("Withdrawal amount must be negative.")
        try:
            with transaction.atomic():
                self.balance += amount
                self.save()
        except IntegrityError:
            raise ValueError("An error occurred while processing the withdrawal.")

    def check_balance_limit(self):
        return self.balance <= BALANCE_LIMIT
