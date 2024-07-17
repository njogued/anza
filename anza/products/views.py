from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views import View
from .models import Product, Review, ProductImage
from .forms import UpdateProductForm, CreateReviewForm, UpdateReviewForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseForbidden, JsonResponse

class ProductDetailView(View):
    # A view to display the details of a product
    form_class = CreateReviewForm

    def get(self, request, product_id):
        product = Product.objects.get(product_id=product_id)
        images = ProductImage.objects.filter(product=product)
        reviews = Review.objects.filter(product=product)
        self_review_bool = False
        self_review = None
        if request.user.is_authenticated:
            self_review = reviews.filter(reviewer=request.user).first()
            if self_review:
                self.form_class = UpdateReviewForm
                self_review_bool = True
        rev_count = reviews.count()
        context = {"product": product, "images": images, "reviews": reviews, "rev_count": rev_count, "form": self.form_class, "self_review": self_review, "self_review_bool": self_review_bool}

        return render(request, "detail-product.html", context)
    
class ProductUpdateView(UpdateView):
    # A view to update a product
    model = Product
    form_class = UpdateProductForm
    template_name = "update_product.html"
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_success_url(self):
        return reverse_lazy('detail_product', kwargs={'product_id': self.object.product_id})
    
    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.business.owner != self.request.user:
            return HttpResponseForbidden("You are not allowed to update business")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        product = form.save()
        product.save()
        return redirect(self.get_success_url())

class ProductDeleteView(DeleteView):
    # A view to delete a product
    model = Product
    template_name = 'delete_product.html'
    context_object_name = 'product'
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'product_id'

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.business.owner != self.request.user:
            return HttpResponseForbidden("You are not allowed to update business")
        return super().dispatch(request, *args, **kwargs)

class CreateReviewView(LoginRequiredMixin, CreateView):
    # A view to create a review for a product
    model = Review
    form_class = CreateReviewForm
    template_name = 'create_review.html'
    success_url = reverse_lazy('home')
    login_url = '/users/login'

    def get(self, request, product_id):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request, product_id):
        form = self.form_class(request.POST)
        curr_user = request.user
        if form.is_valid():
            product_id = self.kwargs.get('product_id')
            product = Product.objects.get(product_id=product_id)
            review = form.save(commit=False)
            review.product = product
            review.reviewer = curr_user
            review.save()
            success_url = reverse('detail_product', kwargs={'product_id': product.product_id})
            return redirect(success_url)
        return render(request, self.template_name, {"form": form})
    
class UpdateReviewView(UpdateView):
    # A view to update a review
    model = Review
    context_object_name = 'review'
    pk_url_kwarg = 'review_id'
    
    def get_success_url(self):
        return reverse_lazy('detail_product', kwargs={'product_id': self.object.product.product_id})
    
    def form_invalid(self, form):
        if form.errors:
            if self.request.is_ajax():
                return JsonResponse(form.errors, status=400)
            return redirect(self.get_success_url())
        
    def post(self, request, review_id):
        # review = Review.objects.get(id=review_id)
        review = self.get_object()
        
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')
        review_description = request.POST.get('review_description')

        # Validate the input data
        errors = {}
        if not rating or not rating.isdigit() or not (1 <= int(rating) <= 10):
            errors['rating'] = ['Rating must be an integer between 1 and 10.']

        if errors:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(errors, status=400)
            return self.form_invalid(None)

        review.rating = rating
        review.review = review_text
        review.review_description = review_description
        review.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"message": "Success"}, status=200)
        return redirect(self.get_success_url())
    
class DeleteReviewView(DeleteView):
    # A view to delete a review
    model = Review
    template_name = 'delete_review.html'
    context_object_name = 'review'
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'review_id'

class ProductListView(ListView):
    # A view to list all products
    model = Product
    template_name = 'list-products.html'
    context_object_name = 'products'
    def queryset(self):
        return Product.objects.all()