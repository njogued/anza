from django.urls import path
from .views import APIUserListView, APIUserCreateView
from .models import CustomUser
from .serializer import UserSerializer
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', APIUserListView.as_view(), name='api_user_list'),
    path('all/', APIUserListView.as_view(), name='api_user_list'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('create/', APIUserCreateView.as_view(), name='api_user_create'),
]