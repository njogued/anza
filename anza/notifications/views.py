from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View
from .models import Notification, NotificationType
from .forms import NotificationForm
import json
from django.http import JsonResponse
from users.models import CustomUser
# Create your views here.


class NotificationListView(ListView):
    # A view to display a list of notifications
    model = Notification
    template_name = "notifications.html"
    context_object_name = "notifications"
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_count'] = Notification.objects.filter(recipient=self.request.user, read=False).count()
        return context
    
class NotificationCreateView(CreateView):
    # A view to create a notification
    model = Notification
    form_class = NotificationForm
    template_name = "create_notification.html"
    success_url = "/activity/"
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        # Check if request is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = json.loads(request.body)
            recipient = data['recipient']    
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