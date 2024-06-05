from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    # A custom user form to handle user creation
    first_name = forms.CharField(max_length=255, required=True)
    username = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(max_length=255, required=True)
    # password = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'username', 'phone_number', 'profile_picture', 'business_name')


class CustomUserChangeForm(UserChangeForm):
    # A custom user form to handle user changes
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'phone_number', 'profile_picture', 'business_name')

class CustomAuthenticationForm(forms.ModelForm):
    # A custom user form to handle user login
    class Meta:
        model = CustomUser
        fields = ('username', 'password')