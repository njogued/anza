from django.shortcuts import render
from .models import CustomUser, Product, Order, OrderItem, Cart, CartItem, Payment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Add items to cart
class AddToCartView(LoginRequiredMixin, View):
    # Add items to cart, creates one if it does not exist
    login_url = '/users/login'

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))
        product = get_object_or_404(Product, product_id=product_id)

        cart, created_cart = Cart.objects.get_or_create(user=request.user, archived=False)
        item, created_item = CartItem.object.get_or_create(cart=cart, product=product)
        if created_item:
            item.quantity = quantity
        else:
            item.quantity += quantity
        total_items_cost = item.calculate_price()
        cart.update_price_total(total_items_cost)
        return JsonResponse({"message": f"{quantity} of {product.name} added to cart"}, status=200)     

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
class UpdateCartView(LoginRequiredMixin, DeleteView):
    # A view to create a new cart in back-end
    login_url = '/users/login'
    model = CartItem

    def delete(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        product_removed = get_object_or_404(Product, product_id=product_id)
        cart = get_object_or_404(cart__user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product_removed)
        cart_item.delete()
        cart.save()        
        return JsonResponse({"message": "Product removed from cart successfully"}, status=200)

    
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        new_quantity = request.POST.get("quantity")
        product_to_update = get_object_or_404(Product, product_id=product_id)
        cart = get_object_or_404(cart__user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product_to_update)
        cart_item.quantity = new_quantity
        return JsonResponse({"message": "Product quantity in Cart updated"}, status=201)


# Create an order and notify seller