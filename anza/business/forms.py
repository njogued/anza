from .models import Business, Category
from django import forms

class CreateBusinessForm(forms.ModelForm):
    # A custom form to handle business creation
    class Meta:
        model = Business
        fields = ('name', 'phone_number', 'description', 'categories', 'logo')
    
    # def save(self, curr_user, commit=True):
    #     business = super(CreateBusinessForm, self).save(commit=False)
    #     business.owner = curr_user
    #     if commit:
    #         business.save()
    #     return business

class BusinessUpdateForm(forms.ModelForm):
    # A custom form to handle business updates
    class Meta:
        model = Business
        fields = ('name', 'address', 'phone_number', 'email', 'website', 'description', 'logo', 'categories', 'facebook_link', 'twitter_link', 'instagram_link', 'linkedin_link', 'tiktok_link')