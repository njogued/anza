from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    SignUpView,
    UserDetailView, 
    LoginView, 
    TestView, 
    CustomPasswordResetView, 
    CustomPasswordResetDoneView, 
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password_reset_complete/", CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("test/", TestView.as_view(), name="test"),
    path("<str:username>/", UserDetailView.as_view(), name="details"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)