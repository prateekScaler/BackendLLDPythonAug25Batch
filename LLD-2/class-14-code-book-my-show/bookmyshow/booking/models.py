"""
BookMyShow Django Models
Following the LLD design pattern with proper relationships

Key Concepts for Interviews:
1. OneToMany: ForeignKey (reverse: related_name)
2. ManyToMany: Through model for additional fields
3. Enums: TextChoices for fixed values
4. Indexes: For performance on frequently queried fields
5. Constraints: For data integrity
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta


class SeatType(models.TextChoices):
    """Enum for seat types - Interview tip: Use TextChoices over CharField choices"""
    GOLD = 'GOLD', 'Gold'
    DIAMOND = 'DIAMOND', 'Diamond'
    PLATINUM = 'PLATINUM', 'Platinum'


class SeatStatus(models.TextChoices):
    """Seat booking status - Important for concurrency control"""
    AVAILABLE = 'AVAILABLE', 'Available'
    BOOKED = 'BOOKED', 'Booked'
    LOCKED = 'LOCKED', 'Locked'  # Temporary lock during booking process


class PaymentMode(models.TextChoices):
    """Payment methods"""
    UPI = 'UPI', 'UPI'
    CREDIT_CARD = 'CREDIT_CARD', 'Credit Card'
    NETBANKING = 'NETBANKING', 'Net Banking'


class PaymentStatus(models.TextChoices):
    """Payment transaction status"""
    PENDING = 'PENDING', 'Pending'
    SUCCESS = 'SUCCESS', 'Success'
    FAILED = 'FAILED', 'Failed'
    REFUNDED = 'REFUNDED', 'Refunded'


class TicketStatus(models.TextChoices):
    """Ticket booking status"""
    BOOKED = 'BOOKED', 'Booked'
    CANCELLED = 'CANCELLED', 'Cancelled'
    CONFIRMED = 'CONFIRMED', 'Confirmed'


class City(models.Model):
    """
    City model - Root of the hierarchy
    This is the entry point for location-based filtering
    """
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Cities'
        ordering = ['name']

    def __str__(self):
        return self.name


class Theater(models.Model):
    """
    Theater/Cinema model
    Contains screens and shows
    Relationship: City -> Theater (One to Many via ForeignKey)
    """
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200, db_index=True)
    address = models.TextField()
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='theaters'  # city.theaters.all()
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['city', 'name']
        indexes = [
            models.Index(fields=['city', 'name']),
        ]

    def __str__(self):
        return f"{self.name} - {self.city.name}"


class Screen(models.Model):
    """
    Screen/Hall within a theater
    Interview Note: Each screen has seats and shows movies
    Relationship: Theater -> Screen (One to Many)
    """
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    theater = models.ForeignKey(
        Theater,
        on_delete=models.CASCADE,
        related_name='screens'  # theater.screens.all()
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['theater', 'name']
        unique_together = ['theater', 'name']

    def __str__(self):
        return f"{self.theater.name} - {self.name}"


class Seat(models.Model):
    """
    Seat configuration in a screen
    Interview Note: This is the template/master data for seats
    Relationship: Screen -> Seat (One to Many)
    """
    id = models.CharField(max_length=50, primary_key=True)
    number = models.CharField(max_length=10)  # e.g., A1, B5, etc.
    seat_type = models.CharField(
        max_length=20,
        choices=SeatType.choices,
        default=SeatType.GOLD
    )
    screen = models.ForeignKey(
        Screen,
        on_delete=models.CASCADE,
        related_name='seats'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['screen', 'number']
        unique_together = ['screen', 'number']
        indexes = [
            models.Index(fields=['screen', 'seat_type']),
        ]

    def __str__(self):
        return f"{self.screen.name} - {self.number} ({self.seat_type})"


class Movie(models.Model):
    """
    Movie model
    Interview Note: Movies can have multiple shows across different screens
    """
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200, db_index=True)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    category = models.CharField(max_length=50, db_index=True)  # Action, Drama, etc.
    languages = models.JSONField(default=list)  # List of languages: ['Hindi', 'English']
    duration = models.IntegerField(help_text="Duration in minutes")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-rating', 'name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return self.name


class Show(models.Model):
    """
    Show/Showtime model - The actual screening of a movie
    Interview Note: This is the core entity for booking
    Relationships:
    - Movie -> Show (One to Many)
    - Screen -> Show (One to Many)
    - Theater -> Show (One to Many)
    """
    id = models.CharField(max_length=50, primary_key=True)
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='shows'
    )
    screen = models.ForeignKey(
        Screen,
        on_delete=models.CASCADE,
        related_name='shows'
    )
    theater = models.ForeignKey(
        Theater,
        on_delete=models.CASCADE,
        related_name='shows'
    )
    start_time = models.DateTimeField(db_index=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    language = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time']
        indexes = [
            models.Index(fields=['movie', 'start_time']),
            models.Index(fields=['screen', 'start_time']),
            models.Index(fields=['theater', 'start_time']),
        ]
        # Ensure no overlapping shows on same screen
        constraints = [
            models.UniqueConstraint(
                fields=['screen', 'start_time'],
                name='unique_screen_showtime'
            )
        ]

    def __str__(self):
        return f"{self.movie.name} at {self.theater.name} - {self.start_time}"

    @property
    def end_time(self):
        """Calculate end time of the show"""
        return self.start_time + timedelta(minutes=self.duration)

    @property
    def cutoff_time(self):
        """Cutoff time for booking (1 hour before start)"""
        return self.start_time - timedelta(hours=1)

    def is_booking_allowed(self):
        """Check if booking is still allowed"""
        return timezone.now() < self.cutoff_time


class ShowSeat(models.Model):
    """
    ShowSeat - Instance of a seat for a specific show
    Interview Note: This is critical for concurrency control

    Key Points:
    1. Created when a show is created (one per seat per show)
    2. Status changes: AVAILABLE -> LOCKED -> BOOKED
    3. LOCKED is temporary during payment processing
    4. Price varies based on multiple factors

    Relationship: Through model connecting Show and Seat
    """
    id = models.CharField(max_length=50, primary_key=True)
    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE,
        related_name='show_seats'
    )
    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE,
        related_name='show_seats'
    )
    status = models.CharField(
        max_length=20,
        choices=SeatStatus.choices,
        default=SeatStatus.AVAILABLE,
        db_index=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    locked_at = models.DateTimeField(null=True, blank=True)
    locked_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='locked_seats'
    )
    version = models.IntegerField(default=0)  # For optimistic locking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['show', 'seat']
        unique_together = ['show', 'seat']
        indexes = [
            models.Index(fields=['show', 'status']),
            models.Index(fields=['locked_at']),
        ]

    def __str__(self):
        return f"{self.show} - {self.seat.number} ({self.status})"


class User(AbstractUser):
    """
    Extended User model
    Interview Note: Using AbstractUser for flexibility
    """
    phone = models.CharField(max_length=15, unique=True)

    # Fix for groups and user_permissions clash
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='booking_users',
        related_query_name='booking_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='booking_users',
        related_query_name='booking_user',
    )

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username


class Ticket(models.Model):
    """
    Ticket/Booking model
    Interview Note: Main booking entity

    Relationships:
    - User -> Ticket (One to Many)
    - Show -> Ticket (One to Many)
    - Ticket -> ShowSeat (One to Many via ticket_seats)
    - Ticket -> Payment (One to One)
    """
    id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    status = models.CharField(
        max_length=20,
        choices=TicketStatus.choices,
        default=TicketStatus.BOOKED,
        db_index=True
    )
    booking_time = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-booking_time']
        indexes = [
            models.Index(fields=['user', 'booking_time']),
            models.Index(fields=['show', 'booking_time']),
        ]

    def __str__(self):
        return f"Ticket {self.id} - {self.user.username} - {self.show.movie.name}"

    def can_cancel(self):
        """Check if ticket can be cancelled (before cutoff time)"""
        return (
            self.status == TicketStatus.CONFIRMED and
            timezone.now() < self.show.cutoff_time
        )


class TicketSeat(models.Model):
    """
    Through model connecting Ticket and ShowSeat
    Interview Note: Explicit many-to-many with additional fields
    """
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='ticket_seats'
    )
    show_seat = models.ForeignKey(
        ShowSeat,
        on_delete=models.CASCADE,
        related_name='ticket_seats'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['ticket', 'show_seat']

    def __str__(self):
        return f"{self.ticket.id} - {self.show_seat.seat.number}"


class Payment(models.Model):
    """
    Payment model
    Interview Note: One-to-One with Ticket

    Key Points:
    1. Created when booking is initiated
    2. Status changes: PENDING -> SUCCESS/FAILED
    3. Refund creates new payment with REFUNDED status
    """
    id = models.CharField(max_length=50, primary_key=True)
    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    mode = models.CharField(
        max_length=20,
        choices=PaymentMode.choices
    )
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        db_index=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['ticket', 'status']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"Payment {self.id} - {self.ticket.id} - {self.status}"


class PricingRule(models.Model):
    """
    Dynamic pricing configuration
    Interview Note: Business logic for price calculation

    Price varies based on:
    - Seat type
    - Day of week (weekend surge)
    - Time of day (prime time)
    - Movie (blockbusters cost more)
    - Theater/Screen (premium screens)
    """
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Multipliers
    seat_type = models.CharField(max_length=20, choices=SeatType.choices, null=True, blank=True)
    seat_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)

    # Day of week (0=Monday, 6=Sunday)
    day_of_week = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(6)]
    )
    day_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)

    # Time of day
    start_hour = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(23)]
    )
    end_hour = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(23)]
    )
    time_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)

    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Coupon(models.Model):
    """
    Discount coupon model
    Interview Note: Business feature for promotions
    """
    code = models.CharField(max_length=50, unique=True, primary_key=True)
    description = models.TextField()
    discount_type = models.CharField(
        max_length=20,
        choices=[('PERCENTAGE', 'Percentage'), ('FIXED', 'Fixed Amount')]
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Minimum booking amount to apply coupon"
    )
    max_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Maximum discount amount (for percentage type)"
    )
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    usage_limit = models.IntegerField(default=1, help_text="Max uses per user")
    total_usage_limit = models.IntegerField(null=True, blank=True, help_text="Total uses allowed")
    current_usage = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.discount_value}"

    def is_valid(self):
        """Check if coupon is currently valid"""
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_until and
            (self.total_usage_limit is None or self.current_usage < self.total_usage_limit)
        )
