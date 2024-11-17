from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
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
        banned_usernames = [
            "admin", "superuser", "staff", "user", "root", "rootuser", 
            "adminuser", "superuser", "staffuser", "useruser", "rootadmin", "rootstaff", "profile"]
        if username in banned_usernames:
            raise forms.ValidationError("Username cannot be {}".format(username))
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username
    
class CustomUserUpdateForm(forms.ModelForm):
    # A custom user form to handle user updates
    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'phone_number', 'profile_picture',
            'tiktok_link', 'instagram_link', 'twitter_link', 'facebook_link', 
            'linkedin_link', 'whatsapp_link', 'website_link'
        )

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
    
    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            if profile_picture.size > 5 * 1024 * 1024:  # 5MB max size
                raise ValidationError("Profile picture size should not exceed 5MB.")
            # How to validate if valid file??
            # if profile_picture.get('content_type') and not profile_picture.get('content_type').startswith("image/"):
            #     raise ValidationError("Only image files are allowed.")
        return profile_picture

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