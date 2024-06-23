from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import Product, Review, ProductImage
from .forms import CreateProductForm, ProductImageForm
from django.urls import reverse, reverse_lazy

# Create your views here.
class CreateProductView(LoginRequiredMixin, CreateView):
    def get(self, request):
        # Provide the user with a form to create a new product
        product_form = self.form_class()
        image_form = ProductImageForm()
        return render(request, self.template_name, {"product_form": product_form, "image_form": image_form})
    
    def post(self, request):
        # Handle the form submission
        curr_user = request.user
        product_form = self.form_class(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save()
            images = request.FILES.getlist('image')
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            success_url = reverse('detail_product', kwargs={'product_id': product.product_id})
            return redirect(success_url)
        return render(request, self.template_name, {"form": form})
    model = Product
    form_class = CreateProductForm
    success_url = reverse_lazy("home")
    template_name = "create_product.html"
    login_url = "/users/login"