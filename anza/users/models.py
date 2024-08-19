from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    tiktok_link = models.URLField(max_length=200, null=True, blank=True)
    instagram_link = models.URLField(max_length=200, null=True, blank=True)
    twitter_link = models.URLField(max_length=200, null=True, blank=True)
    facebook_link = models.URLField(max_length=200, null=True, blank=True)
    linkedin_link = models.URLField(max_length=200, null=True, blank=True)
    website_link = models.URLField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    banned = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Badge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='badges/', blank=True, null=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + ' - ' + self.badge.name