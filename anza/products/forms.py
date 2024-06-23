from .models import Product
from django import forms
from .widgets import CustomClearableFileInput

class CreateProductForm(forms.ModelForm):
    # A custom form to handle product creation
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'quantity', 'category')

class UpdateProductForm(forms.ModelForm):
    # A custom form to handle product updates
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'quantity', 'category')

class ProductImageForm(forms.ModelForm):
    # A custom form to handle product image uploads
    class Meta:
        model = Product
        fields = ['image']
        widgets = {
            'image': CustomClearableFileInput(),
        }

    image = forms.ImageField(widget=CustomClearableFileInput())