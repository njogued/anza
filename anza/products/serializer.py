from .models import Product
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    # Create serializers for the Product model
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'description', 'price', 'category', 'created_at']
        read_only_fields = ['id', 'created_at']