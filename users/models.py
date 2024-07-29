from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None, **extra_fields):
        user = self.create_user(email, nickname, password, **extra_fields)
        UserRole.objects.create(user=user, role='Admin', is_admin=True, is_verified=True)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=255)
    is_tg_verified = models.BooleanField(blank=True, null=True)
    telegram_id = models.CharField(max_length=100, blank=True, null=True, default='', unique=True)
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
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_operator = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_admin:
            self.role = 'Admin'
        elif self.is_operator:
            self.role = 'Operator'
        else:
            self.role = 'Customer'
        super(UserRole, self).save(*args, **kwargs)

    def __str__(self):
        return f"Role for {self.user.email}: {self.role}"