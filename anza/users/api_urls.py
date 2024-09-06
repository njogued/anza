from django.urls import path
from .views import APIUserListView, APIUserCreateView
from .models import CustomUser
from .serializer import UserSerializer
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('list/', APIUserListView.as_view(), name='user-list'),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
    path('create/', APIUserCreateView.as_view(), name='user-create'),
]