from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View
from .models import Notification, NotificationType, create_notification
from .forms import NotificationForm
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from users.models import CustomUser
from users.consumers import send_user_notification
# Create your views here.


class NotificationListView(ListView):
    # A view to display a list of notifications
    model = Notification
    template_name = "notifications.html"
    context_object_name = "notifications"
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = Notification.objects.filter(recipient=self.request.user)
        queryset.filter(read=False).update(read=True)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_count'] = Notification.objects.filter(recipient=self.request.user, read=False).count()
        return context
    
class NotificationCreateView(CreateView):
    # A view to create a notification
    model = Notification
    success_url = "/notifications/"
    form_class = NotificationForm

    def post(self, request):
        # Check if request is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = json.loads(request.body)
            form = self.form_class(data)
            if form.is_valid():
                notification = form.save(commit=False)
                notification.creator = request.user
                notification.save()
                return JsonResponse({"status": "success", "message": "Notification sent successfully"})
            else:
                return JsonResponse({"status": "error", "message": "Error sending notification"})
            
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                notification = form.save(commit=False)
                notification.creator = request.user
                notification.save()
                return redirect(self.success_url)
            else:
                return render(request, self.template_name, {"form": form})
            
class SendNotificationView(LoginRequiredMixin, View):
    login_url = "/users/login"

    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = json.loads(request.body)
            new_notification = create_notification(data.creator, data.recipient, data.notification_type_name, data.message)
            return new_notification
        else:
            data = request.POST
            new_notification = create_notification(data['creator'], data['recipient'], data['notification_type_name'], data['message'])
            return new_notification