from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import Business
from .forms import CreateBusinessForm
from django.urls import reverse_lazy

# Create your views here.
class CreateBusinessView(LoginRequiredMixin, CreateView):
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})
    def post(self, request):
        curr_user = request.user
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = curr_user
            business.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form})
    model = Business
    form_class = CreateBusinessForm
    success_url = reverse_lazy("home")
    template_name = "create_business.html"
    login_url = "/users/login"

class BusinessDetailView(CreateView):
    model = Business
    template_name = "detail_business.html"

class BusinessUpdateView(CreateView):
    model = Business
    form_class = CreateBusinessForm
    template_name = "update_business.html"
    success_url = reverse_lazy("home")

class BusinessDeleteView(CreateView):
    model = Business
    template_name = "delete_business.html"
    success_url = reverse_lazy("home")