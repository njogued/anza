from django.db import models
from users.models import CustomUser
# Create your models here.
    
class NotificationType(models.Model):
    # Model that represents a notification type
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Notification(models.Model):
    # Model that represents a notification
    notification_id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_notifications')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_notifications', default=None)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE, related_name='notifications', default=None)
    message = models.TextField()
    read = models.BooleanField(default=False)
    url = models.URLField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.recipient.username}, {self.message}"