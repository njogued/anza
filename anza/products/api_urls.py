from django.urls import path
from .views import APIProductListView, APIProductDetailView

urlpatterns = [
    path("", APIProductListView.as_view(), name="products"),
    path("all/", APIProductListView.as_view(), name="products"),
    path("<int:pk>/", APIProductDetailView.as_view(), name="product"),
]