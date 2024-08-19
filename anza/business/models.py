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
    business_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='businesses')
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    tiktok_link = models.URLField(max_length=200, null=True, blank=True)
    instagram_link = models.URLField(max_length=200, null=True, blank=True)
    twitter_link = models.URLField(max_length=200, null=True, blank=True)
    facebook_link = models.URLField(max_length=200, null=True, blank=True)
    linkedin_link = models.URLField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=1000)
    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)
    categories = models.ForeignKey(Category, related_name='businesses', blank=True, on_delete=models.CASCADE, null=True)
    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0.0)
    total_rating_int = models.IntegerField(null=True, blank=True, default=0)
    reviews = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            "business_id": self.business_id,
            "name": self.name,
            "owner": self.owner.username,
            "address": self.address,
            "phone_number": self.phone_number,
            "email": self.email,
            "website": self.website,
            "tiktok_link": self.tiktok_link,
            "instagram_link": self.instagram_link,
            "twitter_link": self.twitter_link,
            "facebook_link": self.facebook_link,
            "linkedin_link": self.linkedin_link,
            "description": self.description,
            "logo": self.logo.url if self.logo else None,
            "categories": self.categories.name if self.categories else None,
            "rating": self.rating,
            "total_rating_int": self.total_rating_int,
            "reviews": self.reviews,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "archived": self.archived
        }
