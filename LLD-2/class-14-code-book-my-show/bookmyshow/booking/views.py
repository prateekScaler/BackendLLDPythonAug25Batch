"""
BookMyShow Views (Controllers in MVC)

Interview Points:
1. Views = Controllers in Django (Django uses MVT, not MVC)
2. Thin views, fat services (business logic in services)
3. Views handle HTTP request/response only
4. Different view types: APIView, ViewSet, function-based

Mapping to MVC:
- Model: Django Models (ORM)
- View: Django Templates (we don't use - REST API only)
- Controller: Django Views (this file!)
- Service: Custom service layer (our addition)

Flow:
Request -> URLs -> View -> Serializer -> Service -> Model -> DB
"""
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import (
    City, Theater, Movie, Show, ShowSeat, Ticket, User
)
from .serializers import (
    CitySerializer, TheaterSerializer, TheaterListSerializer,
    MovieSerializer, ShowSerializer, ShowDetailSerializer,
    ShowSeatSerializer, TicketSerializer, TicketListSerializer,
    BookingRequestSerializer, UserSerializer, UserCreateSerializer,
    CouponValidationSerializer
)
from .services.booking_service_pessimistic import BookingServicePessimistic
from .services.movie_service import MovieService


# ============= Configuration =============

# You can switch between different booking service implementations here!
# Interview Note: Dependency injection pattern
BookingService = BookingServicePessimistic

# Uncomment to use different implementations:
# from .services.booking_service_optimistic import BookingServiceOptimistic
# BookingService = BookingServiceOptimistic

# from .services.booking_service_thread import BookingServiceThread
# BookingService = BookingServiceThread


# ============= ViewSets =============

class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for City (Read-Only)

    Interview Note: ReadOnlyModelViewSet provides list() and retrieve() only
    Users can't create/update/delete cities via API
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

    # Interview Note: Override queryset for optimization
    def get_queryset(self):
        """
        Optimize query with annotations

        Interview Tip: Use select_related/prefetch_related to avoid N+1 queries
        """
        return City.objects.all().order_by('name')


class TheaterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Theater

    Interview Note: Different serializers for list vs detail
    """
    queryset = Theater.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city']
    search_fields = ['name', 'address']

    def get_serializer_class(self):
        """
        Use different serializer based on action

        Interview Tip: Optimize by using lighter serializer for list views
        """
        if self.action == 'list':
            return TheaterListSerializer
        return TheaterSerializer

    def get_queryset(self):
        """Optimize query"""
        queryset = Theater.objects.select_related('city')

        if self.action == 'list':
            # Add annotation for list view
            from django.db.models import Count
            queryset = queryset.annotate(screen_count=Count('screens'))

        return queryset.order_by('city__name', 'name')


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Movie with search functionality

    Interview Note: Custom actions with @action decorator
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Custom search endpoint with advanced filters

        Interview Note: @action creates custom endpoint
        URL: /api/movies/search/?query=avengers&city=mumbai

        This demonstrates service layer usage
        """
        query = request.query_params.get('query', '')
        city_id = request.query_params.get('city')
        category = request.query_params.get('category')
        language = request.query_params.get('language')
        min_rating = request.query_params.get('min_rating')

        # Call service layer - Interview Note: Business logic in service
        movies = MovieService.search_movies(
            query=query,
            city_id=city_id,
            category=category,
            language=language,
            min_rating=float(min_rating) if min_rating else None
        )

        # Paginate results
        page = self.paginate_queryset(movies)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def shows(self, request, pk=None):
        """
        Get shows for a movie

        Interview Note: detail=True means requires movie ID
        URL: /api/movies/{id}/shows/?city=mumbai&date=2024-01-01
        """
        movie = self.get_object()
        city_id = request.query_params.get('city')
        date_str = request.query_params.get('date')

        date = None
        if date_str:
            from datetime import datetime
            date = datetime.strptime(date_str, '%Y-%m-%d').date()

        shows = MovieService.get_movie_shows(
            movie_id=movie.id,
            city_id=city_id,
            date=date
        )

        serializer = ShowSerializer(shows, many=True)
        return Response(serializer.data)


class ShowViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Show

    Interview Note: Different serializers for list vs detail (with seats)
    """
    queryset = Show.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie', 'theater', 'language']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ShowDetailSerializer
        return ShowSerializer

    def get_queryset(self):
        """
        Optimize with select_related

        Interview Note: Prevent N+1 query problem
        """
        queryset = Show.objects.select_related(
            'movie', 'theater', 'theater__city', 'screen'
        )

        if self.action == 'retrieve':
            # Prefetch show seats for detail view
            queryset = queryset.prefetch_related(
                'show_seats',
                'show_seats__seat'
            )

        return queryset.order_by('start_time')

    @action(detail=True, methods=['get'])
    def available_seats(self, request, pk=None):
        """
        Get available seats for a show

        Interview Note: Custom action for specific business logic
        URL: /api/shows/{id}/available_seats/
        """
        show = self.get_object()
        seats = BookingService.get_available_seats(show.id)
        serializer = ShowSeatSerializer(seats, many=True)
        return Response(serializer.data)


class TicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Ticket with booking functionality

    Interview Note: ModelViewSet provides full CRUD
    But we override create/update with custom logic
    """
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        User can only see their own tickets

        Interview Note: Filter by current user
        """
        return Ticket.objects.filter(
            user=self.request.user
        ).select_related(
            'show', 'show__movie', 'show__theater', 'show__screen', 'payment'
        ).prefetch_related(
            'ticket_seats', 'ticket_seats__show_seat', 'ticket_seats__show_seat__seat'
        ).order_by('-booking_time')

    def get_serializer_class(self):
        """Different serializer for list"""
        if self.action == 'list':
            return TicketListSerializer
        return TicketSerializer

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel a ticket

        Interview Note: POST for non-idempotent operations
        URL: /api/tickets/{id}/cancel/
        """
        ticket = self.get_object()

        try:
            # Call service layer
            cancelled_ticket = BookingService().cancel_booking(
                ticket_id=ticket.id,
                user=request.user
            )

            serializer = self.get_serializer(cancelled_ticket)
            return Response(serializer.data)

        except (ValueError, PermissionError) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# ============= Function-Based Views =============

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_tickets(request):
    """
    Book tickets endpoint

    Interview Note: Function-based view for complex custom logic
    Could also be a ViewSet action, but this is simpler for one-off endpoints

    Flow:
    1. Validate request data with serializer
    2. Call service layer
    3. Return response

    This is the MOST IMPORTANT endpoint - demonstrates entire flow!
    """
    # Step 1: Validate request
    serializer = BookingRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    validated_data = serializer.validated_data

    try:
        # Step 2: Call service layer (business logic)
        # Interview Note: This is where concurrency control happens!
        result = BookingService().book_tickets(
            user=request.user,
            show_id=validated_data['show_id'],
            seat_ids=validated_data['seat_ids'],
            payment_mode=validated_data['payment_mode'],
            coupon_code=validated_data.get('coupon_code')
        )

        # Step 3: Return response
        ticket_serializer = TicketSerializer(result['ticket'])
        return Response({
            'ticket': ticket_serializer.data,
            'payment_id': result['payment'].id,
            'total_amount': result['total_amount'],
            'discount': result['discount'],
            'message': 'Booking successful! Please complete payment.'
        }, status=status.HTTP_201_CREATED)

    except ValueError as e:
        # Business logic errors (validation, availability, etc.)
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        # Unexpected errors
        return Response(
            {'error': 'Booking failed. Please try again.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_payment(request, ticket_id):
    """
    Confirm payment for a ticket

    Interview Note: Separate endpoint for payment confirmation
    In real system, this would be called by payment gateway callback

    URL: /api/tickets/{ticket_id}/confirm-payment/
    """
    payment_success = request.data.get('payment_success', False)

    try:
        ticket = BookingService().confirm_booking(
            ticket_id=ticket_id,
            payment_success=payment_success
        )

        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

    except Ticket.DoesNotExist:
        return Response(
            {'error': 'Ticket not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    User registration

    Interview Note: AllowAny for registration endpoint
    """
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_coupon(request):
    """
    Validate coupon code

    Interview Note: Validation endpoint before booking
    """
    serializer = CouponValidationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # This is a simplified version - full logic in service
    from .models import Coupon
    try:
        coupon = Coupon.objects.get(code=serializer.validated_data['coupon_code'])
        if coupon.is_valid():
            return Response({
                'valid': True,
                'discount_type': coupon.discount_type,
                'discount_value': coupon.discount_value,
                'min_amount': coupon.min_amount
            })
        else:
            return Response({
                'valid': False,
                'error': 'Coupon is expired or inactive'
            })
    except Coupon.DoesNotExist:
        return Response({
            'valid': False,
            'error': 'Invalid coupon code'
        })


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint

    Interview Note: Always good to have for monitoring
    """
    return Response({
        'status': 'ok',
        'service': 'bookmyshow',
        'booking_service': BookingService.__name__
    })


"""
INTERVIEW NOTES: View Layer Best Practices

1. Thin Views, Fat Services
   - Views should only handle HTTP concerns
   - Business logic belongs in services
   - Validation in serializers

2. Use Appropriate View Types
   - ViewSets for standard CRUD
   - Function-based views for custom logic
   - APIView for full control

3. Serializer Selection
   - Different serializers for list vs detail
   - Different for read vs write
   - Nested serializers carefully (performance!)

4. Query Optimization
   - select_related for ForeignKey (JOIN)
   - prefetch_related for ManyToMany (separate queries)
   - Annotate for aggregations

5. Permissions
   - AllowAny for public endpoints
   - IsAuthenticated for user-specific
   - Custom permissions for complex rules

6. Error Handling
   - Use appropriate HTTP status codes
   - Return meaningful error messages
   - Log errors for debugging

7. Pagination
   - Always paginate list endpoints
   - Configurable page size
   - Return total count

Common Interview Questions:

Q: What's the difference between APIView and ViewSet?
A: APIView gives full control, ViewSet provides standard CRUD methods.
   Use APIView for custom endpoints, ViewSet for REST resources.

Q: How do you prevent N+1 queries?
A: Use select_related (JOIN) for ForeignKey, prefetch_related for M2M.

Q: Where should business logic go?
A: Services! Views should be thin - only handle HTTP concerns.

Q: How to handle transactions in views?
A: In services with @transaction.atomic decorator, not in views.

Q: How to version APIs?
A: URL versioning (/api/v1/), Header versioning, or Accept header.
"""
