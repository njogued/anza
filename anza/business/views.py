import json
from django.core.serializers import serialize
from django.urls import reverse
from django.views import View
from django.urls import reverse_lazy
from django.db.models import Avg, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Business, Category
from .forms import CreateBusinessForm, BusinessUpdateForm
from products.models import Product, ProductImage, Review
from products.forms import CreateProductForm, ProductImageForm
from users.models import CustomUser
from users.consumers import send_user_notification
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializer import BusinessSerializer
from products.serializer import ProductSerializer
from rest_framework.exceptions import NotFound
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

# Create your views here.
class CreateBusinessView(LoginRequiredMixin, CreateView):
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})
    def post(self, request):
        curr_user = request.user
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = curr_user
            business.save()
            success_url = reverse('detail_business', kwargs={'business_id': business.business_id})
            return redirect(success_url)
        return render(request, self.template_name, {"form": form})
    model = Business
    form_class = CreateBusinessForm
    success_url = reverse_lazy("home")
    template_name = "create_business.html"
    login_url = "/users/login"

class BusinessDetailView(DetailView):
    model = Business
    template_name = "detail-businesses.html"
    context_object_name = "business"
    pk_url_kwarg = 'business_id'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.archived:
            obj = None
        return obj
    
    def get_context_data(self, **kwargs):
        # Get the existing context data from the parent class
        context = super().get_context_data(**kwargs)
        business = self.object
        # If the business object is None, add a flag to the context
        if self.object is None:
            context['business_deleted'] = True
        else:
            context['business_deleted'] = False
            products = business.products.all()
            num_products = products.count()
            reviews = Review.objects.filter(product__in=products)
            rating_info = reviews.aggregate(
                avg_rating=Avg('rating'),
                num_reviews=Count('id')
            )
            avg_rating = rating_info['avg_rating'] or 0
            num_reviews = rating_info['num_reviews'] or 0
            context['num_products'] = num_products
            context['num_reviews'] = num_reviews
            context['avg_rating'] = avg_rating
            context['reviews'] = reviews
            context['products'] = products
            print(business.owner)
            print(self.request.user)
            info = {
                "user": business.owner.id,
                "message": f"new business page visit for {business.name}"
            }
            send_user_notification(info)
        return context
    
    def render_to_response(self, context, **response_kwargs):
        # Check the flag in the context to see if the business is deleted
        if context.get('business_deleted'):
            return HttpResponse("Business deleted")
        # If not archived, call the parent class's render_to_response method
        return super().render_to_response(context, **response_kwargs)

class BusinessListView(ListView):
    model = Business
    template_name = "list-businesses.html"
    context_object_name = "businesses"
    # paginate_by = 10
    # ordering = ['name']
    def get_queryset(self):
        return Business.objects.filter(archived=False)

class BusinessUpdateView(UpdateView):
    model = Business
    form_class = BusinessUpdateForm
    template_name = "update_business.html"
    context_object_name = 'business'
    pk_url_kwarg = 'business_id'

    def get_success_url(self):
        return reverse_lazy('detail_business', kwargs={'business_id': self.object.business_id})
    
    def dispatch(self, request, *args, **kwargs):
        business = self.get_object()
        if business.owner != self.request.user:
            return HttpResponseForbidden("You are not allowed to update business")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        business = form.save()
        business.save()
        return redirect(self.get_success_url())


class BusinessDeleteView(View):
    template_name = "delete_business.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = 'business_id'
    
    def dispatch(self, request, *args, **kwargs):
        business_id = kwargs.get(self.pk_url_kwarg)
        business = get_object_or_404(Business, pk=business_id)
        if business.owner != request.user:
            return HttpResponseForbidden("You are not allowed to delete this business")
        self.business = business
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'business': self.business})

    def post(self, request, *args, **kwargs):
        business_id = kwargs.get(self.pk_url_kwarg)
        business = get_object_or_404(Business, pk=business_id)
        business.archived = True
        business.save()
        return redirect(self.success_url)
    
