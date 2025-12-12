"""
BookMyShow Serializers
Demonstrates different serializer patterns for LLD interviews

Key Concepts:
1. ModelSerializer vs Serializer
2. Nested serializers (read vs write)
3. SerializerMethodField for computed fields
4. Different serializers for read vs write operations
5. Validation at field and object level
"""
from rest_framework import serializers
from django.utils import timezone
from .models import (
    City, Theater, Screen, Seat, Movie, Show, ShowSeat,
    User, Ticket, TicketSeat, Payment, PricingRule, Coupon,
    SeatType, SeatStatus, PaymentMode, PaymentStatus, TicketStatus
)


# ============= City, Theater, Screen Serializers =============

class CitySerializer(serializers.ModelSerializer):
    """
    Basic ModelSerializer
    Interview Note: ModelSerializer auto-generates fields from model
    """
    theater_count = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['id', 'name', 'theater_count', 'created_at']
        read_only_fields = ['created_at']

    def get_theater_count(self, obj):
        """Computed field - Interview Tip: Use select_related/prefetch_related"""
        return obj.theaters.count()


class ScreenSerializer(serializers.ModelSerializer):
    """Screen serializer with seat count"""
    seat_count = serializers.SerializerMethodField()
    available_seat_types = serializers.SerializerMethodField()

    class Meta:
        model = Screen
        fields = ['id', 'name', 'theater', 'seat_count', 'available_seat_types']

    def get_seat_count(self, obj):
        return obj.seats.count()

    def get_available_seat_types(self, obj):
        """Get unique seat types in this screen"""
        return list(obj.seats.values_list('seat_type', flat=True).distinct())


class TheaterSerializer(serializers.ModelSerializer):
    """
    Theater with nested screens
    Interview Note: Nested serializers - read_only for GET, write separately
    """
    city_name = serializers.CharField(source='city.name', read_only=True)
    screens = ScreenSerializer(many=True, read_only=True)
    screen_count = serializers.SerializerMethodField()

    class Meta:
        model = Theater
        fields = ['id', 'name', 'address', 'city', 'city_name', 'screens', 'screen_count']

    def get_screen_count(self, obj):
        return obj.screens.count()


class TheaterListSerializer(serializers.ModelSerializer):
    """
    Lighter serializer for list views
    Interview Tip: Use different serializers for list vs detail views
    """
    city_name = serializers.CharField(source='city.name', read_only=True)
    screen_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Theater
        fields = ['id', 'name', 'city_name', 'screen_count']


# ============= Movie Serializers =============

class MovieSerializer(serializers.ModelSerializer):
    """
    Movie serializer with validation
    Interview Note: Custom validation in validate_<field> and validate()
    """
    languages_display = serializers.SerializerMethodField()
    show_count = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'name', 'rating', 'category', 'languages',
            'languages_display', 'duration', 'description',
            'show_count', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_languages_display(self, obj):
        """Format languages as comma-separated string"""
        return ', '.join(obj.languages) if obj.languages else ''

    def get_show_count(self, obj):
        """Count upcoming shows"""
        return obj.shows.filter(start_time__gte=timezone.now()).count()

    def validate_rating(self, value):
        """
        Field-level validation
        Interview Note: Called automatically for each field
        """
        if value < 0 or value > 10:
            raise serializers.ValidationError("Rating must be between 0 and 10")
        return value

    def validate_languages(self, value):
        """Ensure languages is a non-empty list"""
        if not isinstance(value, list) or len(value) == 0:
            raise serializers.ValidationError("At least one language is required")
        return value

    def validate(self, data):
        """
        Object-level validation
        Interview Note: Use for validations involving multiple fields
        """
        if data.get('duration', 0) <= 0:
            raise serializers.ValidationError("Duration must be positive")
        return data


# ============= Show and ShowSeat Serializers =============

class SeatSerializer(serializers.ModelSerializer):
    """Basic seat serializer"""
    class Meta:
        model = Seat
        fields = ['id', 'number', 'seat_type']


class ShowSeatSerializer(serializers.ModelSerializer):
    """
    ShowSeat with seat details
    Interview Note: Nested read-only serializer for related data
    """
    seat = SeatSerializer(read_only=True)
    seat_number = serializers.CharField(source='seat.number', read_only=True)
    seat_type = serializers.CharField(source='seat.seat_type', read_only=True)

    class Meta:
        model = ShowSeat
        fields = [
            'id', 'seat', 'seat_number', 'seat_type',
            'status', 'price', 'locked_at'
        ]
        read_only_fields = ['locked_at']


class ShowSerializer(serializers.ModelSerializer):
    """
    Show serializer with all related information
    Interview Note: Multiple nested serializers
    """
    movie_name = serializers.CharField(source='movie.name', read_only=True)
    movie_rating = serializers.FloatField(source='movie.rating', read_only=True)
    theater_name = serializers.CharField(source='theater.name', read_only=True)
    screen_name = serializers.CharField(source='screen.name', read_only=True)
    city_name = serializers.CharField(source='theater.city.name', read_only=True)
    end_time = serializers.DateTimeField(read_only=True)
    cutoff_time = serializers.DateTimeField(read_only=True)
    is_booking_allowed = serializers.BooleanField(read_only=True)
    available_seats_count = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = [
            'id', 'movie', 'movie_name', 'movie_rating',
            'theater', 'theater_name', 'screen', 'screen_name',
            'city_name', 'start_time', 'end_time', 'cutoff_time',
            'duration', 'language', 'is_booking_allowed',
            'available_seats_count'
        ]

    def get_available_seats_count(self, obj):
        """Count available seats"""
        return obj.show_seats.filter(status=SeatStatus.AVAILABLE).count()


