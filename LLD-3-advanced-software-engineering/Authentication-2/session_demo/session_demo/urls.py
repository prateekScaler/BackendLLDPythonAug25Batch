"""
URL Configuration for Session Demo
===================================

This file routes URLs to views.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin panel (optional - for viewing sessions in database)
    path('admin/', admin.site.urls),

    # Our demo app URLs
    path('', include('auth_app.urls')),
]
