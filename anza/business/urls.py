from django.urls import path
from .views import (
    CreateBusinessView, 
    BusinessDetailView, 
    BusinessUpdateView, 
    BusinessDeleteView, 
    BusinessListView, 
    CreateProductView, 
    SearchView
)

urlpatterns = [
    path("create/", CreateBusinessView.as_view(), name="create_business"),
    path("<int:business_id>/update/", BusinessUpdateView.as_view(), name="update_business"),
    path("<int:business_id>/delete/", BusinessDeleteView.as_view(), name="delete_business"),
    path("all/", BusinessListView.as_view(), name="list_business"),
    path("search/", SearchView.as_view(), name="search_business"),
    path("<int:business_id>/", BusinessDetailView.as_view(), name="detail_business"),
    path("<int:business_id>/product/create/", CreateProductView.as_view(), name="detail_business")
]