class ShowDetailSerializer(ShowSerializer):
    """
    Detailed show serializer with seat layout
    Interview Tip: Extend serializers for detail views
    """
    show_seats = ShowSeatSerializer(many=True, read_only=True)

    class Meta(ShowSerializer.Meta):
        fields = ShowSerializer.Meta.fields + ['show_seats']


# ============= Booking Serializers =============

class BookingRequestSerializer(serializers.Serializer):
    """
    Non-model serializer for booking request
    Interview Note: Use Serializer (not ModelSerializer) for non-model data
    """
    show_id = serializers.CharField()
    seat_ids = serializers.ListField(
        child=serializers.CharField(),
        min_length=1,
        max_length=10
    )
    payment_mode = serializers.ChoiceField(choices=PaymentMode.choices)
    coupon_code = serializers.CharField(required=False, allow_blank=True)

    def validate_seat_ids(self, value):
        """Ensure unique seat IDs"""
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Duplicate seat IDs found")
        return value

    def validate(self, data):
        """
        Cross-field validation
        Interview Note: Check business rules here
        """
        # Validate show exists and booking is allowed
        try:
            show = Show.objects.get(id=data['show_id'])
            if not show.is_booking_allowed():
                raise serializers.ValidationError(
                    "Booking not allowed. Cutoff time has passed."
                )
        except Show.DoesNotExist:
            raise serializers.ValidationError("Invalid show ID")

        # Validate seats belong to the show
        seat_ids = data['seat_ids']
        show_seats = ShowSeat.objects.filter(
            id__in=seat_ids,
            show_id=data['show_id']
        )

        if show_seats.count() != len(seat_ids):
            raise serializers.ValidationError("Invalid seat IDs for this show")

        # Check if any seat is not available
        unavailable = show_seats.exclude(status=SeatStatus.AVAILABLE)
        if unavailable.exists():
            unavailable_seats = list(unavailable.values_list('seat__number', flat=True))
            raise serializers.ValidationError(
                f"Seats not available: {', '.join(unavailable_seats)}"
            )

        data['show'] = show
        data['show_seats'] = show_seats
        return data


class TicketSeatSerializer(serializers.ModelSerializer):
    """Ticket seat with details"""
    seat_number = serializers.CharField(source='show_seat.seat.number', read_only=True)
    seat_type = serializers.CharField(source='show_seat.seat.seat_type', read_only=True)
    price = serializers.DecimalField(
        source='show_seat.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = TicketSeat
        fields = ['seat_number', 'seat_type', 'price']


class PaymentSerializer(serializers.ModelSerializer):
    """Payment details"""
    class Meta:
        model = Payment
        fields = [
            'id', 'amount', 'mode', 'status',
            'transaction_id', 'timestamp'
        ]
        read_only_fields = ['timestamp']


class TicketSerializer(serializers.ModelSerializer):
    """
    Ticket serializer with full details
    Interview Note: Multiple nested serializers for complete representation
    """
    user_name = serializers.CharField(source='user.username', read_only=True)
    movie_name = serializers.CharField(source='show.movie.name', read_only=True)
    theater_name = serializers.CharField(source='show.theater.name', read_only=True)
    screen_name = serializers.CharField(source='show.screen.name', read_only=True)
    show_time = serializers.DateTimeField(source='show.start_time', read_only=True)
    seats = TicketSeatSerializer(source='ticket_seats', many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)
    can_cancel = serializers.BooleanField(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'user_name', 'movie_name', 'theater_name',
            'screen_name', 'show_time', 'amount', 'status',
            'booking_time', 'seats', 'payment', 'can_cancel'
        ]
        read_only_fields = ['booking_time']


class TicketListSerializer(serializers.ModelSerializer):
    """
    Lighter serializer for ticket list
    Interview Tip: Optimize for list views
    """
    movie_name = serializers.CharField(source='show.movie.name', read_only=True)
    show_time = serializers.DateTimeField(source='show.start_time', read_only=True)
    seat_count = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id', 'movie_name', 'show_time', 'amount',
            'status', 'booking_time', 'seat_count'
        ]

    def get_seat_count(self, obj):
        return obj.ticket_seats.count()


# ============= User Serializers =============

class UserSerializer(serializers.ModelSerializer):
    """User serializer for profile"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Separate serializer for user creation
    Interview Note: Different serializer for create to handle password
    """
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        """Override create to hash password"""
        user = User.objects.create_user(**validated_data)
        return user


# ============= Other Serializers =============

class CouponSerializer(serializers.ModelSerializer):
    """Coupon serializer with validation"""
    is_valid_now = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = [
            'code', 'description', 'discount_type', 'discount_value',
            'min_amount', 'max_discount', 'valid_from', 'valid_until',
            'is_valid_now'
        ]

    def get_is_valid_now(self, obj):
        return obj.is_valid()


class CouponValidationSerializer(serializers.Serializer):
    """
    Serializer for coupon validation request
    Interview Note: Request/Response pattern with Serializer
    """
    coupon_code = serializers.CharField()
    booking_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_booking_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Booking amount must be positive")
        return value
