from django.urls import path
from .views import APIProductListView, APIProductDetailView, APIProductUpdateView

urlpatterns = [
    path("", APIProductListView.as_view(), name="products"),
    path("all/", APIProductListView.as_view(), name="products"),
    path("<int:product_id>/", APIProductDetailView.as_view(), name="product"),
    path("<int:product_id>/update/", APIProductUpdateView.as_view(), name="update_product"),
]