from django.db import models
from users.models import CustomUser

class Category(models.Model):
    # Model that represents a category
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Business(models.Model):
    # Model that represents a business
    name = models.CharField(max_length=255)
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='business')
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    website = models.URLField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(upload_to='business_logos/')
    categories = models.ManyToManyField(Category, related_name='businesses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name
