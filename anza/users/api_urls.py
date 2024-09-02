from django.urls import path
from .views import UserListView
from .models import CustomUser
from .serializer import UserSerializer

urlpatterns = [
    path('list/', UserListView.as_view(), name='user-list'),
]