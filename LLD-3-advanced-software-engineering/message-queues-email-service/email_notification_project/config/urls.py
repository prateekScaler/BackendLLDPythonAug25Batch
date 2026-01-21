"""
URL configuration for email_notification_project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def home(request):
    """Simple home endpoint with API documentation."""
    return JsonResponse({
        'message': 'Email Notification Service - Demo Project',
        'version': '1.0.0',
        'endpoints': {
            'POST /api/register/': 'Register a new user (sends welcome email)',
            'POST /api/password-reset/': 'Request password reset (sends reset email)',
            'POST /api/order-confirm/': 'Confirm an order (sends confirmation email)',
            'GET /api/health/': 'Health check endpoint',
        },
        'documentation': 'See docs/kafka-email-integration-guide.md for full documentation'
    })


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
]
