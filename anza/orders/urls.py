from django.urls import path
from .views import CreateCartView

urlpatterns = [
    path("create/", CreateCartView.as_view(), name="create_cart")
]