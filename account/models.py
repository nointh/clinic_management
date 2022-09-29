from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from .managers import CustomUserManager
# Create your models here.
class User(AbstractUser):
    class UserRole(models.TextChoices):
        ADMIN = 'admin'
        BASE = 'base'
        DOCTOR = 'doctor'
        ASSISTANT = 'assistance'
    objects = CustomUserManager()
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)

    phone = models.CharField(max_length=30, blank=True, null=True)
    role = models.CharField(max_length=20,
                    choices=UserRole.choices,
                    default=UserRole.BASE)
    class Meta(AbstractUser.Meta):
       swappable = 'AUTH_USER_MODEL'

    def __str__(self) -> str:
        return self.username


