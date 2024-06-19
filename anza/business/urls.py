from django.urls import path
from .views import CreateBusinessView, BusinessDetailView, BusinessUpdateView, BusinessDeleteView, BusinessListView

urlpatterns = [
    path("create/", CreateBusinessView.as_view(), name="create_business"),
    path("update/<int:business_id>/", BusinessUpdateView.as_view(), name="update_business"),
    path("delete/<int:business_id>/", BusinessDeleteView.as_view(), name="delete_business"),
    path("all/", BusinessListView.as_view(), name="list_business"),
    path("<int:business_id>/", BusinessDetailView.as_view(), name="detail_business"),
]