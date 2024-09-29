from django.forms import ModelForm
from .models import Notification

class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = ['recipient', 'creator', 'notification_type', 'message', 'url', 'read']

