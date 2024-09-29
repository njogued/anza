from django.urls import path
from .views import NotificationListView, SendNotificationView

urlpatterns = [
    path("", NotificationListView.as_view(), name="all_notifications"),
    path("send_urgent_notification", SendNotificationView.as_view(), name="send_urgent_notification"),
]