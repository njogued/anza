from django.contrib import admin
from .models import NotificationType, Notification

# Register your models here.

admin.site.register(NotificationType)
admin.site.register(Notification)