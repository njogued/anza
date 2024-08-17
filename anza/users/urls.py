from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .views import SignUpView, UserDetailView, LoginView, CustomPasswordResetView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset_confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password_reset_confirm/MQ/set-password/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("<str:username>/", UserDetailView.as_view(), name="details"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)