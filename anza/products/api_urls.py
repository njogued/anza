from django.urls import path
from .views import (
    APIProductListView, 
    APIProductDetailView, 
    APIProductUpdateView, 
    APIProductDeleteView,
    APIProductReviewListView,
    APIProductReviewCreateView,
    APIReviewUpdateView,
    APIReviewDeleteView
)

urlpatterns = [
    path("", APIProductListView.as_view(), name="products"),
    path("all/", APIProductListView.as_view(), name="api_products_list"),
    path("<int:product_id>/", APIProductDetailView.as_view(), name="api_products_list"),
    path("<int:product_id>/update/", APIProductUpdateView.as_view(), name="api_update_product"),
    path("<int:product_id>/delete/", APIProductDeleteView.as_view(), name="api_delete_product"),
    path("<int:product_id>/review/create/", APIProductReviewCreateView.as_view(), name="api_product_review_create"),
    path("<int:product_id>/reviews/", APIProductReviewListView.as_view(), name="api_product_review_list"),
    path("reviews/<int:review_id>/update/", APIReviewUpdateView.as_view(), name="api_review_update"),
    path("reviews/<int:review_id>/delete/", APIReviewDeleteView.as_view(), name="api_review_delete")
]