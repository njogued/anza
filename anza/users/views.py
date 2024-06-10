from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, views
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"

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
