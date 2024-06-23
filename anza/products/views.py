from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView
from django.views import View
from .models import Product, Review, ProductImage
from .forms import CreateProductForm, ProductImageForm, UpdateProductForm
from django.urls import reverse, reverse_lazy

# Create your views here.
# class CreateProductView(LoginRequiredMixin, CreateView):
#     def get(self, request):
#         # Provide the user with a form to create a new product
#         product_form = self.form_class()
#         image_form = ProductImageForm()
#         return render(request, self.template_name, {"product_form": product_form, "image_form": image_form})
    
#     def post(self, request):
#         # Handle the form submission
#         curr_user = request.user
#         product_form = self.form_class(request.POST, request.FILES)
#         if product_form.is_valid():
#             product = product_form.save()
#             images = request.FILES.getlist('image')
#             for image in images:
#                 ProductImage.objects.create(product=product, image=image)
#             success_url = reverse('detail_product', kwargs={'product_id': product.product_id})
#             return redirect(success_url)
#         return render(request, self.template_name, {"product_form": product_form, "image_form": ProductImageForm()})
#     model = Product
#     form_class = CreateProductForm
#     success_url = reverse_lazy("home")
#     template_name = "create_product.html"
#     login_url = "/users/login"

class ProductDetailView(View):
    # A view to display the details of a product
    def get(self, request, product_id):
        product = Product.objects.get(product_id=product_id)
        images = ProductImage.objects.filter(product=product)
        reviews = Review.objects.filter(product=product)
        return render(request, "detail_product.html", {"product": product, "images": images, "reviews": reviews})
    
class ProductUpdateView(View):
    # A view to update a product
    model = Product
    form_class = UpdateProductForm
    template_name = "update_product.html"
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_success_url(self):
        return reverse_lazy('detail_product', kwargs={'product_id': self.object.product_id})
    
    def form_valid(self, form):
        product = form.save()
        product.save()
        return redirect(self.get_success_url())

class ProductDeleteView(DeleteView):
    # A view to delete a product
    model = Product
    template_name = 'delete_product.html'
    context_object_name = 'product'
    success_url = reverse_lazy('product_list')
    pk_url_kwarg = 'product_id'

class CreateReviewView(LoginRequiredMixin, CreateView):
    # A view to create a review for a product
    model = Review
    fields = ['rating', 'comment']
    template_name = 'create_review.html'
    success_url = reverse_lazy('home')
    login_url = '/users/login'

    def form_valid(self, form):
        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(product_id=product_id)
        review = form.save(commit=False)
        review.product = product
        review.user = self.request.user
        review.save()
        return redirect(reverse('detail_product', kwargs={'product_id': product_id}))
    
class UpdateReviewView(View):
    # A view to update a review
    model = Review
    fields = ['rating', 'comment']
    template_name = 'update_review.html'
    context_object_name = 'review'
    pk_url_kwarg = 'review_id'
    
    def get_success_url(self):
        return reverse_lazy('detail_product', kwargs={'product_id': self.object.product.product_id})
    
    def form_valid(self, form):
        review = form.save()
        review.save()
        return redirect(self.get_success_url())
    
class DeleteReviewView(DeleteView):
    # A view to delete a review
    model = Review
    template_name = 'delete_review.html'
    context_object_name = 'review'
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'review_id'