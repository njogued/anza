from django.urls import path
from .views import ProductDetailView, ProductUpdateView, ProductDeleteView, CreateReviewView, UpdateReviewView, DeleteReviewView, ProductListView

urlpatterns = [
    # path("create/", CreateProductView.as_view(), name="create_product"),
    path("update/<int:product_id>/", ProductUpdateView.as_view(), name="update_product"),
    path("delete/<int:product_id>/", ProductDeleteView.as_view(), name="delete_product"),
    path("<int:product_id>/", ProductDetailView.as_view(), name="detail_product"),
    path("<int:product_id>/review/create/", CreateReviewView.as_view(), name="create_review"),
    path("review/update/<int:review_id>/", UpdateReviewView.as_view(), name="update_review"),
    path("review/delete/<int:review_id>/", DeleteReviewView.as_view(), name="delete_review"),
    path("all/", ProductListView.as_view(), name="list_product"),
]