from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, views
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser
from django.http import Http404

class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "sign-up.html"

    def form_valid(self, form):
        # You can add additional logic here if needed
        return super().form_valid(form)

class LoginView(views.LoginView):
    form_class = CustomAuthenticationForm
    # success_url = reverse_lazy("login")
    template_name = "login.html"
    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
        return render(request, self.template_name, {"form": form})
    
class UserDetailView(DetailView):
    model = CustomUser
    template_name = "user_details.html"
    context_object_name = 'user_profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except CustomUser.DoesNotExist:
            raise Http404("User not found")
