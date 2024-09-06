from django.urls import path
from .views import APIProductListView, APIProductDetailView

urlpatterns = [
    path("list/", APIProductListView.as_view(), name="products"),
    path("<int:pk>/", APIProductDetailView.as_view(), name="product"),
]