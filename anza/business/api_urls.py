from django.urls import path
from .views import APIBusinessListView

urlpatterns = [
    path('list/', APIBusinessListView.as_view(), name='business-list'),
]