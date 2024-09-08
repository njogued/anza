from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views import View
from .models import Product, Review, ProductImage
from .forms import UpdateProductForm, CreateReviewForm, UpdateReviewForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseForbidden, JsonResponse
from notifications.models import create_notification
from rest_framework import generics
from .serializer import ProductSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

class ProductDetailView(View):
    # A view to display the details of a product
    form_class = CreateReviewForm

    def get(self, request, product_id):
        product = Product.objects.get(product_id=product_id)
        images = ProductImage.objects.filter(product=product)
        reviews = Review.objects.filter(product=product)
        self_review_bool = False
        self_review = None
        product_owner = product.business.owner
        if request.user.is_authenticated:
            self_review = reviews.filter(reviewer=request.user).first()
            if self_review:
                self.form_class = UpdateReviewForm
                self_review_bool = True
        rev_count = reviews.count()
        context = {"product": product, "images": images, "reviews": reviews, "rev_count": rev_count, "form": self.form_class, "self_review": self_review, "self_review_bool": self_review_bool, "product_owner": product_owner}

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
            # modify rating and review in business
            business = product.business
            business.total_rating_int += int(review.rating)
            business.reviews += 1
            business.rating = business.total_rating_int / business.reviews
            business.save()
            success_url = reverse('detail_product', kwargs={'product_id': product.product_id})
            # create notification
            # to fix: use celery to create a notif async and send back response
            create_notification(
                creator=request.user,
                recipient=product.business.owner,
                notification_type_name="New Review",
                message=f"New Review for your product {product.name}",
                url=success_url
            )
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

        # Update the rating in business model
        old_rating = review.rating
        business = review.product.business
        business.total_rating_int += int(rating) - old_rating
        business.rating = business.total_rating_int / business.reviews
        business.save()
        # Update rating in rating model
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
    pk_url_kwarg = 'review_id'
    product_id = None
    
    def post(self, request, review_id):
        review = self.get_object()
        self.product_id = review.product.product_id
        success_url = reverse('detail_product', kwargs={'product_id': self.product_id})
        # update the rating in business model
        business = review.product.business
        business.total_rating_int -= review.rating
        business.reviews -= 1
        if business.reviews > 0:
            business.rating = business.total_rating_int / business.reviews
        else:
            business.rating = 0
        review.delete()
        return redirect(success_url)

    # def post(self, request, review_id):
    #     review = self.get_object()
    #     review.archived = True
    #     review.save()
    #     return redirect(reverse('detail_product', kwargs={'product_id': review.product.product_id}))

    
    # def get_success_url(self):
    #     reverse_lazy('detail_product', kwargs={'product_id': self.product_id})
    

class ProductListView(ListView):
    # A view to list all products
    model = Product
    template_name = 'list-products.html'
    context_object_name = 'products'
    def queryset(self):
        return Product.objects.all()
    
class APIProductListView(generics.ListAPIView):
    # A view to list all products
    queryset = Product.objects.filter(archived=False).order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class APIProductDetailView(generics.RetrieveAPIView):
    # A view to display the details of one product
    lookup_field = 'product_id'
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs.get(self.lookup_field)
        product = Product.objects.filter(product_id=product_id)
        if product.exists():
            return product
        raise NotFound ({"message": "Product not found"})
    
class APIProductUpdateView(generics.RetrieveUpdateAPIView):
    # A view to update a product
    lookup_field = 'product_id'
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs.get(self.lookup_field)
        product = Product.objects.filter(product_id=product_id)
        if product.exists():
            return product
        raise NotFound ({"message": "Product not found"})
    
class APIProductDeleteView(generics.DestroyAPIView):
    # A view to delete a product
    lookup_field = 'product_id'
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs.get(self.lookup_field)
        product = Product.objects.filter(product_id=product_id)
        if product.exists():
            return product
        raise NotFound ({"message": "Product not found"})
    
    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.business.owner != request.user:
            return Response({"message": "You are not allowed to delete this product"}, status=403)
        product.make_delete()
        return JsonResponse({"message": "Product deleted"}, status=200)

class APIProductReviewCreateView(generics.CreateAPIView):
    # A view to create a review for a product given product id in url
    lookup_field = 'product_id'
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, request, *args, **kwargs):
        product_id = self.kwargs.get(self.lookup_field)
        product = Product.objects.get(product_id=product_id)
        business = product.business
        if business.owner == request.user or product.archived:
            return Response({"message": "You are not allowed to review this product. You either own it or it's deleted."}, status=403)
        review = Review.objects.create(
            product=product,
            reviewer=request.user,
            **request.data
        )
        # modify rating and review in business
        business.total_rating_int += int(review.rating)
        business.reviews += 1
        business.rating = business.total_rating_int / business.reviews
        business.save()
        return review
    
class APIReviewUpdateView(generics.RetrieveUpdateAPIView):
    # A view to update a review
    lookup_field = 'review_id'
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        review_id = self.kwargs.get(self.lookup_field)
        review = Review.objects.filter(id=review_id)
        if review.exists():
            return review
        raise NotFound ({"message": "Review not found"})
    
    def update(self, request, *args, **kwargs):
        review = self.get_object()
        rating = request.data.get('rating')
        review_text = request.data.get('review')
        review_description = request.data.get('review_description')

        # Validate the input data
        errors = {}
        if not rating or not rating.isdigit() or not (1 <= int(rating) <= 10):
            errors['rating'] = ['Rating must be an integer between 1 and 10.']

        if errors:
            return Response(errors, status=400)

        # Update the rating in business model
        old_rating = review.rating
        business = review.product.business
        business.total_rating_int += int(rating) - old_rating
        business.rating = business.total_rating_int / business.reviews
        business.save()
        # Update rating in rating model
        for k, v in request.data.items():
            if k in ["rating", "review", "review_description"]:
                setattr(review, k, v)
        review.save()
        return Response({"message": "Success"}, status=200)
    
class APIReviewDeleteView(generics.DestroyAPIView):
    # A view to delete a review
    lookup_field = 'review_id'
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        review_id = self.kwargs.get(self.lookup_field)
        review = Review.objects.filter(id=review_id)
        if review.exists():
            return review
        raise NotFound ({"message": "Review not found"})
    
    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        product = review.product
        business = product.business
        business.total_rating_int -= review.rating
        business.reviews -= 1
        if business.reviews > 0:
            # avoid ZeroDivisionError
            business.rating = business.total_rating_int / business.reviews
        else:
            business.rating = 0
        review.make_delete()
        return JsonResponse({"message": "Review deleted"}, status=200)


class APIProductReviewListView(generics.ListAPIView):
    # A view to list all reviews for a product
    queryset = Review.objects.filter(archived=False).order_by('-rating')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