class CreateProductView(LoginRequiredMixin, CreateView):
    def get(self, request, business_id):
        # Provide the user with a form to create a new product
        product_form = self.form_class()
        image_form = ProductImageForm()
        return render(request, self.template_name, {"product_form": product_form, "image_form": image_form})
    
    def post(self, request, business_id):
        # Handle the form submission
        curr_user = request.user
        business_id = self.kwargs.get('business_id')
        business = Business.objects.get(business_id=business_id)
        product_form = self.form_class(request.POST, request.FILES)
        if business.owner != curr_user:
            return HttpResponseForbidden("You are not allowed to create product for this business")
        if product_form.is_valid():
            product = product_form.save(commit=False)
            images = request.FILES.getlist('image')
            product.business = business
            product.save()
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            success_url = reverse('detail_product', kwargs={'product_id': product.product_id})
            return redirect(success_url)
        return render(request, self.template_name, {"product_form": product_form, "image_form": ProductImageForm()})
    model = Product
    form_class = CreateProductForm
    success_url = reverse_lazy("home")
    template_name = "create_product.html"
    login_url = "/users/login"
    pk_url_kwarg = 'business_id'

class SearchView(ListView):
    def get(self, request):
        query = request.GET.get('query')
        curr_user = request.user
        # Use curr user to filter the search results and record as an action
        return self.get_queryset(query)

    def get_queryset(self, query):
        businesses = Business.objects.filter(name__icontains=query).order_by('-rating')
        products = Product.objects.filter(name__icontains=query).annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
        users = CustomUser.objects.filter(username__icontains=query).order_by('created_at')
        businesses = serialize('json', businesses)
        products = serialize('json', products)
        users = serialize('json', users)
        try:
            context = {
                "businesses": businesses,
                "products": products,
                "users": users,
                "message": "Success"
            }
            return JsonResponse(context, status=200, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"message": "Failed to fetch"}, status=200)
    
    def post(self, request):
        curr_user = request.user
        query = request.POST.get('query')
        # Use curr user to filter the search results and record as an action
        return self.get_queryset(query)
    
class APIBusinessListView(generics.ListAPIView):
    # return a list of businesses
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

class APIBusinessDetailView(generics.RetrieveAPIView):
    # return a single business
    lookup_field = 'business_id'
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Dynamically filter using the business_id from the URL
        business_id = self.kwargs.get(self.lookup_field)
        return Business.objects.filter(archived=False, business_id=business_id)
    
class APIBusinessCreateView(generics.CreateAPIView):
    # create a new business
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Dynamically set the owner based on the current user
        serializer.save(owner=self.request.user)


class APIBusinessUpdateView(generics.UpdateAPIView):
    # update a business
    lookup_field = 'business_id'
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Dynamically filter using the business_id from the URL
        business_id = self.kwargs.get(self.lookup_field)
        return Business.objects.filter(archived=False, business_id=business_id)
    
    def put(self, request, *args, **kwargs):
        # Dynamically set the owner based on the current user
        business = self.get_object()
        if business.owner != request.user:
            return HttpResponseForbidden("You are not allowed to update this business")
        return self.partial_update(request, *args, **kwargs)
    
class APIBusinessDeleteView(generics.DestroyAPIView):
    # delete a business
    lookup_field = 'business_id'
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Dynamically filter using the business_id from the URL
        business_id = self.kwargs.get(self.lookup_field)
        return Business.objects.filter(archived=False, business_id=business_id)
    
    def destroy(self, request, *args, **kwargs):
        # Dynamically set the archived flag to True
        instance = self.get_object()
        instance.archived = True
        instance.save()
        return JsonResponse({"message": "Success"}, status=200)
    
    def post(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class APIBusinessProductsView(generics.ListAPIView):
    # return a list of products for a business
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Dynamically filter using the business_id from the URL
        business_id = self.kwargs.get('business_id')
        try:
            business = Business.objects.get(business_id=business_id)
            return Product.objects.filter(business__business_id=business_id)
        except Business.DoesNotExist:
            raise NotFound({"message": "Business not found"})
        
class APIBusinessProductsCreateView(generics.CreateAPIView):
    # create a new product for a business
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def perform_create(self, serializer):
        # Dynamically set the business based on the URL
        business_id = self.kwargs.get('business_id')
        business = Business.objects.get(business_id=business_id)
        serializer.save(business=business)