from django.urls import path
from .views import AddToCartView, DeleteCartView, UpdateCartView, CreateOrderView

urlpatterns = [
    path("add_to_cart/", AddToCartView.as_view(), name="add_to_cart"),
    path("delete_cart/", DeleteCartView.as_view(), name="delete_cart"),
    path("update_cart/", UpdateCartView.as_view(), name="update_cart"),
    path("buy/", CreateOrderView.as_view(), name="create_order"),
]