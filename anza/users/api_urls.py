from django.urls import path
from .views import UserListView
from .models import CustomUser
from .serializer import UserSerializer
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('list/', UserListView.as_view(), name='user-list'),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
]