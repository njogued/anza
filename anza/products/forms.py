from .models import Product, Review, ProductImage
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
        model = ProductImage
        fields = ['image', 'is_cover']
        widgets = {
            'image': CustomClearableFileInput(),
        }

    image = forms.ImageField(widget=CustomClearableFileInput())

class CreateReviewForm(forms.ModelForm):
    # Custom form to handle creating reviews
    class Meta:
        model = Review
        fields = ('rating', 'review', 'review_description')

    def clean_review(self):
        review = self.cleaned_data.get('review')
        if not review:
            return ' '
        return review

    def clean_review_description(self):
        review_description = self.cleaned_data.get('review_description')
        if not review_description:
            return ' '
        return review_description
    

class UpdateReviewForm(forms.ModelForm):
    # Custom form to handle updating reviews
    class Meta:
        model = Review
        fields = ('rating', 'review', 'review_description')

    def clean_review(self):
        review = self.cleaned_data.get('review')
        if not review:
            return ' ' 
        return review

    def clean_review_description(self):
        review_description = self.cleaned_data.get('review_description')
        if not review_description:
            return ' ' 
        return review_description
    
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 10:
            raise forms.ValidationError("Rating must be between 1 and 10")
        return rating