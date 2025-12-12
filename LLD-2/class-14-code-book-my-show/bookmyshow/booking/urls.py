"""
URL Configuration for BookMyShow API

Interview Points:
1. RESTful URL design
2. ViewSet routing with DefaultRouter
3. Function-based view routing
4. API versioning (optional but good practice)
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Interview Note: DefaultRouter automatically creates routes for ViewSets
# Generates: list, create, retrieve, update, partial_update, destroy
router = DefaultRouter()

# Register ViewSets
# Interview Note: basename is auto-generated from queryset if not provided
router.register(r'cities', views.CityViewSet, basename='city')
router.register(r'theaters', views.TheaterViewSet, basename='theater')
router.register(r'movies', views.MovieViewSet, basename='movie')
router.register(r'shows', views.ShowViewSet, basename='show')
router.register(r'tickets', views.TicketViewSet, basename='ticket')

# URL patterns
urlpatterns = [
    # ViewSet routes - Interview Note: Includes all CRUD + custom actions
    # /api/cities/ - GET (list)
    # /api/cities/{id}/ - GET (retrieve)
    # /api/movies/search/ - GET (custom action)
    # /api/shows/{id}/available_seats/ - GET (custom action)
    # etc.
    path('', include(router.urls)),

    # Function-based view routes - Interview Note: Manual routing
    path('book/', views.book_tickets, name='book-tickets'),
    path('tickets/<str:ticket_id>/confirm-payment/', views.confirm_payment, name='confirm-payment'),
    path('register/', views.register_user, name='register'),
    path('validate-coupon/', views.validate_coupon, name='validate-coupon'),
    path('health/', views.health_check, name='health-check'),

    # DRF built-in auth views (for browsable API)
    path('auth/', include('rest_framework.urls')),
]


"""
GENERATED ROUTES FROM VIEWSETS:

Cities:
- GET    /api/cities/                    - List all cities
- GET    /api/cities/{id}/               - Get city details

Theaters:
- GET    /api/theaters/                  - List theaters (filterable by city)
- GET    /api/theaters/{id}/             - Get theater details

Movies:
- GET    /api/movies/                    - List movies
- GET    /api/movies/{id}/               - Get movie details
- GET    /api/movies/search/             - Search movies (custom action)
- GET    /api/movies/{id}/shows/         - Get shows for movie (custom action)

Shows:
- GET    /api/shows/                     - List shows
- GET    /api/shows/{id}/                - Get show details with seats
- GET    /api/shows/{id}/available_seats/ - Get available seats (custom action)

Tickets:
- GET    /api/tickets/                   - List user's tickets
- GET    /api/tickets/{id}/              - Get ticket details
- POST   /api/tickets/{id}/cancel/       - Cancel ticket (custom action)

Custom Endpoints:
- POST   /api/book/                      - Book tickets
- POST   /api/tickets/{id}/confirm-payment/ - Confirm payment
- POST   /api/register/                  - Register user
- POST   /api/validate-coupon/           - Validate coupon
- GET    /api/health/                    - Health check

Interview Questions:

Q: Why use router for ViewSets but manual paths for function-based views?
A: Router automatically generates standard REST routes. Function-based views
   need manual routing for custom endpoints.

Q: What's the difference between /api/tickets/{id}/ and /api/book/?
A: First is RESTful resource endpoint (ViewSet), second is RPC-style
   custom action (function-based view for complex operation).

Q: How to version APIs?
A: Multiple approaches:
   1. URL: /api/v1/movies/, /api/v2/movies/
   2. Header: Accept: application/vnd.bookmyshow.v1+json
   3. Query param: /api/movies/?version=1 (not recommended)

Q: Should POST /api/book/ be POST /api/tickets/ instead?
A: Both valid! /api/tickets/ is more RESTful (creating ticket resource).
   /api/book/ is more RPC-style (performing booking action).
   Choose based on team preference and API design philosophy.
"""
