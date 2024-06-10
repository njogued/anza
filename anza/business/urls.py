from django.urls import path
from .views import CreateBusinessView, BusinessDetailView, BusinessUpdateView, BusinessDeleteView

urlpatterns = [
    path("create/", CreateBusinessView.as_view(), name="create_business"),
    path("update/<int:pk>/", BusinessUpdateView.as_view(), name="update_business"),
    path("delete/<int:pk>/", BusinessDeleteView.as_view(), name="delete_business"),
    path("<int:pk>/", BusinessDetailView.as_view(), name="detail_business"),

]