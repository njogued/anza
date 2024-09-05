from .models import Business
from rest_framework import serializers


class BusinessSerializer(serializers.ModelSerializer):
    # create serializers for the business model
    class Meta:
        model = Business
        fields = ['id', 'name', 'description', 'owner', 'review', 'rating', 'phone_number', 'created_at']
        read_only_fields = ['id', 'created_at']