# Django REST Framework Views and ViewSets Guide

## Table of Contents
1. [Overview](#overview)
2. [Function-Based Views (FBV)](#function-based-views-fbv)
3. [Class-Based Views (CBV)](#class-based-views-cbv)
4. [Generic Views](#generic-views)
5. [ViewSets](#viewsets)
6. [When to Use What](#when-to-use-what)
7. [Real Examples from BookMyShow](#real-examples-from-bookmyshow)
8. [Best Practices](#best-practices)
9. [Interview Questions](#interview-questions)

---

## Overview

Django REST Framework (DRF) provides multiple ways to create API endpoints. Understanding the **progression** and **trade-offs** is crucial for interviews.

### Evolution of Views in DRF

```
Function-Based Views (FBV)
    ↓ (more structure)
APIView (Class-Based)
    ↓ (reduce boilerplate)
Generic Views
    ↓ (more automation)
ViewSets + Routers
```

**Key Principle**: More abstraction = less code, but less flexibility.

---

## Function-Based Views (FBV)

### Basic Example

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def city_list(request):
    """
    List all cities or create a new city.
    """
    if request.method == 'GET':
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Detail View (Single Object)

```python
@api_view(['GET', 'PUT', 'DELETE'])
def city_detail(request, pk):
    """
    Retrieve, update, or delete a city.
    """
    try:
        city = City.objects.get(pk=pk)
    except City.DoesNotExist:
        return Response(
            {"error": "City not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = CitySerializer(city)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CitySerializer(city, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### Pros and Cons

✅ **Pros:**
- Simple and explicit
- Easy to understand for beginners
- Full control over logic
- Good for custom endpoints (e.g., `/book/`, `/confirm-payment/`)

❌ **Cons:**
- Lots of boilerplate code
- Repetitive (every endpoint needs similar code)
- Hard to reuse common patterns
- Manual validation, error handling

### When to Use FBV?

- **Custom actions** that don't fit CRUD (Create, Read, Update, Delete)
- **One-off endpoints** with unique logic
- **Non-resource-based APIs** (e.g., `/health/`, `/calculate/`)

**Examples from BookMyShow:**
```python
@api_view(['POST'])
def book_tickets(request):
    # Custom booking logic with concurrency control
    ...

@api_view(['POST'])
def validate_coupon(request):
    # Custom coupon validation logic
    ...
```

---

## Class-Based Views (CBV)

### APIView - Base Class

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CityList(APIView):
    """
    List all cities or create a new city.
    """
    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Detail View with APIView

```python
class CityDetail(APIView):
    """
    Retrieve, update, or delete a city.
    """
    def get_object(self, pk):
        try:
            return City.objects.get(pk=pk)
        except City.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        city = self.get_object(pk)
        serializer = CitySerializer(city)
        return Response(serializer.data)

    def put(self, request, pk):
        city = self.get_object(pk)
        serializer = CitySerializer(city, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        city = self.get_object(pk)
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### URLconf

```python
from django.urls import path

urlpatterns = [
    path('cities/', CityList.as_view(), name='city-list'),
    path('cities/<int:pk>/', CityDetail.as_view(), name='city-detail'),
]
```

### Pros and Cons

✅ **Pros:**
- Better organization (methods instead of if/elif)
- Reusable via inheritance
- Built-in support for permissions, authentication
- Mixin support for sharing behavior

❌ **Cons:**
- Still some boilerplate
- Need to handle get_object, validation manually

### When to Use APIView?

- Need **more control** than generic views
- Custom logic that doesn't fit standard CRUD
- Want **class-based organization** but full flexibility

---

## Generic Views

DRF provides **generic views** that reduce boilerplate for common patterns.

### ListCreateAPIView

Combines `GET` (list) and `POST` (create):

```python
from rest_framework.generics import ListCreateAPIView

class CityList(ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
```

**That's it!** DRF handles:
- Listing all cities
- Creating new cities
- Validation
- Pagination (if configured)

### RetrieveUpdateDestroyAPIView

Combines `GET`, `PUT`, `PATCH`, `DELETE` for a single object:

```python
from rest_framework.generics import RetrieveUpdateDestroyAPIView

class CityDetail(RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'pk'
```

### All Generic Views

| Generic View | Methods | Use Case |
|--------------|---------|----------|
| `CreateAPIView` | POST | Create only |
| `ListAPIView` | GET | List only (read-only) |
| `RetrieveAPIView` | GET | Detail only (read-only) |
| `DestroyAPIView` | DELETE | Delete only |
| `UpdateAPIView` | PUT, PATCH | Update only |
| `ListCreateAPIView` | GET, POST | List + Create |
| `RetrieveUpdateAPIView` | GET, PUT, PATCH | Detail + Update |
| `RetrieveDestroyAPIView` | GET, DELETE | Detail + Delete |
| `RetrieveUpdateDestroyAPIView` | GET, PUT, PATCH, DELETE | Full CRUD on single object |

### Customizing Generic Views

```python
class MovieList(ListCreateAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        """
        Optionally filter by query params
        """
        queryset = Movie.objects.all()
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(
                shows__theater__city__slug=city
            ).distinct()
        return queryset

    def perform_create(self, serializer):
        """
        Custom logic before saving
        """
        serializer.save(created_by=self.request.user)
```

### Pros and Cons

✅ **Pros:**
- Minimal code
- Standard CRUD patterns handled automatically
- Easy to customize via hooks (`get_queryset`, `perform_create`)
- Built-in pagination, filtering, permissions

❌ **Cons:**
- Less flexible than APIView
- Can be confusing for complex logic
- Multiple inheritance can be hard to debug

### When to Use Generic Views?

- Standard **CRUD operations** on a model
- Need **quick prototyping**
- Want **DRY code** with customization hooks

---

## ViewSets

**ViewSets** combine logic for multiple related views into a **single class**.

### ModelViewSet - The Most Powerful

```python
from rest_framework.viewsets import ModelViewSet

class CityViewSet(ModelViewSet):
    """
    A ViewSet for viewing and editing cities.
    Automatically provides:
    - list()    -> GET /cities/
    - create()  -> POST /cities/
    - retrieve() -> GET /cities/{pk}/
    - update()  -> PUT /cities/{pk}/
    - partial_update() -> PATCH /cities/{pk}/
    - destroy() -> DELETE /cities/{pk}/
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'slug'  # Use slug instead of pk
```

### Router - Automatic URL Generation

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='city')

urlpatterns = [
    path('api/', include(router.urls)),
]
```

**Generated URLs:**
```
GET    /api/cities/          -> list()
POST   /api/cities/          -> create()
GET    /api/cities/{slug}/   -> retrieve()
PUT    /api/cities/{slug}/   -> update()
PATCH  /api/cities/{slug}/   -> partial_update()
DELETE /api/cities/{slug}/   -> destroy()
```

### Custom Actions with @action

```python
from rest_framework.decorators import action
from rest_framework.response import Response

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=True, methods=['get'])
    def shows(self, request, pk=None):
        """
        GET /api/movies/{pk}/shows/
        Custom endpoint to get all shows for a movie
        """
        movie = self.get_object()
        city = request.query_params.get('city')
        date = request.query_params.get('date')

        shows = Show.objects.filter(movie=movie)
        if city:
            shows = shows.filter(theater__city__slug=city)
        if date:
            shows = shows.filter(start_time__date=date)

        serializer = ShowSerializer(shows, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        GET /api/movies/search/?query=avengers
        Custom endpoint for searching movies
        """
        query = request.query_params.get('query', '')
        movies = Movie.objects.filter(name__icontains=query)
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)
```

**Generated URLs:**
```
GET /api/movies/{pk}/shows/    -> shows action (detail=True)
GET /api/movies/search/         -> search action (detail=False)
```

### ReadOnlyModelViewSet

For **read-only** resources:

```python
from rest_framework.viewsets import ReadOnlyModelViewSet

class CityViewSet(ReadOnlyModelViewSet):
    """
    Only provides:
    - list()     -> GET /cities/
    - retrieve() -> GET /cities/{pk}/

    No create, update, or delete
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
```

### ViewSet Types

| ViewSet | Provides | Use Case |
|---------|----------|----------|
| `ViewSet` | Empty (define all actions manually) | Full custom control |
| `GenericViewSet` | Base + mixins | Pick specific actions |
| `ReadOnlyModelViewSet` | list, retrieve | Read-only resources |
| `ModelViewSet` | Full CRUD | Standard editable resources |

### Mixing in Actions with GenericViewSet

```python
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

class CityViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    Only list and retrieve, no create/update/delete
    More explicit than ReadOnlyModelViewSet
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
```

**Available Mixins:**
- `CreateModelMixin` - POST
- `ListModelMixin` - GET (list)
- `RetrieveModelMixin` - GET (detail)
- `UpdateModelMixin` - PUT, PATCH
- `DestroyModelMixin` - DELETE

### Pros and Cons

✅ **Pros:**
- **Minimal code** for full CRUD
- **Automatic routing** (no URL patterns!)
- **Custom actions** via `@action` decorator
- **Consistent structure** across codebase
- **Easy to extend** with mixins

❌ **Cons:**
- **Less explicit** (URLs auto-generated)
- **Harder to debug** for beginners
- **Overkill** for simple endpoints
- **Router magic** can be confusing

### When to Use ViewSets?

- **Standard resources** with CRUD operations (Cities, Movies, Theaters)
- **Related actions** on same resource (Movie → shows, reviews, ratings)
- Want **automatic routing**
- Building **consistent RESTful APIs**

---

## When to Use What?

### Decision Tree

```
Does this endpoint fit standard CRUD?
│
├─ NO → Use Function-Based View or APIView
│        Examples: /book/, /validate-coupon/, /health/
│
└─ YES → Is it a single resource with related actions?
         │
         ├─ YES → Use ViewSet
         │        Examples: Movies (with /shows/, /reviews/)
         │
         └─ NO → Are there multiple unrelated endpoints?
                  │
                  ├─ YES → Use Generic Views
                  │        Examples: /cities/, /theaters/
                  │
                  └─ NO → Use ViewSet for consistency
```

### Comparison Table

| Feature | FBV | APIView | Generic View | ViewSet |
|---------|-----|---------|--------------|---------|
| **Code Size** | Most | More | Less | Least |
| **Flexibility** | Full | Full | Medium | Medium |
| **Learning Curve** | Easy | Easy | Medium | Hard |
| **Boilerplate** | High | Medium | Low | Lowest |
| **Custom Logic** | Easy | Easy | Hooks | Actions |
| **URL Patterns** | Manual | Manual | Manual | Auto |
| **Best For** | Custom | Complex | Standard CRUD | Resources |

### Recommendation by Use Case

| Use Case | Recommended Approach | Example |
|----------|---------------------|---------|
| Standard CRUD resource | **ViewSet** | Cities, Movies, Theaters |
| Read-only resource | **ReadOnlyModelViewSet** | Static content, configurations |
| Custom business logic | **Function-Based View** | Book tickets, validate coupon |
| Complex filtering | **Generic View** | Search with many filters |
| Multiple related actions | **ViewSet + @action** | Movie (shows, reviews, ratings) |
| Non-resource endpoint | **Function-Based View** | Health check, stats |
| Quick prototype | **ModelViewSet** | Any CRUD resource |

---

## Real Examples from BookMyShow

### Example 1: City (ViewSet - Read-Only)

```python
class CityViewSet(ReadOnlyModelViewSet):
    """
    Cities are managed by admins, users can only view
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'slug'
```

**Why?**
- Users don't create/update cities
- Simple, clean, automatic routing
- Consistent with other resources

### Example 2: Movie (ViewSet with Custom Actions)

```python
class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def shows(self, request, slug=None):
        """
        GET /api/movies/{slug}/shows/?city=mumbai&date=2024-12-15
        """
        movie = self.get_object()
        city = request.query_params.get('city')
        date = request.query_params.get('date')

        shows = Show.objects.filter(movie=movie)
        if city:
            shows = shows.filter(theater__city__slug=city)
        if date:
            shows = shows.filter(start_time__date=date)

        serializer = ShowSerializer(shows, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        GET /api/movies/search/?query=avengers&city=mumbai
        """
        query = request.query_params.get('query', '')
        city = request.query_params.get('city')

        movies = Movie.objects.filter(name__icontains=query)
        if city:
            movies = movies.filter(
                shows__theater__city__slug=city
            ).distinct()

        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)
```

**Why?**
- Movie is a standard resource (CRUD)
- Related actions (shows, search) belong to same resource
- ViewSet keeps everything organized

### Example 3: Booking (Function-Based View)

```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_tickets(request):
    """
    POST /api/book/
    Custom booking logic with concurrency control
    """
    serializer = BookingRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    # Get the appropriate service based on settings
    service = get_booking_service()

    try:
        ticket = service.book_tickets(
            user=request.user,
            show_id=serializer.validated_data['show_id'],
            seat_ids=serializer.validated_data['seat_ids'],
            payment_mode=serializer.validated_data['payment_mode'],
            coupon_code=serializer.validated_data.get('coupon_code')
        )

        return Response(
            TicketSerializer(ticket).data,
            status=status.HTTP_201_CREATED
        )

    except SeatNotAvailableException as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except OptimisticLockException as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_409_CONFLICT
        )
```

**Why?**
- Booking is not CRUD on a single resource
- Complex business logic (concurrency, payment, validation)
- Doesn't fit ViewSet pattern
- Function is more readable for custom logic

### Example 4: Show (ViewSet with Custom Queryset)

```python
class ShowViewSet(ReadOnlyModelViewSet):
    serializer_class = ShowSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """
        Filter by movie, theater, date
        """
        queryset = Show.objects.select_related(
            'movie', 'screen__theater__city'
        ).all()

        movie = self.request.query_params.get('movie')
        theater = self.request.query_params.get('theater')
        date = self.request.query_params.get('date')

        if movie:
            queryset = queryset.filter(movie__slug=movie)
        if theater:
            queryset = queryset.filter(screen__theater__slug=theater)
        if date:
            queryset = queryset.filter(start_time__date=date)

        return queryset

    @action(detail=True, methods=['get'])
    def available_seats(self, request, id=None):
        """
        GET /api/shows/{id}/available_seats/
        """
        show = self.get_object()
        available = ShowSeat.objects.filter(
            show=show,
            status=SeatStatus.AVAILABLE
        ).select_related('seat')

        serializer = ShowSeatSerializer(available, many=True)
        return Response(serializer.data)
```

**Why?**
- Shows are read-only for users
- Need custom filtering logic
- Custom action for available seats
- ViewSet keeps it organized

---

## Best Practices

### 1. Use Appropriate Serializers

```python
class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        """
        Use different serializers for different actions
        """
        if self.action == 'list':
            return MovieListSerializer  # Minimal fields
        elif self.action == 'retrieve':
            return MovieDetailSerializer  # All fields
        return MovieSerializer  # Default
```

### 2. Optimize Queries

```python
class TheaterViewSet(ReadOnlyModelViewSet):
    serializer_class = TheaterSerializer

    def get_queryset(self):
        """
        Avoid N+1 queries with select_related
        """
        return Theater.objects.select_related('city').prefetch_related('screens')
```

### 3. Add Permissions

```python
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Anyone can view (GET)
    # Only authenticated users can create/update/delete
```

### 4. Add Pagination

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# Automatically applies to all ViewSets!
```

### 5. Add Filtering

```python
from django_filters.rest_framework import DjangoFilterBackend

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'language', 'rating']

# GET /api/movies/?category=Action&language=English
```

### 6. Handle Errors Gracefully

```python
from rest_framework.exceptions import ValidationError

class BookingViewSet(ModelViewSet):
    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except SeatNotAvailableException as e:
            raise ValidationError({"seats": str(e)})
```

### 7. Use Throttling

```python
from rest_framework.throttling import UserRateThrottle

class BookingRateThrottle(UserRateThrottle):
    rate = '10/hour'  # Max 10 bookings per hour

class BookingView(APIView):
    throttle_classes = [BookingRateThrottle]
```

### 8. Document with Docstrings

```python
class MovieViewSet(ModelViewSet):
    """
    API endpoint for managing movies.

    list: Return all movies with optional filtering
    retrieve: Return a single movie by slug
    create: Create a new movie (admin only)
    update: Update a movie (admin only)
    destroy: Delete a movie (admin only)
    """
    pass
```

---

## Interview Questions

### Q1: What's the difference between APIView and ViewSet?

**Answer:**

**APIView:**
- Base class for creating API endpoints
- Define HTTP methods explicitly (get, post, put, delete)
- Manual URL routing
- Good for custom logic

**ViewSet:**
- Combines multiple related views into one class
- Defines actions (list, create, retrieve, update, destroy)
- Automatic URL routing via Router
- Good for standard CRUD operations

**Example:**

```python
# APIView - Manual routing
class MovieList(APIView):
    def get(self, request):
        ...
    def post(self, request):
        ...

# URL
path('movies/', MovieList.as_view())

# ViewSet - Automatic routing
class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

# Router generates URLs automatically
router.register(r'movies', MovieViewSet)
```

### Q2: When would you use a Function-Based View over a ViewSet?

**Answer:**

Use **Function-Based Views** when:
1. **Custom business logic** that doesn't fit CRUD pattern
2. **One-off endpoints** (health check, webhooks)
3. **Complex operations** involving multiple models
4. **Non-resource-based APIs**

**Example from BookMyShow:**

```python
@api_view(['POST'])
def book_tickets(request):
    """
    Booking involves:
    - Validating seats
    - Checking availability (with locks)
    - Applying coupons
    - Creating ticket
    - Creating payment
    - Sending confirmation

    This doesn't fit ModelViewSet pattern!
    """
    ...
```

### Q3: Explain the @action decorator in ViewSets

**Answer:**

`@action` adds **custom endpoints** to a ViewSet beyond standard CRUD.

**Parameters:**
- `detail=True`: Operates on a single object (`/movies/{pk}/shows/`)
- `detail=False`: Operates on collection (`/movies/search/`)
- `methods`: HTTP methods allowed (`['get', 'post']`)

**Example:**

```python
class MovieViewSet(ModelViewSet):
    @action(detail=True, methods=['get'])
    def shows(self, request, pk=None):
        """
        GET /api/movies/{pk}/shows/
        """
        movie = self.get_object()
        shows = Show.objects.filter(movie=movie)
        return Response(ShowSerializer(shows, many=True).data)

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        """
        GET /api/movies/top_rated/
        """
        movies = Movie.objects.filter(rating__gte=8.0)
        return Response(self.get_serializer(movies, many=True).data)
```

### Q4: How do you optimize queries in ViewSets?

**Answer:**

**1. Override get_queryset() with select_related/prefetch_related:**

```python
class TheaterViewSet(ModelViewSet):
    serializer_class = TheaterSerializer

    def get_queryset(self):
        return Theater.objects.select_related('city').prefetch_related('screens')
```

**2. Use different serializers for list vs detail:**

```python
def get_serializer_class(self):
    if self.action == 'list':
        return TheaterListSerializer  # Only id, name
    return TheaterDetailSerializer  # All fields + screens
```

**3. Add pagination:**

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
```

### Q5: What are mixins in DRF?

**Answer:**

**Mixins** are small, reusable classes that provide specific CRUD functionality.

**Available Mixins:**
- `CreateModelMixin` - create()
- `ListModelMixin` - list()
- `RetrieveModelMixin` - retrieve()
- `UpdateModelMixin` - update(), partial_update()
- `DestroyModelMixin` - destroy()

**Use Case:** When you want only specific actions, not full CRUD.

**Example:**

```python
from rest_framework import mixins, viewsets

class CityViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    Provides only:
    - list()     -> GET /cities/
    - retrieve() -> GET /cities/{pk}/

    No create, update, or delete
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
```

This is equivalent to `ReadOnlyModelViewSet` but more explicit.

### Q6: How do you handle different serializers for different actions?

**Answer:**

Override `get_serializer_class()`:

```python
class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            # Minimal fields for listing
            return MovieListSerializer

        elif self.action == 'retrieve':
            # Full details for single movie
            return MovieDetailSerializer

        elif self.action in ['create', 'update']:
            # Write serializer (different validation)
            return MovieWriteSerializer

        return MovieSerializer  # Default
```

**Different Serializers:**

```python
class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'rating', 'category']

class MovieDetailSerializer(serializers.ModelSerializer):
    shows = ShowSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'

class MovieWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['name', 'description', 'rating', 'category']
        # No 'id' or 'shows' - write only
```

### Q7: What's the difference between Router and manually defining URLs?

**Answer:**

**With Router (ViewSet):**

```python
# urls.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'movies', MovieViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

**Generated URLs:**
```
GET    /api/movies/           -> list
POST   /api/movies/           -> create
GET    /api/movies/{pk}/      -> retrieve
PUT    /api/movies/{pk}/      -> update
PATCH  /api/movies/{pk}/      -> partial_update
DELETE /api/movies/{pk}/      -> destroy
```

**Manual URLs (Generic Views):**

```python
# views.py
class MovieList(ListCreateAPIView):
    ...

class MovieDetail(RetrieveUpdateDestroyAPIView):
    ...

# urls.py
urlpatterns = [
    path('movies/', MovieList.as_view()),
    path('movies/<int:pk>/', MovieDetail.as_view()),
]
```

**Trade-offs:**

| Aspect | Router | Manual URLs |
|--------|--------|-------------|
| Code | Less | More |
| Clarity | Auto-generated (less obvious) | Explicit |
| Flexibility | Medium | High |
| Best for | Standard resources | Custom endpoints |

---

## Summary

### Quick Reference

| Need | Use This |
|------|----------|
| Full CRUD on resource | `ModelViewSet` |
| Read-only resource | `ReadOnlyModelViewSet` |
| Custom business logic | Function-Based View (`@api_view`) |
| Standard CRUD + custom actions | `ViewSet` + `@action` |
| Only some CRUD operations | Generic Views or Mixins |
| Complete custom control | `APIView` |
| Quick prototype | `ModelViewSet` + Router |

### Progression for Learning

1. **Start with Function-Based Views** - Understand basics
2. **Move to APIView** - Learn class-based structure
3. **Use Generic Views** - Reduce boilerplate for CRUD
4. **Master ViewSets** - Professional Django REST APIs
5. **Mix and Match** - Choose right tool for each endpoint

### Interview Talking Points

✅ **Know the trade-offs**: Less code vs more control
✅ **Understand routing**: Manual vs automatic
✅ **Query optimization**: select_related, prefetch_related
✅ **Different serializers**: List vs detail vs write
✅ **Custom actions**: @action decorator
✅ **Permissions**: Who can access what
✅ **When to use what**: Decision criteria

---

## Related Files

- `bookmyshow/booking/views.py` - Real implementation examples
- `bookmyshow/booking/serializers.py` - Serializers used in views
- `bookmyshow/urls.py` - URL configuration with router
- `guides/05_API_DOCUMENTATION.md` - API endpoint documentation

---

**Practice Exercise:**

Try implementing the same endpoint in **three different ways**:

1. **Function-Based View**
2. **Generic View (ListCreateAPIView)**
3. **ViewSet**

Compare code length, readability, and flexibility!

---

Happy coding! 🚀
