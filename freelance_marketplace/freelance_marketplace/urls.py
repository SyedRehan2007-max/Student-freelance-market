"""
URL configuration for freelance_marketplace project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('marketplace.urls')),
]
