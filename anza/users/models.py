from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    business_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=False, blank=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    banned = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'username', 'phone_number']
    objects = CustomUserManager()

    def __str__(self):
        return self.username