"""
URL configuration for users app.

This module defines all API endpoints for the email notification demo.
"""

from django.urls import path
from .views import (
    UserRegistrationView,
    PasswordResetView,
    OrderConfirmationView,
    PaymentReceiptView,
    ShippingUpdateView,
    HealthCheckView,
)

urlpatterns = [
    # User Account Endpoints
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),

    # E-commerce Endpoints
    path('order-confirm/', OrderConfirmationView.as_view(), name='order-confirm'),
    path('payment-receipt/', PaymentReceiptView.as_view(), name='payment-receipt'),
    path('shipping-update/', ShippingUpdateView.as_view(), name='shipping-update'),

    # Health Check
    path('health/', HealthCheckView.as_view(), name='health'),
]
