# Browse Flow Guide - Cities, Theaters, Movies & Shows

## Overview

This guide walks through the **browsing experience** where users explore available cities, theaters, movies, and shows before making a booking.

**User Journey:**
```
1. Select City
2. Browse Movies (or browse Theaters)
3. Select Movie
4. View Shows for Movie
5. Select Show & View Seat Layout
```

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Flow 1: List Cities](#flow-1-list-cities)
3. [Flow 2: Search Movies](#flow-2-search-movies)
4. [Flow 3: Get Movie Shows](#flow-3-get-movie-shows)
5. [Flow 4: View Show Details](#flow-4-view-show-details)
6. [Flow 5: Browse Theaters](#flow-5-browse-theaters)
7. [Complete Sequence Diagram](#complete-sequence-diagram)

---

## Architecture Overview

```
┌─────────────┐
│   Client    │
│  (Browser)  │
└──────┬──────┘
       │ HTTP Request
       ↓
┌─────────────────────────────────────┐
│           Django URLs               │
│    bookmyshow/urls.py              │
└──────┬──────────────────────────────┘
       │ Route to View
       ↓
┌─────────────────────────────────────┐
│          Views/ViewSets             │
│    booking/views.py                 │
│  - CityViewSet                      │
│  - MovieViewSet                     │
│  - ShowViewSet                      │
│  - TheaterViewSet                   │
└──────┬──────────────────────────────┘
       │ Get data
       ↓
┌─────────────────────────────────────┐
│         Serializers                 │
│    booking/serializers.py           │
│  - Validate data                    │
│  - Transform to JSON                │
└──────┬──────────────────────────────┘
       │ Query
       ↓
┌─────────────────────────────────────┐
│            Models                   │
│    booking/models.py                │
│  - Database queries via ORM         │
└─────────────────────────────────────┘
```

**No Service Layer in Browse Flows**: These are simple read operations, so we directly query models from views.

---

## Flow 1: List Cities

**User Action:** User opens app, needs to select their city

### Sequence Diagram

```
Client          View              Model              Serializer
  │              │                 │                     │
  │─────GET /api/cities/───────────>│                     │
  │              │                 │                     │
  │              │──City.objects.all()──>                │
  │              │                 │                     │
  │              │<──[City, City]──│                     │
  │              │                 │                     │
  │              │──────CitySerializer(cities, many=True)────>│
  │              │                 │                     │
  │              │<────JSON [{...}, {...}]──────────────│
  │              │                 │                     │
  │<────200 OK with cities─────────│                     │
  │              │                 │                     │
```

### API Endpoint

```http
GET /api/cities/
```

**Response:**
```json
[
  {
    "id": "mumbai",
    "name": "Mumbai",
    "state": "Maharashtra",
    "theater_count": 25
  },
  {
    "id": "delhi",
    "name": "Delhi",
    "state": "Delhi",
    "theater_count": 18
  }
]
```

### Code Flow

#### 1. URL Configuration
**File:** `bookmyshow/urls.py`

```python
from rest_framework.routers import DefaultRouter
from booking.views import CityViewSet

router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='city')

# Generates:
# GET  /api/cities/       -> list()
# GET  /api/cities/{id}/  -> retrieve()
```

#### 2. View (Controller)
**File:** `booking/views.py`

```python
class CityViewSet(ReadOnlyModelViewSet):
    """
    Read-only viewset for cities.
    Users can only view cities, not create/update/delete.

    Actions:
    - list():     GET /api/cities/
    - retrieve(): GET /api/cities/{slug}/
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'slug'  # Use city slug instead of pk
```

**Location:** `booking/views.py:15-25`

**What happens:**
1. `queryset = City.objects.all()` - Gets all cities from database
2. `ReadOnlyModelViewSet` - Only allows GET requests
3. `lookup_field = 'slug'` - Use city slug (e.g., "mumbai") in URLs

#### 3. Serializer
**File:** `booking/serializers.py`

```python
class CitySerializer(serializers.ModelSerializer):
    theater_count = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['id', 'name', 'state', 'theater_count']

    def get_theater_count(self, obj):
        """Count theaters in this city"""
        return obj.theaters.count()
```

**Location:** `booking/serializers.py:10-20`

**What it does:**
- Converts `City` model instance to JSON
- Adds computed field `theater_count`
- Only exposes safe fields (no internal IDs)

#### 4. Model
**File:** `booking/models.py`

```python
class City(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    class Meta:
        db_table = 'booking_city'
        verbose_name_plural = 'Cities'
```

**Location:** `booking/models.py:25-35`

**Database Query Generated:**
```sql
SELECT id, name, state FROM booking_city;
```

### Validation

✅ **No validation needed** - This is a simple GET request

### Error Handling

| Scenario | Response |
|----------|----------|
| No cities exist | `200 OK` with empty array `[]` |
| Invalid city slug | `404 Not Found` |
| Server error | `500 Internal Server Error` |

---

## Flow 2: Search Movies

**User Action:** User searches for movies in their city

### Sequence Diagram

```
Client          View                 Model              Serializer
  │              │                    │                     │
  │──GET /api/movies/search/?city=mumbai&query=avengers───>│
  │              │                    │                     │
  │              │──Filter queryset───│                     │
  │              │   by city          │                     │
  │              │   by query         │                     │
  │              │                    │                     │
  │              │<──[Movie, Movie]───│                     │
  │              │                    │                     │
  │              │────MovieSerializer(movies, many=True)────>│
  │              │                    │                     │
  │              │<────JSON [{...}, {...}]──────────────────│
  │              │                    │                     │
  │<────200 OK with movies─────────────                     │
  │              │                    │                     │
```

### API Endpoint

```http
GET /api/movies/search/?query=avengers&city=mumbai&min_rating=7&language=English
```

**Query Parameters:**
- `query` - Search in movie name/description
- `city` - Filter by city slug
- `min_rating` - Minimum rating (float)
- `language` - Filter by language
- `category` - Filter by genre

**Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "movie-1",
      "name": "Avengers: Endgame",
      "description": "Epic conclusion...",
      "rating": 8.4,
      "language": "English",
      "category": "Action",
      "duration": 181,
      "release_date": "2019-04-26",
      "poster_url": "https://...",
      "available_cities": ["mumbai", "delhi"]
    }
  ]
}
```

### Code Flow

#### 1. URL Configuration
**File:** `bookmyshow/urls.py`

```python
router.register(r'movies', MovieViewSet, basename='movie')

# Custom action generates:
# GET /api/movies/search/
```

#### 2. View (Controller)
**File:** `booking/views.py`

```python
class MovieViewSet(ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'slug'

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Search movies with advanced filters
        GET /api/movies/search/?query=avengers&city=mumbai
        """
        # Extract query parameters
        query = request.query_params.get('query', '')
        city = request.query_params.get('city')
        min_rating = request.query_params.get('min_rating')
        language = request.query_params.get('language')
        category = request.query_params.get('category')

        # Start with all movies
        queryset = Movie.objects.all()

        # Apply filters
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )

        if city:
            # Filter movies that have shows in this city
            queryset = queryset.filter(
                shows__theater__city__slug=city
            ).distinct()

        if min_rating:
            queryset = queryset.filter(rating__gte=float(min_rating))

        if language:
            queryset = queryset.filter(language=language)

        if category:
            queryset = queryset.filter(category=category)

        # Serialize and return
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
```

**Location:** `booking/views.py:50-95`

**Step-by-step:**
1. **Extract parameters** from query string
2. **Start with all movies** (`Movie.objects.all()`)
3. **Apply filters incrementally**:
   - Text search: `name__icontains` or `description__icontains`
   - City filter: Join through `shows → theater → city`
   - Rating filter: `rating__gte` (greater than or equal)
   - Language/Category: Exact match
4. **Use `.distinct()`** to avoid duplicate movies (multiple shows)
5. **Serialize** results to JSON
6. **Return response**

#### 3. Serializer
**File:** `booking/serializers.py`

```python
class MovieSerializer(serializers.ModelSerializer):
    available_cities = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'name', 'description', 'rating',
            'language', 'category', 'duration',
            'release_date', 'poster_url', 'available_cities'
        ]

    def get_available_cities(self, obj):
        """Get list of cities where this movie is showing"""
        return list(
            obj.shows.values_list('theater__city__slug', flat=True)
            .distinct()
        )
```

**Location:** `booking/serializers.py:30-50`

**Computed Fields:**
- `available_cities` - Joins through shows → theater → city

#### 4. Models Involved

**Primary Model:** `Movie`
```python
class Movie(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    rating = models.FloatField()
    language = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    duration = models.IntegerField()  # minutes
    release_date = models.DateField()
    poster_url = models.URLField()
```

**Location:** `booking/models.py:100-115`

**Related Models:**
- `Show` - Many shows per movie
- `Theater` - Through shows
- `City` - Through theater

**Database Query Generated:**
```sql
SELECT DISTINCT m.*
FROM booking_movie m
LEFT JOIN booking_show s ON s.movie_id = m.id
LEFT JOIN booking_theater t ON s.theater_id = t.id
LEFT JOIN booking_city c ON t.city_id = c.id
WHERE (m.name LIKE '%avengers%' OR m.description LIKE '%avengers%')
  AND c.slug = 'mumbai'
  AND m.rating >= 7.0
  AND m.language = 'English';
```

### Validation

| Parameter | Validation | Error |
|-----------|------------|-------|
| `query` | Optional, string | - |
| `city` | Must exist in database | 400 if invalid slug |
| `min_rating` | Must be float 0-10 | 400 if invalid |
| `language` | Optional, string | - |
| `category` | Optional, string | - |

### Error Handling

```python
if min_rating:
    try:
        min_rating = float(min_rating)
        if not (0 <= min_rating <= 10):
            raise ValueError
    except ValueError:
        return Response(
            {"error": "min_rating must be between 0 and 10"},
            status=400
        )
```

---

## Flow 3: Get Movie Shows

**User Action:** User selects a movie, wants to see showtimes

### Sequence Diagram

```
Client          View                 Model              Serializer
  │              │                    │                     │
  │──GET /api/movies/movie-1/shows/?city=mumbai&date=2024-12-15──>│
  │              │                    │                     │
  │              │──get_object()──────>│                     │
  │              │  (Movie)           │                     │
  │              │<───Movie───────────│                     │
  │              │                    │                     │
  │              │──Show.objects.filter()                   │
  │              │   movie=movie      │                     │
  │              │   city=city        │                     │
  │              │   date=date        │                     │
  │              │<──[Show, Show]─────│                     │
  │              │                    │                     │
  │              │────ShowSerializer(shows, many=True)──────>│
  │              │                    │                     │
  │              │<────JSON [{...}, {...}]──────────────────│
  │              │                    │                     │
  │<────200 OK with shows──────────────                     │
  │              │                    │                     │
```

### API Endpoint

```http
GET /api/movies/{movie_id}/shows/?city=mumbai&date=2024-12-15
```

**Response:**
```json
{
  "movie": {
    "id": "movie-1",
    "name": "Avengers: Endgame"
  },
  "shows": [
    {
      "id": "show-1",
      "start_time": "2024-12-15T14:00:00Z",
      "end_time": "2024-12-15T17:01:00Z",
      "theater": {
        "id": "pvr-mumbai-1",
        "name": "PVR Phoenix",
        "city": "Mumbai"
      },
      "screen": {
        "id": "screen-1",
        "name": "Screen 1",
        "capacity": 100
      },
      "available_seats": 45,
      "price_range": {
        "min": 200,
        "max": 500
      }
    }
  ]
}
```

### Code Flow

#### 1. URL Configuration
```python
router.register(r'movies', MovieViewSet, basename='movie')

# Custom action generates:
# GET /api/movies/{slug}/shows/
```

#### 2. View (Controller)
**File:** `booking/views.py`

```python
class MovieViewSet(ReadOnlyModelViewSet):
    @action(detail=True, methods=['get'])
    def shows(self, request, slug=None):
        """
        Get all shows for a movie
        GET /api/movies/{slug}/shows/?city=mumbai&date=2024-12-15
        """
        # Get the movie
        movie = self.get_object()

        # Extract query parameters
        city = request.query_params.get('city')
        date = request.query_params.get('date')

        # Filter shows
        shows = Show.objects.filter(movie=movie).select_related(
            'theater__city',
            'screen'
        )

        if city:
            shows = shows.filter(theater__city__slug=city)

        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
                shows = shows.filter(start_time__date=date_obj)
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD"},
                    status=400
                )

        # Order by start time
        shows = shows.order_by('start_time')

        # Serialize
        serializer = ShowSerializer(shows, many=True)
        return Response({
            "movie": MovieSerializer(movie).data,
            "shows": serializer.data
        })
```

**Location:** `booking/views.py:100-145`

**Step-by-step:**
1. **Get movie** using `self.get_object()` (from URL param)
2. **Extract filters** (city, date)
3. **Query shows** for this movie
4. **Optimize query** with `select_related()` (avoid N+1)
5. **Apply filters** incrementally
6. **Validate date format** (YYYY-MM-DD)
7. **Order results** by start time
8. **Return movie + shows**

#### 3. Serializer
**File:** `booking/serializers.py`

```python
class ShowSerializer(serializers.ModelSerializer):
    theater = TheaterSerializer(source='screen.theater', read_only=True)
    screen = ScreenSerializer(read_only=True)
    available_seats = serializers.SerializerMethodField()
    price_range = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = [
            'id', 'start_time', 'end_time',
            'theater', 'screen',
            'available_seats', 'price_range'
        ]

    def get_end_time(self, obj):
        """Calculate end time = start + movie duration"""
        return obj.start_time + timedelta(minutes=obj.movie.duration)

    def get_available_seats(self, obj):
        """Count available seats for this show"""
        return obj.showseat_set.filter(
            status=SeatStatus.AVAILABLE
        ).count()

    def get_price_range(self, obj):
        """Get min and max prices for this show"""
        prices = obj.showseat_set.values_list('price', flat=True)
        return {
            "min": min(prices) if prices else 0,
            "max": max(prices) if prices else 0
        }
```

**Location:** `booking/serializers.py:80-120`

**Nested Serializers:**
- `TheaterSerializer` - Theater details
- `ScreenSerializer` - Screen details

**Computed Fields:**
- `end_time` - Start time + movie duration
- `available_seats` - Count of AVAILABLE ShowSeats
- `price_range` - Min/max seat prices

#### 4. Models Involved

**Primary:** `Show`
```python
class Show(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='shows')
    start_time = models.DateTimeField()
```

**Related:**
- `Movie` (ForeignKey)
- `Screen` → `Theater` → `City` (through relationships)
- `ShowSeat` (reverse relationship)

**Location:** `booking/models.py:150-165`

### Validation

```python
# Date validation
if date:
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return Response(
            {"error": "Invalid date format. Use YYYY-MM-DD"},
            status=400
        )

# City validation (implicit)
if city:
    # If city doesn't exist, filter returns empty queryset
    # No error, just empty results
```

---

## Flow 4: View Show Details

**User Action:** User selects a show, views seat layout

### Sequence Diagram

```
Client          View                 Model              Serializer
  │              │                    │                     │
  │──GET /api/shows/show-1/───────────────────────────────>│
  │              │                    │                     │
  │              │──Show.objects.get()│                     │
  │              │  select_related()  │                     │
  │              │  prefetch_related()│                     │
  │              │<───Show with seats─│                     │
  │              │                    │                     │
  │              │────ShowDetailSerializer(show)────────────>│
  │              │                    │                     │
  │              │<────JSON with seat layout────────────────│
  │              │                    │                     │
  │<────200 OK with show + seats───────                     │
  │              │                    │                     │
```

### API Endpoint

```http
GET /api/shows/{show_id}/
```

**Response:**
```json
{
  "id": "show-1",
  "movie": {
    "id": "movie-1",
    "name": "Avengers: Endgame",
    "duration": 181
  },
  "theater": {
    "id": "pvr-mumbai-1",
    "name": "PVR Phoenix",
    "address": "High Street Phoenix, Mumbai"
  },
  "screen": {
    "id": "screen-1",
    "name": "Screen 1"
  },
  "start_time": "2024-12-15T14:00:00Z",
  "end_time": "2024-12-15T17:01:00Z",
  "show_seats": [
    {
      "id": "show-1-seat-A1",
      "seat": {
        "row": "A",
        "number": "1",
        "seat_type": "GOLD"
      },
      "price": 200.00,
      "status": "AVAILABLE"
    },
    {
      "id": "show-1-seat-A2",
      "seat": {
        "row": "A",
        "number": "2",
        "seat_type": "GOLD"
      },
      "price": 200.00,
      "status": "BOOKED"
    }
  ],
  "summary": {
    "total_seats": 100,
    "available": 45,
    "booked": 50,
    "locked": 5
  }
}
```

### Code Flow

#### 1. View (Controller)
**File:** `booking/views.py`

```python
class ShowViewSet(ReadOnlyModelViewSet):
    serializer_class = ShowDetailSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """
        Optimize query with select_related and prefetch_related
        """
        return Show.objects.select_related(
            'movie',
            'screen__theater__city'
        ).prefetch_related(
            'showseat_set__seat'
        ).all()

    def retrieve(self, request, *args, **kwargs):
        """
        GET /api/shows/{id}/
        Returns show with seat layout
        """
        show = self.get_object()
        serializer = self.get_serializer(show)
        return Response(serializer.data)
```

**Location:** `booking/views.py:180-210`

**Query Optimization:**
- `select_related()` - Joins movie, screen, theater, city (1 query)
- `prefetch_related()` - Fetches all ShowSeats (2 queries total)
- **Without optimization:** Would be N+1 queries (1 + number of seats)

#### 2. Serializer
**File:** `booking/serializers.py`

```python
class ShowDetailSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    theater = TheaterSerializer(source='screen.theater', read_only=True)
    screen = ScreenSerializer(read_only=True)
    show_seats = ShowSeatSerializer(source='showseat_set', many=True, read_only=True)
    summary = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = [
            'id', 'movie', 'theater', 'screen',
            'start_time', 'end_time', 'show_seats', 'summary'
        ]

    def get_end_time(self, obj):
        return obj.start_time + timedelta(minutes=obj.movie.duration)

    def get_summary(self, obj):
        """Seat availability summary"""
        seats = obj.showseat_set.all()
        return {
            "total_seats": seats.count(),
            "available": seats.filter(status=SeatStatus.AVAILABLE).count(),
            "booked": seats.filter(status=SeatStatus.BOOKED).count(),
            "locked": seats.filter(status=SeatStatus.LOCKED).count()
        }
```

**Location:** `booking/serializers.py:150-180`

**Nested Serializers:**
```python
class ShowSeatSerializer(serializers.ModelSerializer):
    seat = SeatSerializer(read_only=True)

    class Meta:
        model = ShowSeat
        fields = ['id', 'seat', 'price', 'status']

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['row', 'number', 'seat_type']
```

#### 3. Models Involved

**Primary:** `Show`
**Related:**
- `ShowSeat` (one-to-many)
- `Seat` (through ShowSeat)
- `Movie`, `Screen`, `Theater`, `City`

**Location:** `booking/models.py:200-250`

### Performance Optimization

**Bad (N+1 queries):**
```python
show = Show.objects.get(id=show_id)
# 1 query

for show_seat in show.showseat_set.all():
    # N queries (one per seat!)
    print(show_seat.seat.row, show_seat.seat.number)
```

**Good (3 queries total):**
```python
show = Show.objects.select_related('movie', 'screen__theater').prefetch_related('showseat_set__seat').get(id=show_id)
# Query 1: Get show with movie, screen, theater
# Query 2: Get all ShowSeats for this show
# Query 3: Get all Seats for those ShowSeats
```

---

## Flow 5: Browse Theaters

**User Action:** User wants to browse theaters in their city

### API Endpoint

```http
GET /api/theaters/?city=mumbai&search=PVR
```

**Response:**
```json
[
  {
    "id": "pvr-mumbai-1",
    "name": "PVR Phoenix",
    "address": "High Street Phoenix, Lower Parel",
    "city": "Mumbai",
    "screen_count": 8,
    "current_movies": ["movie-1", "movie-2", "movie-3"]
  }
]
```

### Code Flow

#### View
```python
class TheaterViewSet(ReadOnlyModelViewSet):
    serializer_class = TheaterSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Theater.objects.select_related('city').prefetch_related('screens')

        city = self.request.query_params.get('city')
        search = self.request.query_params.get('search')

        if city:
            queryset = queryset.filter(city__slug=city)

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset
```

**Location:** `booking/views.py:220-240`

---

## Complete Sequence Diagram

### End-to-End User Journey

```
User → Client → View → Serializer → Model → Database

[1] List Cities
User opens app
    │
    ├──GET /api/cities/
    │      └──CityViewSet.list()
    │             └──CitySerializer
    │                    └──City.objects.all()
    │
    └──Display: Mumbai, Delhi, Bangalore...

[2] Search Movies
User searches "Avengers" in Mumbai
    │
    ├──GET /api/movies/search/?query=avengers&city=mumbai
    │      └──MovieViewSet.search()
    │             └──Movie.objects.filter(...)
    │                    └──JOIN shows, theaters, cities
    │
    └──Display: Avengers Endgame, Avengers Age of Ultron...

[3] View Shows
User clicks "Avengers Endgame"
    │
    ├──GET /api/movies/movie-1/shows/?city=mumbai&date=2024-12-15
    │      └──MovieViewSet.shows()
    │             └──Show.objects.filter(movie=movie, city=city)
    │
    └──Display:
         PVR Phoenix - 2:00 PM (45 seats)
         INOX Mall - 6:00 PM (70 seats)

[4] View Seat Layout
User clicks "PVR Phoenix - 2:00 PM"
    │
    ├──GET /api/shows/show-1/
    │      └──ShowViewSet.retrieve()
    │             └──Show with ShowSeats (prefetch_related)
    │
    └──Display: Seat map
         [A1][A2][A3]  ← Available (Green)
         [B1][B2][B3]  ← Booked (Gray)
         [C1][C2][C3]  ← Locked (Yellow)

[5] Ready to Book
User selects seats A1, A2
    │
    └──Proceed to Booking Flow →
```

---

## Summary: Files & Responsibilities

| Component | File | Purpose |
|-----------|------|---------|
| **URLs** | `bookmyshow/urls.py` | Route requests to views |
| **Views** | `booking/views.py` | Handle HTTP, call models, return responses |
| **Serializers** | `booking/serializers.py` | Validate input, transform to/from JSON |
| **Models** | `booking/models.py` | Database structure, business logic |
| **Services** | N/A | Not used in browse flows (simple reads) |

---

## Key Takeaways

### 1. **Read-Only ViewSets**
Cities, Theaters, Movies, Shows are all `ReadOnlyModelViewSet` - users can't modify them.

### 2. **Custom Actions with @action**
- `@action(detail=True)` - Actions on single object (e.g., `/movies/{id}/shows/`)
- `@action(detail=False)` - Actions on collection (e.g., `/movies/search/`)

### 3. **Query Optimization**
Always use `select_related()` and `prefetch_related()` to avoid N+1 queries.

### 4. **Incremental Filtering**
Start with broad queryset, apply filters one by one based on query params.

### 5. **Nested Serializers**
Show details include Movie, Theater, Screen - all via nested serializers.

### 6. **Computed Fields**
- `available_seats` - Count at query time
- `price_range` - Min/max calculation
- `end_time` - Start time + duration

---

## Next Steps

**Continue to:** [09_BOOKING_FLOW_GUIDE.md](./09_BOOKING_FLOW_GUIDE.md)

This guide covers the **booking process** with concurrency control, payment, and ticket generation.
