from django.shortcuts import render
from .models import CustomUser, Product, Order, OrderItem, Cart, CartItem, Payment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.http import JsonResponse

# Create a cart
class CreateCartView(LoginRequiredMixin, CreateView):
    # A view to create a new cart in back-end
    model = Cart
    login_url = '/users/login'

    def post(self, request):
        existing_cart = Cart.objects.filter(user=request.user)
        if existing_cart:
            return existing_cart
        new_cart = Cart.objects.create(user=request.user)
        new_cart.save()
        return new_cart
    
# Delete a cart
class DeleteCartView(LoginRequiredMixin, DeleteView):
    # A view to delete a cart
    model = Cart
    login_url = '/users/login'

    def delete(self, request):
        existing_cart = Cart.objects.filter(user=request.user)
        if existing_cart:
            existing_cart.delete()
            return JsonResponse({"message": "Cart cleared"}, status=200)


# Update a cart


# Create an order


# Update an cart