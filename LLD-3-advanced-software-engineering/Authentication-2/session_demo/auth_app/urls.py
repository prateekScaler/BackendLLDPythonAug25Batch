"""
URL Configuration for Auth Demo App
====================================

All endpoints for the session-based authentication demo.
"""

from django.urls import path
from . import views

urlpatterns = [
    # ==========================================================================
    # PAGES
    # ==========================================================================

    # Home page with demo dashboard
    path('', views.home, name='home'),

    # CORS test page (simulates different origin)
    path('cors-test/', views.cors_test_page, name='cors_test'),


    # ==========================================================================
    # AUTHENTICATION APIs
    # ==========================================================================

    # Login - creates session
    # POST /api/login/  {"username": "testuser", "password": "testpass123"}
    path('api/login/', views.login_view, name='login'),

    # Logout - destroys session
    # POST /api/logout/
    path('api/logout/', views.logout_view, name='logout'),

    # Create test user (run once to set up)
    # POST /api/create-user/
    path('api/create-user/', views.create_test_user, name='create_user'),


    # ==========================================================================
    # SESSION & COOKIE APIs
    # ==========================================================================

    # Get current session info
    # GET /api/session/
    path('api/session/', views.session_info, name='session_info'),

    # Set data in session
    # POST /api/session/set/  {"key": "name", "value": "John"}
    path('api/session/set/', views.set_session_data, name='set_session_data'),

    # Get all session data
    # GET /api/session/data/
    path('api/session/data/', views.get_session_data, name='get_session_data'),

    # Set a custom cookie (with configurable attributes)
    # GET /api/cookie/set/?httponly=true&secure=false&samesite=Lax&max_age=3600
    path('api/cookie/set/', views.set_custom_cookie, name='set_custom_cookie'),

    # Delete a custom cookie
    # GET /api/cookie/delete/?name=demo_cookie
    path('api/cookie/delete/', views.delete_custom_cookie, name='delete_custom_cookie'),


    # ==========================================================================
    # DEMO APIs
    # ==========================================================================

    # Protected resource (requires authentication)
    # GET /api/protected/
    path('api/protected/', views.protected_resource, name='protected_resource'),

    # CORS demo endpoint
    # GET /api/cors/
    path('api/cors/', views.cors_demo, name='cors_demo'),

    # Show all request headers
    # GET /api/headers/
    path('api/headers/', views.headers_info, name='headers_info'),
]
