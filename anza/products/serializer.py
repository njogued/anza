from .models import Product, ProductImage
from rest_framework import serializers

class ProductImageSerializer(serializers.ModelSerializer):
    # Create serializers for the ProductImage model
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'product', 'created_at']
        read_only_fields = ['id', 'created_at']
class ProductSerializer(serializers.ModelSerializer):
    # Create serializers for the Product model
    # images = ProductImageSerializer(many=True, read_only=True)
    # new_images = serializers.ListField(child=serializers.ImageField(), write_only=True)
    class Meta:
        model = Product
        # add 'new_images' to the fields list
        fields = ['product_id', 'name', 'description', 'price', 'category', 'created_at', 'quantity', 'archived']
        read_only_fields = ['product_id', 'created_at']

    # def create(self, validated_data):
    #     new_images = validated_data.pop('new_images')
    #     product = Product.objects.create(**validated_data)
    #     for image_data in new_images:
    #         ProductImage.objects.create(product=product, image=image_data)
    #     return product