"""
URL configuration for anza project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from users.views import MyProfileView
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include('users.urls')), 
    path("business/", include('business.urls')),
    path("products/", include('products.urls')),
    path("order/", include('orders.urls')),
    path("notifications/", include('notifications.urls')),
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("contact/", TemplateView.as_view(template_name="contact.html"), name="contact"),
    path("api/users/", include('users.api_urls')),
    path("api/business/", include('business.api_urls')),
    path("api/products/", include('products.api_urls')),
    path("profile/", MyProfileView.as_view(template_name="user_profile.html"), name="profile"),
    # path("research/", ResearchView.as_view(), name="research"),
    # path("refer/<int:pk>", ReferView.as_view(), name="refer"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
