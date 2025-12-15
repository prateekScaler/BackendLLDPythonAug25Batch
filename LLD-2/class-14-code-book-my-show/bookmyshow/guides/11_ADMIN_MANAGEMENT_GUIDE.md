# Admin Management Guide - System Administration

## Overview

This guide covers **administrative operations** for managing the BookMyShow system - adding movies, theaters, shows, pricing, and coupons.

**Admin Capabilities:**
```
1. Manage Movies (CRUD)
2. Manage Theaters & Screens (CRUD)
3. Manage Shows & Schedules
4. Set Pricing Rules
5. Create Coupons
6. View Analytics
```

**Access Control:**
- Only staff/superusers can manage data
- Uses Django Admin + REST API
- Permissions per resource

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Django Admin Interface](#django-admin-interface)
3. [REST API for Admin](#rest-api-for-admin)
4. [Flow 1: Add Movie](#flow-1-add-movie)
5. [Flow 2: Create Show](#flow-2-create-show)
6. [Flow 3: Set Pricing](#flow-3-set-pricing)
7. [Flow 4: Create Coupon](#flow-4-create-coupon)
8. [Data Seeding](#data-seeding)

---

## Architecture Overview

```
┌────────────────────────────────────┐
│        Admin Interface             │
│                                    │
│  Option 1: Django Admin            │
│  /admin/                           │
│  - Built-in UI                     │
│  - Full CRUD                       │
│  - No custom code needed           │
│                                    │
│  Option 2: REST API                │
│  /api/admin/                       │
│  - Custom admin dashboard          │
│  - Mobile admin apps               │
│  - Integration with other systems  │
└─────────┬──────────────────────────┘
          │
          ↓
┌────────────────────────────────────┐
│        Authorization               │
│  - IsAdminUser permission          │
│  - IsStaff permission              │
│  - Custom permissions              │
└─────────┬──────────────────────────┘
          │
          ↓
┌────────────────────────────────────┐
│      Models (Django ORM)           │
│  - Movie, Theater, Show            │
│  - PricingRule, Coupon             │
│  - All with admin.ModelAdmin       │
└────────────────────────────────────┘
```

**Two Approaches:**

1. **Django Admin** - Quick, built-in, works out of the box
2. **REST API** - Custom dashboards, mobile apps, integrations

---

## Django Admin Interface

### Setup

**File:** `booking/admin.py`

```python
from django.contrib import admin
from booking.models import (
    City, Theater, Screen, Seat, Movie, Show,
    ShowSeat, User, Ticket, Payment, TicketSeat,
    PricingRule, Coupon
)

# Register all models with admin
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'state', 'theater_count']
    search_fields = ['name', 'state']
    ordering = ['name']

    def theater_count(self, obj):
        """Show number of theaters in city"""
        return obj.theaters.count()
    theater_count.short_description = 'Theaters'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'language', 'rating',
        'duration', 'release_date', 'shows_count'
    ]
    list_filter = ['category', 'language', 'release_date']
    search_fields = ['name', 'description']
    ordering = ['-release_date']
    date_hierarchy = 'release_date'

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'poster_url')
        }),
        ('Details', {
            'fields': ('category', 'language', 'rating', 'duration', 'release_date')
        }),
    )

    def shows_count(self, obj):
        """Number of shows for this movie"""
        return obj.shows.count()
    shows_count.short_description = 'Shows'


@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'address', 'screen_count']
    list_filter = ['city']
    search_fields = ['name', 'address']
    raw_id_fields = ['city']  # Autocomplete for city

    def screen_count(self, obj):
        return obj.screens.count()
    screen_count.short_description = 'Screens'


@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    list_display = ['name', 'theater', 'capacity', 'seat_count']
    list_filter = ['theater__city']
    raw_id_fields = ['theater']

    def capacity(self, obj):
        return obj.seats.count()
    capacity.short_description = 'Seats'

    def seat_count(self, obj):
        return obj.seats.count()


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'movie', 'theater', 'screen',
        'start_time', 'available_seats', 'booked_seats'
    ]
    list_filter = ['start_time', 'screen__theater__city']
    search_fields = ['movie__name', 'screen__theater__name']
    raw_id_fields = ['movie', 'screen']
    date_hierarchy = 'start_time'

    def theater(self, obj):
        return obj.screen.theater.name

    def available_seats(self, obj):
        return obj.showseat_set.filter(status='AVAILABLE').count()
    available_seats.short_description = 'Available'

    def booked_seats(self, obj):
        return obj.showseat_set.filter(status='BOOKED').count()
    booked_seats.short_description = 'Booked'


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'movie', 'show_time',
        'total_amount', 'status', 'booking_time'
    ]
    list_filter = ['status', 'booking_time']
    search_fields = ['id', 'user__username', 'show__movie__name']
    raw_id_fields = ['user', 'show']
    readonly_fields = ['booking_time', 'id']
    date_hierarchy = 'booking_time'

    def movie(self, obj):
        return obj.show.movie.name

    def show_time(self, obj):
        return obj.show.start_time

    fieldsets = (
        ('Ticket Information', {
            'fields': ('id', 'user', 'show', 'booking_time')
        }),
        ('Payment', {
            'fields': ('total_amount', 'status')
        }),
    )


@admin.register(PricingRule)
class PricingRuleAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'seat_type', 'base_price',
        'day_multiplier', 'time_multiplier',
        'is_active'
    ]
    list_filter = ['seat_type', 'is_active', 'day_of_week']
    search_fields = ['name']

    fieldsets = (
        ('Basic', {
            'fields': ('name', 'seat_type', 'base_price', 'is_active')
        }),
        ('Multipliers', {
            'fields': ('day_of_week', 'day_multiplier', 'time_of_day', 'time_multiplier')
        }),
        ('Scope', {
            'fields': ('movie', 'theater'),
            'description': 'Leave empty to apply globally'
        }),
    )


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'discount_percent', 'max_discount',
        'valid_from', 'valid_until', 'is_active', 'usage_count'
    ]
    list_filter = ['is_active', 'valid_from', 'valid_until']
    search_fields = ['code']
    date_hierarchy = 'valid_from'

    fieldsets = (
        ('Coupon Details', {
            'fields': ('code', 'description')
        }),
        ('Discount', {
            'fields': ('discount_percent', 'max_discount')
        }),
        ('Validity', {
            'fields': ('valid_from', 'valid_until', 'is_active')
        }),
        ('Usage Limits', {
            'fields': ('max_uses', 'max_uses_per_user')
        }),
    )

    def usage_count(self, obj):
        """Count how many times coupon was used"""
        return obj.tickets.count()
    usage_count.short_description = 'Used'


# Inline admin for nested editing
class ScreenInline(admin.TabularInline):
    model = Screen
    extra = 1
    fields = ['name', 'capacity']


class TheaterAdminWithScreens(admin.ModelAdmin):
    """Theater admin with inline screen editing"""
    list_display = ['name', 'city', 'screen_count']
    inlines = [ScreenInline]

    def screen_count(self, obj):
        return obj.screens.count()


# Re-register Theater with inlines
admin.site.unregister(Theater)
admin.site.register(Theater, TheaterAdminWithScreens)
```

**Location:** `booking/admin.py:1-200`

### Features

**1. List Display**
- Customizable columns
- Sortable
- Filterable
- Searchable

**2. Fieldsets**
- Organized form layout
- Collapsible sections
- Help text

**3. Inline Editing**
- Edit related objects on same page
- E.g., Edit screens while editing theater

**4. Custom Actions**
```python
@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    actions = ['create_show_seats']

    def create_show_seats(self, request, queryset):
        """Bulk action to create ShowSeats for selected shows"""
        for show in queryset:
            # Get all seats from screen
            seats = show.screen.seats.all()

            for seat in seats:
                ShowSeat.objects.get_or_create(
                    show=show,
                    seat=seat,
                    defaults={
                        'price': calculate_price(show, seat),
                        'status': 'AVAILABLE'
                    }
                )

        self.message_user(request, f"Created ShowSeats for {queryset.count()} shows")

    create_show_seats.short_description = "Create ShowSeats for selected shows"
```

### Access Django Admin

```
URL: http://localhost:8000/admin/

Login with superuser credentials:
Username: admin
Password: admin123
```

**Create Superuser:**
```bash
python manage.py createsuperuser
```

---

## REST API for Admin

### Permissions

**File:** `booking/permissions.py`

```python
from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Allow access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsAdminOrReadOnly(BasePermission):
    """
    Allow read access to anyone, write access to admins only.
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff
```

**Location:** `booking/permissions.py:1-20`

### ViewSets with Admin Permissions

```python
from rest_framework.viewsets import ModelViewSet
from booking.permissions import IsAdminUser, IsAdminOrReadOnly

class MovieViewSet(ModelViewSet):
    """
    GET: Anyone can view movies
    POST/PUT/DELETE: Only admins
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'


class ShowViewSet(ModelViewSet):
    """Only admins can manage shows"""
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        """Auto-create ShowSeats when show is created"""
        show = serializer.save()
        self.create_show_seats(show)

    def create_show_seats(self, show):
        """Create ShowSeat instances for all seats in screen"""
        seats = show.screen.seats.all()

        for seat in seats:
            price = self.calculate_price(show, seat)
            ShowSeat.objects.create(
                show=show,
                seat=seat,
                price=price,
                status='AVAILABLE'
            )

    def calculate_price(self, show, seat):
        """Calculate seat price based on pricing rules"""
        # Get applicable pricing rule
        rule = PricingRule.objects.filter(
            seat_type=seat.seat_type,
            is_active=True
        ).first()

        if rule:
            return rule.base_price
        return 200  # Default price
```

---

## Flow 1: Add Movie

**Admin Action:** Add a new movie to the system

### Using Django Admin

1. Navigate to: `/admin/booking/movie/`
2. Click "Add Movie"
3. Fill form:
   - Name: "Dune: Part Two"
   - Description: "Epic sci-fi sequel..."
   - Category: "Sci-Fi"
   - Language: "English"
   - Rating: 8.5
   - Duration: 166
   - Release Date: 2024-03-01
   - Poster URL: "https://..."
4. Click "Save"

### Using REST API

```http
POST /api/movies/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "Dune: Part Two",
  "description": "Epic sci-fi sequel...",
  "category": "Sci-Fi",
  "language": "English",
  "rating": 8.5,
  "duration": 166,
  "release_date": "2024-03-01",
  "poster_url": "https://..."
}
```

**Response (201 Created):**
```json
{
  "id": "dune-part-two",
  "name": "Dune: Part Two",
  "slug": "dune-part-two",
  "description": "Epic sci-fi sequel...",
  "category": "Sci-Fi",
  "language": "English",
  "rating": 8.5,
  "duration": 166,
  "release_date": "2024-03-01",
  "poster_url": "https://...",
  "created_at": "2024-12-15T10:00:00Z"
}
```

### Validation

```python
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def validate_rating(self, value):
        """Rating must be 0-10"""
        if not (0 <= value <= 10):
            raise serializers.ValidationError(
                "Rating must be between 0 and 10"
            )
        return value

    def validate_duration(self, value):
        """Duration must be positive"""
        if value <= 0:
            raise serializers.ValidationError(
                "Duration must be a positive number"
            )
        return value

    def validate_release_date(self, value):
        """Release date can't be too far in past"""
        from datetime import date, timedelta
        min_date = date.today() - timedelta(days=365*5)  # 5 years ago

        if value < min_date:
            raise serializers.ValidationError(
                "Release date cannot be more than 5 years in the past"
            )
        return value
```

---

## Flow 2: Create Show

**Admin Action:** Schedule a movie show

### Sequence Diagram

```
Admin           API              Service           Model
  │              │                 │                │
  │──POST /api/shows/─────────────>│                │
  │  {movie, screen, time}         │                │
  │              │                 │                │
  │              │──Create Show────────────────────>│
  │              │                 │                │
  │              │<──Show created──────────────────│
  │              │                 │                │
  │              │──Create ShowSeats─>              │
  │              │  (for all seats)│                │
  │              │  with pricing   │                │
  │              │                 │                │
  │              │                 │──Create 100 ShowSeats──>│
  │              │                 │                │
  │              │<────ShowSeats created────────────│
  │              │                 │                │
  │<─201 Created─│                 │                │
  │  {show + seats}                │                │
```

### API Endpoint

```http
POST /api/shows/
Authorization: Bearer <admin_token>

{
  "movie_id": "dune-part-two",
  "screen_id": "pvr-mumbai-1-screen-1",
  "start_time": "2024-12-20T18:00:00Z"
}
```

**Response (201 Created):**
```json
{
  "id": "show-dune-20241220-1800",
  "movie": {
    "id": "dune-part-two",
    "name": "Dune: Part Two"
  },
  "screen": {
    "id": "pvr-mumbai-1-screen-1",
    "name": "Screen 1",
    "theater": {
      "name": "PVR Phoenix Mumbai"
    }
  },
  "start_time": "2024-12-20T18:00:00Z",
  "end_time": "2024-12-20T20:46:00Z",
  "show_seats_created": 100,
  "price_range": {
    "min": 200,
    "max": 500
  }
}
```

### Code Flow

```python
class ShowViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        """
        Create show and automatically generate ShowSeats
        """
        show = serializer.save()

        # Generate unique show ID
        show.id = self.generate_show_id(show)
        show.save()

        # Create ShowSeats for all seats in screen
        seats_created = self.create_show_seats(show)

        # Store count for response
        show.seats_created = seats_created

    def generate_show_id(self, show):
        """Generate show ID: show-{movie}-{date}-{time}"""
        date_str = show.start_time.strftime('%Y%m%d')
        time_str = show.start_time.strftime('%H%M')
        movie_slug = show.movie.slug
        return f"show-{movie_slug}-{date_str}-{time_str}"

    def create_show_seats(self, show):
        """
        Create ShowSeat for each seat in screen
        """
        seats = show.screen.seats.all()
        show_seats_to_create = []

        for seat in seats:
            # Calculate price based on seat type and show time
            price = self.calculate_seat_price(show, seat)

            show_seat_id = f"{show.id}-{seat.id}"

            show_seats_to_create.append(
                ShowSeat(
                    id=show_seat_id,
                    show=show,
                    seat=seat,
                    price=price,
                    status='AVAILABLE'
                )
            )

        # Bulk create for performance
        ShowSeat.objects.bulk_create(show_seats_to_create)

        return len(show_seats_to_create)

    def calculate_seat_price(self, show, seat):
        """
        Calculate price based on:
        - Seat type (GOLD, DIAMOND, PLATINUM)
        - Day of week (weekend = higher)
        - Time of day (evening = higher)
        - Movie popularity
        - Theater tier
        """
        # Get base price from pricing rule
        rule = PricingRule.objects.filter(
            seat_type=seat.seat_type,
            is_active=True
        ).first()

        base_price = rule.base_price if rule else 200

        # Apply multipliers
        multiplier = 1.0

        # Weekend multiplier
        if show.start_time.weekday() in [5, 6]:  # Sat, Sun
            multiplier *= 1.3

        # Evening show multiplier (6PM-10PM)
        hour = show.start_time.hour
        if 18 <= hour <= 22:
            multiplier *= 1.2

        # Movie rating multiplier
        if show.movie.rating >= 8.0:
            multiplier *= 1.1

        final_price = base_price * multiplier

        return round(final_price, 2)
```

**Location:** `booking/views.py:750-850`

### Validation

```python
class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ['id', 'movie', 'screen', 'start_time']

    def validate(self, data):
        """
        Validate show creation:
        1. Screen is available at this time
        2. No overlapping shows
        3. Start time is in future
        """
        movie = data['movie']
        screen = data['screen']
        start_time = data['start_time']

        # Check start time is in future
        if start_time <= timezone.now():
            raise serializers.ValidationError(
                "Show start time must be in the future"
            )

        # Calculate end time
        end_time = start_time + timedelta(minutes=movie.duration + 30)

        # Check for overlapping shows on same screen
        overlapping = Show.objects.filter(
            screen=screen,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if overlapping:
            raise serializers.ValidationError(
                "Screen is not available at this time. Show overlaps with another show."
            )

        return data
```

---

## Flow 3: Set Pricing

**Admin Action:** Configure dynamic pricing rules

### API Endpoint

```http
POST /api/pricing-rules/
Authorization: Bearer <admin_token>

{
  "name": "Weekend Evening GOLD",
  "seat_type": "GOLD",
  "base_price": 200,
  "day_of_week": "SAT",
  "day_multiplier": 1.3,
  "time_of_day": "EVENING",
  "time_multiplier": 1.2,
  "movie": null,
  "theater": null,
  "is_active": true
}
```

### Pricing Logic

```python
class PricingRule(models.Model):
    """
    Dynamic pricing configuration
    """
    name = models.CharField(max_length=100)
    seat_type = models.CharField(
        max_length=20,
        choices=SeatType.choices
    )
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Time-based multipliers
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('MON', 'Monday'),
            ('TUE', 'Tuesday'),
            ('WED', 'Wednesday'),
            ('THU', 'Thursday'),
            ('FRI', 'Friday'),
            ('SAT', 'Saturday'),
            ('SUN', 'Sunday'),
            ('WEEKDAY', 'Mon-Thu'),
            ('WEEKEND', 'Fri-Sun'),
            ('ANY', 'Any Day'),
        ],
        default='ANY'
    )
    day_multiplier = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=1.0
    )

    time_of_day = models.CharField(
        max_length=20,
        choices=[
            ('MORNING', '9AM-12PM'),
            ('AFTERNOON', '12PM-5PM'),
            ('EVENING', '5PM-10PM'),
            ('NIGHT', '10PM-12AM'),
            ('ANY', 'Any Time'),
        ],
        default='ANY'
    )
    time_multiplier = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=1.0
    )

    # Optional: specific to movie/theater
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    theater = models.ForeignKey(
        Theater,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'booking_pricingrule'
        ordering = ['-is_active', 'name']
```

**Location:** `booking/models.py:400-470`

### Example Pricing Rules

| Rule | Seat Type | Base | Day Mult | Time Mult | Final Price |
|------|-----------|------|----------|-----------|-------------|
| Weekday Morning GOLD | GOLD | ₹150 | 0.8 | 0.9 | ₹108 |
| Weekend Evening GOLD | GOLD | ₹200 | 1.3 | 1.2 | ₹312 |
| Friday Night PLATINUM | PLATINUM | ₹400 | 1.5 | 1.3 | ₹780 |
| Blockbuster Surcharge | Any | +₹50 | - | - | +₹50 |

---

## Flow 4: Create Coupon

**Admin Action:** Create discount coupon

### API Endpoint

```http
POST /api/coupons/
Authorization: Bearer <admin_token>

{
  "code": "NEWYEAR2025",
  "description": "New Year Special - 20% off",
  "discount_percent": 20,
  "max_discount": 100,
  "valid_from": "2025-01-01T00:00:00Z",
  "valid_until": "2025-01-07T23:59:59Z",
  "max_uses": 1000,
  "max_uses_per_user": 1,
  "is_active": true
}
```

**Response:**
```json
{
  "id": 5,
  "code": "NEWYEAR2025",
  "description": "New Year Special - 20% off",
  "discount_percent": 20,
  "max_discount": 100.00,
  "valid_from": "2025-01-01T00:00:00Z",
  "valid_until": "2025-01-07T23:59:59Z",
  "max_uses": 1000,
  "max_uses_per_user": 1,
  "times_used": 0,
  "is_active": true
}
```

### Model

```python
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    max_uses = models.IntegerField(null=True, blank=True)
    max_uses_per_user = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        """Check if coupon is currently valid"""
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_until and
            (self.max_uses is None or self.times_used < self.max_uses)
        )

    @property
    def times_used(self):
        """Count usage"""
        return self.tickets.count()
```

---

## Data Seeding

### Management Command

**File:** `booking/management/commands/seed_data.py`

```python
from django.core.management.base import BaseCommand
from booking.models import (
    City, Theater, Screen, Seat, Movie, Show,
    ShowSeat, PricingRule, Coupon, SeatType
)

class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create cities
        self.create_cities()

        # Create theaters
        self.create_theaters()

        # Create movies
        self.create_movies()

        # Create shows
        self.create_shows()

        # Create pricing rules
        self.create_pricing_rules()

        # Create coupons
        self.create_coupons()

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def create_cities(self):
        cities = [
            City(id='mumbai', name='Mumbai', state='Maharashtra'),
            City(id='delhi', name='Delhi', state='Delhi'),
            City(id='bangalore', name='Bangalore', state='Karnataka'),
        ]
        City.objects.bulk_create(cities, ignore_conflicts=True)
        self.stdout.write('✓ Cities created')

    def create_theaters(self):
        mumbai = City.objects.get(id='mumbai')

        theater = Theater.objects.create(
            id='pvr-mumbai-1',
            name='PVR Phoenix',
            address='High Street Phoenix, Lower Parel',
            city=mumbai
        )

        # Create screens
        for i in range(1, 4):
            screen = Screen.objects.create(
                id=f'pvr-mumbai-1-screen-{i}',
                name=f'Screen {i}',
                theater=theater
            )

            # Create seats
            for row in ['A', 'B', 'C', 'D', 'E']:
                for num in range(1, 11):
                    seat_type = SeatType.GOLD if row in ['A', 'B'] else SeatType.DIAMOND

                    Seat.objects.create(
                        id=f'pvr-mumbai-1-screen-{i}-{row}{num}',
                        screen=screen,
                        row=row,
                        number=str(num),
                        seat_type=seat_type
                    )

        self.stdout.write('✓ Theaters, screens, and seats created')

    def create_movies(self):
        movies = [
            Movie(
                id='avengers-endgame',
                name='Avengers: Endgame',
                description='Epic Marvel conclusion',
                category='Action',
                language='English',
                rating=8.4,
                duration=181,
                release_date='2019-04-26'
            ),
            Movie(
                id='dune-part-two',
                name='Dune: Part Two',
                description='Epic sci-fi sequel',
                category='Sci-Fi',
                language='English',
                rating=8.5,
                duration=166,
                release_date='2024-03-01'
            ),
        ]
        Movie.objects.bulk_create(movies, ignore_conflicts=True)
        self.stdout.write('✓ Movies created')

    def create_shows(self):
        # Create shows for next 7 days
        from datetime import datetime, timedelta

        movie = Movie.objects.get(id='avengers-endgame')
        screen = Screen.objects.get(id='pvr-mumbai-1-screen-1')

        for i in range(7):
            date = datetime.now() + timedelta(days=i)
            for hour in [14, 18, 21]:
                start_time = date.replace(hour=hour, minute=0)

                show = Show.objects.create(
                    id=f'show-{i}-{hour}',
                    movie=movie,
                    screen=screen,
                    start_time=start_time
                )

                # Create ShowSeats
                for seat in screen.seats.all():
                    ShowSeat.objects.create(
                        id=f'{show.id}-{seat.id}',
                        show=show,
                        seat=seat,
                        price=200 if seat.seat_type == SeatType.GOLD else 300,
                        status='AVAILABLE'
                    )

        self.stdout.write('✓ Shows and ShowSeats created')
```

**Location:** `booking/management/commands/seed_data.py:1-150`

**Run Command:**
```bash
python manage.py seed_data
```

---

## Summary: Files & Responsibilities

| Component | File | Responsibility |
|-----------|------|----------------|
| **Django Admin** | `booking/admin.py` | Admin interface configuration |
| **Permissions** | `booking/permissions.py` | IsAdminUser, IsAdminOrReadOnly |
| **ViewSets** | `booking/views.py` | Admin CRUD operations |
| **Models** | `booking/models.py` | Data structure |
| **Seed Command** | `management/commands/seed_data.py` | Sample data generation |

---

## Key Takeaways

### 1. Two Admin Approaches
- **Django Admin** - Quick, built-in, great for internal use
- **REST API** - Custom dashboards, mobile apps, integrations

### 2. Permission Layers
- `IsAdminUser` - Only staff can access
- `IsAdminOrReadOnly` - Anyone reads, admins write
- Per-object permissions for fine-grained control

### 3. Auto-Generation
- ShowSeats created automatically when Show is created
- Pricing calculated based on rules
- IDs generated with meaningful patterns

### 4. Bulk Operations
- `bulk_create()` for performance
- Custom admin actions for batch operations
- Seeding scripts for initial data

### 5. Validation
- Prevent overlapping shows
- Ensure dates are valid
- Check pricing rules are consistent

### 6. Computed Fields in Admin
- Show counts, usage stats
- Calculated prices
- Status indicators

---

## Conclusion

You've now covered all four major flows in the BookMyShow system:

1. **Browse Flow** (08) - Cities, Movies, Shows, Seat Selection
2. **Booking Flow** (09) - Locking, Payment, Concurrency Control
3. **Ticket Management** (10) - View, Cancel, Refunds
4. **Admin Management** (11) - CRUD, Pricing, Data Seeding

These guides provide:
- ✅ Complete code walkthroughs
- ✅ Sequence diagrams
- ✅ File locations
- ✅ Database queries
- ✅ Error handling
- ✅ Security considerations

**Next Steps:**
- Review [03_CONCURRENCY_CONTROL.md](./03_CONCURRENCY_CONTROL.md) for deep dive on locking strategies
- Check [02_VIEWS_AND_VIEWSETS.md](./02_VIEWS_AND_VIEWSETS.md) for ViewSet patterns
- Practice with [07_REST_API_DESIGN_QUIZ.md](./07_REST_API_DESIGN_QUIZ.md)

Happy interviewing! 🚀
