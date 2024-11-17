from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserUpdateForm
from .models import CustomUser
from django.http import Http404, JsonResponse, HttpResponse
from django.contrib.auth import views as auth_views
from .serializer import UserSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.mixins import LoginRequiredMixin

class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "sign-up.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"message": "Success"}, status=200)
            else:
                return redirect("login")
        else:
            errors = form.errors.get_json_data()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(errors, status=400, safe=False)
            else:
                return render(request, self.template_name, {"form": form})

class LoginView(auth_views.LoginView):
    # view to handle user login
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy("home")
    template_name = "sign-in.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"message": "Success"}, status=200)
        else:
            return redirect("home")
    
    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = form.errors.get_json_data()
            return JsonResponse(errors, status=400, safe=False)
        else:
            return super().form_invalid(form)
    
class UserDetailView(DetailView):
    model = CustomUser
    template_name = "user_details.html"
    context_object_name = 'user_profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    form_class = CustomUserUpdateForm
    def get_object(self, queryset=None):
        try:
            print(self.request)
            return { "user_profile": super().get_object(queryset), "form": CustomUserUpdateForm() }
        except CustomUser.DoesNotExist:
            raise Http404("User not found")
        
    def post(self, request, *args, **kwargs):
        user_profile = CustomUser.objects.get(email=self.request.user)
        form = self.form_class(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            # need headers to detect ajax request
            # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            #     return JsonResponse({"message": "Success"}, status=200)
            return JsonResponse({"message": "Success"}, status=200)
        else:
            errors = form.errors.get_json_data()
            print(errors)
            # need headers to detect ajax request
            # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            #     return JsonResponse(errors, status=400, safe=False)
            return JsonResponse(errors, status=400, safe=False)
        
class MyProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "user_profile.html"
    context_object_name = 'user_profile'
    login_url = '/users/login'
    form_class = CustomUserUpdateForm
    def get_object(self, queryset=None):
        try:
            user_profile = { "user_profile": CustomUser.objects.get(email=self.request.user), "form": CustomUserUpdateForm() }
            return user_profile
        except CustomUser.DoesNotExist:
            raise Http404("Profile not found")
        
    def post(self, request, *args, **kwargs):
        user_profile = CustomUser.objects.get(email=self.request.user)
        form = self.form_class(request.POST, request.FILES, instance=user_profile)
        print(request.headers.get('X-Requested-With'))
        if form.is_valid():
            form.save()
            return redirect("profile")
            # return JsonResponse({"message": "Success"}, status=200)
        else:
            errors = form.errors.get_json_data()
            print(errors)
            return JsonResponse(errors, status=400, safe=False)
    
class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = "password_reset.html"
    success_url = reverse_lazy("password_reset_done")

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "password_reset_done.html"


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "password_reset_confirm.html"
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        return super().form_valid(form)
    
class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "password_reset_complete.html"

class APIUserListView(generics.ListAPIView):
    # A view to list all users
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class APIUserCreateView(generics.CreateAPIView):
    # A view to create a user
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    