from django.urls import path
from .views import APIBusinessListView, APIBusinessDetailView, APIBusinessCreateView, APIBusinessUpdateView, APIBusinessDeleteView, APIBusinessProductsView, APIBusinessProductsCreateView

urlpatterns = [
    path('list/', APIBusinessListView.as_view(), name='business-list'),
    path('<int:business_id>/', APIBusinessDetailView.as_view(), name='business-detail'),
    path('create/', APIBusinessCreateView.as_view(), name='business-create'),
    path('update/<int:business_id>/', APIBusinessUpdateView.as_view(), name='business-update'),
    path('delete/<int:business_id>/', APIBusinessDeleteView.as_view(), name='business-delete'),
    path('<int:business_id>/products/', APIBusinessProductsView.as_view(), name='business-products'),
    path('<int:business_id>/products/create/', APIBusinessProductsCreateView.as_view(), name='business-product-create'),
]