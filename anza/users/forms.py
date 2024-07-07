from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    # A custom user form to handle user
    class Meta:
        model = CustomUser
        fields = ('email', 'username' )


class CustomUserChangeForm(UserChangeForm):
    # A custom user form to handle user changes
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'phone_number', 'profile_picture')

class CustomAuthenticationForm(forms.ModelForm):
    # A custom user form to handle user login
    class Meta:
        model = CustomUser
        fields = ('username', 'password')