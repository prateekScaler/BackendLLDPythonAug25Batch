from django.urls import path
from . import views

urlpatterns = [
    # Main demo page
    path('', views.home, name='home'),

    # Authentication
    path('api/login/', views.login, name='login'),

    # Token operations
    path('api/verify/', views.verify_token, name='verify'),
    path('api/decode/', views.decode_token, name='decode'),

    # Educational demos
    path('api/tamper/', views.tamper_token, name='tamper'),
    path('api/signature/', views.explain_signature, name='signature'),
    path('api/revoke/', views.revoke_user_token, name='revoke'),
    path('api/expired/', views.create_expired_token, name='expired'),
    path('api/impersonate/', views.impersonation_demo, name='impersonate'),

    # Utility
    path('api/reset/', views.reset_demo, name='reset'),
]
