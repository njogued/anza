from .models import Cart
from django import forms

class CartItemCreateFrom(forms.ModelForm):
    # a form to handle cart creation
    class Meta:
        model = Cart
        fields = ("Product", "Quantity")