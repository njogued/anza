from django.db import models
from business.models import Business, Category
from users.models import CustomUser

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def is_cover_image(self):
        if self.images.filter(is_cover=True).exists():
            return self.images.filter(is_cover=True).first()
        return self.images.first()
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    is_cover = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name + ' - ' + self.image.name
    
    def save(self, *args, **kwargs):
        # Ensure that only one image is set as the cover image
        if self.is_cover:
            ProductImage.objects.filter(product=self.product).update(is_cover=False)
        super(ProductImage, self).save(*args, **kwargs)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name + ' - ' + self.reviewer.email
    
class Upvote(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='upvotes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensure that a user can only upvote a review once
        # db_table = 'upvotes'
        constraints = [
            models.UniqueConstraint(fields=['review', 'user'], name='unique_review_user_upvote')
        ]

    def __str__(self):
        return self.review.product.name + ' - ' + self.user.email