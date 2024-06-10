from .models import Business, Category
from django import forms

class CreateBusinessForm(forms.ModelForm):
    # A custom form to handle business creation
    class Meta:
        model = Business
        fields = ('name', 'address', 'phone_number', 'email', 'website', 'description', 'logo', 'categories')
    
    def save(self, curr_user, commit=True):
        business = super(CreateBusinessForm, self).save(commit=False)
        business.owner = curr_user
        if commit:
            business.save()
        return business