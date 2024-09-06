from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    # Create serializers for the CustomUser model
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_active', 'created_at', 'phone_number', 'profile_picture', 'password']
        read_only_fields = ['id', 'created_at', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}
    
    # Validate the password field
    def validate_username(self, value):
        if ' ' in value:
            raise serializers.ValidationError("Username cannot contain spaces")
        return value
    
    def create(self, validated_data):
        # Pop the password from validated_data to handle it separately
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.password = make_password(password)
        user.save()
        return user