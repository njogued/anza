from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .views import SignUpView, UserDetailView, LoginView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name = "sign-in.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("<str:username>/", UserDetailView.as_view(), name="details"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)