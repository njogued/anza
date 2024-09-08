from django.urls import path
from .views import APIBusinessListView, APIBusinessDetailView, APIBusinessCreateView, APIBusinessUpdateView, APIBusinessDeleteView, APIBusinessProductsView, APIBusinessProductsCreateView

urlpatterns = [
    path('', APIBusinessListView.as_view(), name='api_business_list'),
    path('all/', APIBusinessListView.as_view(), name='api_business_list'),
    path('<int:business_id>/', APIBusinessDetailView.as_view(), name='api_business_detail'),
    path('create/', APIBusinessCreateView.as_view(), name='api_business_create'),
    path('<int:business_id>/update/', APIBusinessUpdateView.as_view(), name='api_business_update'),
    path('<int:business_id>/delete/', APIBusinessDeleteView.as_view(), name='api_business_delete'),
    path('<int:business_id>/products/', APIBusinessProductsView.as_view(), name='api_business_products'),
    path('<int:business_id>/products/create/', APIBusinessProductsCreateView.as_view(), name='api_product_create'),
]