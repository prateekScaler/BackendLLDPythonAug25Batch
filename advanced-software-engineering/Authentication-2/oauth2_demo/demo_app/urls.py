from django.urls import path
from . import views

urlpatterns = [
    # Demo UI
    path('', views.home, name='home'),

    # OAuth2 Provider Endpoints (simulating Google/GitHub)
    path('oauth/authorize/', views.provider_authorize, name='authorize'),
    path('oauth/login/', views.provider_login_submit, name='provider_login'),
    path('oauth/consent/', views.provider_consent_submit, name='provider_consent'),
    path('oauth/token/', views.provider_token, name='token'),
    path('oauth/userinfo/', views.provider_userinfo, name='userinfo'),
    path('oauth/revoke/', views.provider_revoke, name='revoke'),

    # Client Application Callback
    path('callback/', views.client_callback, name='callback'),

    # API endpoints for demo UI
    path('api/exchange/', views.api_exchange_code, name='api_exchange'),
    path('api/userinfo/', views.api_get_userinfo, name='api_userinfo'),
    path('api/refresh/', views.api_refresh_token, name='api_refresh'),
    path('api/revoke/', views.api_revoke_token, name='api_revoke'),
    path('api/reset/', views.api_reset, name='api_reset'),
    path('api/inspect/', views.api_inspect_store, name='api_inspect'),
]
