from django.shortcuts import render
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
