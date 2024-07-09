from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from django.contrib.auth import authenticate
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    # A custom user form to handle user
    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username


class CustomUserChangeForm(UserChangeForm):
    # A custom user form to handle user changes
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'phone_number', 'profile_picture')

class CustomAuthenticationForm(AuthenticationForm):
    # A custom user form to handle user login
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    username = forms.EmailField(label='Email', widget=forms.EmailInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not CustomUser.objects.filter(email=username).exists():
            raise forms.ValidationError("User with email does not exist")   
        else:     
            self.user_cache = authenticate(self.request, email=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid login credentials")
            elif self.user_cache.archived is True or self.user_cache.banned is True:
                raise forms.ValidationError("User banned or deleted, contact support")
            # login(self.request, self.user_cache)
            return self.cleaned_data