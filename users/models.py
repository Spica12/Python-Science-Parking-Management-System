from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, telegram_id, nickname, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, telegram_id=telegram_id, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, telegram_id, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, telegram_id, nickname, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    telegram_id = models.CharField(max_length=100, blank=True, null=True, default='')
    nickname = models.CharField(max_length=255)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class UserRole(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"Role for {self.user.email}: {self.role}"
    

class Table3(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # logic, car number, money to pay.

    def __str__(self):
        return f"Table3 entry for {self.user.email}"