from django.db import models
from users.models import CustomUser
from users.consumers import send_user_notification
# Create your models here.
    
class NotificationType(models.Model):
    # Model that represents a notification type
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    urgency = models.CharField(max_length=50, choices=[('now', 'Now'), ('best_time', 'BestTime'), ('later', 'Later'), ('never', 'Never')], default='never')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Notification(models.Model):
    # Model that represents a notification
    # A notification is not only constrained to actions that a user is notified of
    # Instead, it is a broad term that also includes user activity that the user will not get notified of yet
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
    
def create_notification(creator, recipient, notification_type_name, message, url=None):
    # Get or create notification type
    notification_type, _ = NotificationType.objects.get_or_create(
        name=notification_type_name,
        defaults={'description': f'{notification_type_name} Notification'}
    )



    notification = Notification.objects.create(
        creator=creator,
        recipient=recipient,
        notification_type=notification_type,
        message=message,
        url=url,
        read=False
    )
    notification.save()

    if notification_type.urgency == 'now':
        info = {
                "user": recipient.id,
                "message": message
        }
        send_user_notification(info)
    else:
        pass

    return
