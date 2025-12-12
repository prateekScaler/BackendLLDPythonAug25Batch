# Django REST Framework Serializers Guide for LLD Interviews

## Table of Contents
1. [What are Serializers?](#what-are-serializers)
2. [Serializer vs ModelSerializer](#serializer-vs-modelserializer)
3. [Serialization Flow](#serialization-flow)
4. [Nested Serializers](#nested-serializers)
5. [Validation](#validation)
6. [Interview Gotchas](#interview-gotchas)
7. [Best Practices](#best-practices)

---

## What are Serializers?

### Purpose
Serializers convert between complex data types (Models, QuerySets) and native Python datatypes (dict, list) that can be rendered to JSON/XML.

### Two-way Conversion

```
Python Object  ←──→  Serializer  ←──→  JSON
(Model)              (Validation)      (API Response)
```

**Serialization** (Object → JSON):
```python
movie = Movie.objects.get(id=1)
serializer = MovieSerializer(movie)
json_data = serializer.data
# {'id': 1, 'name': 'Avengers', 'rating': 8.5}
```

**Deserialization** (JSON → Object):
```python
data = {'name': 'Iron Man', 'rating': 8.0}
serializer = MovieSerializer(data=data)
if serializer.is_valid():
    movie = serializer.save()  # Creates Movie object
```

---

## Serializer vs ModelSerializer

### 1. Basic Serializer

**Use when**: Working with non-model data or need full control.

```python
from rest_framework import serializers

class BookingRequestSerializer(serializers.Serializer):
    show_id = serializers.CharField()
    seat_ids = serializers.ListField(child=serializers.CharField())
    payment_mode = serializers.ChoiceField(choices=PaymentMode.choices)

    def validate_seat_ids(self, value):
        """Field-level validation"""
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Duplicate seat IDs")
        return value

    def validate(self, data):
        """Object-level validation"""
        # Cross-field validation logic
        return data
```

**Pros**:
- Full control over fields
- No model dependency
- Good for request/response DTOs

**Cons**:
- Manual field definition
- No auto-save() method

### 2. ModelSerializer

**Use when**: Working with Django models (90% of cases).

```python
from rest_framework import serializers

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'rating', 'category', 'duration']
        read_only_fields = ['id']  # Can't be modified
```

**Auto-generates**:
- Field types from model fields
- Validators from model validators
- save() and create()/update() methods

**Interview Question**: *Why use ModelSerializer?*
- DRY principle (Don't Repeat Yourself)
- Automatic field type inference
- Built-in CRUD operations
- Less boilerplate code

---

## Serialization Flow

### Read Operation (Model → JSON)

```
Database Query → Model Instance → Serializer → Python Dict → JSON Response
```

**Example**:
```python
# Step 1: Query database
movie = Movie.objects.get(id=1)
# Movie(id=1, name='Avengers', rating=8.5)

# Step 2: Serialize
serializer = MovieSerializer(movie)

# Step 3: Get data
data = serializer.data
# OrderedDict([('id', 1), ('name', 'Avengers'), ('rating', 8.5)])

# Step 4: Return as JSON (in view)
return Response(data)
# {"id": 1, "name": "Avengers", "rating": 8.5}
```

### Write Operation (JSON → Model)

```
JSON Request → Python Dict → Serializer (Validation) → Model Instance → Database
```

**Example**:
```python
# Step 1: Receive JSON
request_data = {'name': 'Iron Man', 'rating': 8.0, 'duration': 126}

# Step 2: Deserialize
serializer = MovieSerializer(data=request_data)

# Step 3: Validate
if serializer.is_valid():
    # Step 4: Save to database
    movie = serializer.save()
else:
    # Return errors
    print(serializer.errors)
    # {'name': ['This field is required.']}
```

---

## Nested Serializers

### Problem: Related Data

```python
# Theater model has ForeignKey to City
theater = Theater.objects.get(id=1)

# Basic serializer - only shows city ID
class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = ['id', 'name', 'city']

# Output: {'id': 1, 'name': 'PVR', 'city': 5}  ← Just city ID!
```

### Solution 1: Read-only Nested Serializer

```python
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']

class TheaterSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)  # Nested!

    class Meta:
        model = Theater
        fields = ['id', 'name', 'city']

# Output:
# {
#     'id': 1,
#     'name': 'PVR',
#     'city': {'id': 5, 'name': 'Mumbai'}  ← Full city object!
# }
```

### Solution 2: source parameter

```python
class TheaterSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = Theater
        fields = ['id', 'name', 'city', 'city_name']

# Output:
# {
#     'id': 1,
#     'name': 'PVR',
#     'city': 5,
#     'city_name': 'Mumbai'
# }
```

### Solution 3: SerializerMethodField

```python
class TheaterSerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField()

    class Meta:
        model = Theater
        fields = ['id', 'name', 'city_name']

    def get_city_name(self, obj):
        """Method name must be get_<field_name>"""
        return obj.city.name if obj.city else None

# Output:
# {
#     'id': 1,
#     'name': 'PVR',
#     'city_name': 'Mumbai'
# }
```

### Reverse Relationships

```python
class CitySerializer(serializers.ModelSerializer):
    # Get all theaters in this city (reverse FK)
    theaters = TheaterSerializer(many=True, read_only=True)
    theater_count = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['id', 'name', 'theaters', 'theater_count']

    def get_theater_count(self, obj):
        return obj.theaters.count()

# Output:
# {
#     'id': 1,
#     'name': 'Mumbai',
#     'theaters': [
#         {'id': 1, 'name': 'PVR'},
#         {'id': 2, 'name': 'INOX'}
#     ],
#     'theater_count': 2
# }
```

### Interview Question: *Read vs Write Nested Serializers*

**Problem with writable nested serializers**:
```json
{
    "name": "PVR Andheri",
    "city": {
        "name": "Mumbai"  ← Should this create new city or link to existing?
    }
}
```

**Solution**: Different serializers for read and write!

```python
# Read Serializer (with nested data)
class TheaterReadSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = Theater
        fields = ['id', 'name', 'city']

# Write Serializer (accept city ID)
class TheaterWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = ['id', 'name', 'city']  # city is just an ID

# In View
class TheaterViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TheaterReadSerializer
        return TheaterWriteSerializer
```

---

## Validation

### 1. Field-level Validation

```python
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['name', 'rating', 'duration']

    def validate_rating(self, value):
        """
        Method name: validate_<field_name>
        Called automatically for the field
        """
        if value < 0 or value > 10:
            raise serializers.ValidationError("Rating must be between 0 and 10")
        return value  # MUST return value!

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be positive")
        return value
```

### 2. Object-level Validation

```python
class BookingSerializer(serializers.Serializer):
    show_id = serializers.CharField()
    seat_count = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        """
        Cross-field validation
        Has access to all fields
        """
        # Business rule: Max 10 seats per booking
        if data['seat_count'] > 10:
            raise serializers.ValidationError("Cannot book more than 10 seats")

        # Calculate expected amount
        expected_amount = data['seat_count'] * 100  # Assume $100 per seat
        if data['amount'] < expected_amount:
            raise serializers.ValidationError(
                f"Amount should be at least ${expected_amount}"
            )

        return data  # MUST return data!
```

### 3. Validators

```python
from rest_framework.validators import UniqueValidator

class MovieSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=200,
        validators=[
            UniqueValidator(queryset=Movie.objects.all()),
        ]
    )

    class Meta:
        model = Movie
        fields = ['name', 'rating']
```

### Custom Validators

```python
def validate_coupon_code(value):
    """Reusable validator function"""
    if not value.startswith('DISCOUNT'):
        raise serializers.ValidationError("Invalid coupon format")
    return value

class BookingSerializer(serializers.Serializer):
    coupon_code = serializers.CharField(
        validators=[validate_coupon_code]
    )
```

### Interview Question: *Validation Order*

1. Field type validation (built-in)
2. Field validators (validators=[...])
3. validate_<field_name>() methods
4. validate() method
5. Model validators (if ModelSerializer)

```python
# Execution order:
# 1. Check if 'rating' is a valid float
# 2. Check MinValueValidator, MaxValueValidator
# 3. Call validate_rating(value)
# 4. Call validate(data)
# 5. Check model validators
```

---

## Interview Gotchas

### 1. read_only vs write_only

```python
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Only in input
    full_name = serializers.CharField(source='get_full_name', read_only=True)  # Only in output

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'full_name']

# Input (can include password):
# {'username': 'john', 'password': 'secret123'}

# Output (includes full_name, excludes password):
# {'id': 1, 'username': 'john', 'full_name': 'John Doe'}
```

### 2. many=True

```python
# Single object
movie = Movie.objects.get(id=1)
serializer = MovieSerializer(movie)

# Multiple objects
movies = Movie.objects.all()
serializer = MovieSerializer(movies, many=True)  # ← Important!
```

### 3. context

```python
# In view:
serializer = MovieSerializer(movie, context={'request': request})

# In serializer:
class MovieSerializer(serializers.ModelSerializer):
    can_book = serializers.SerializerMethodField()

    def get_can_book(self, obj):
        request = self.context.get('request')
        user = request.user if request else None
        return user.is_authenticated  # Access user from context!
```

### 4. to_representation() and to_internal_value()

**Custom output format**:
```python
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'rating']

    def to_representation(self, instance):
        """Customize output"""
        data = super().to_representation(instance)
        data['rating_percentage'] = data['rating'] * 10  # Add computed field
        return data

# Output:
# {'id': 1, 'name': 'Avengers', 'rating': 8.5, 'rating_percentage': 85.0}
```

**Custom input parsing**:
```python
class MovieSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        """Customize input parsing"""
        # Convert rating percentage to rating
        if 'rating_percentage' in data:
            data['rating'] = data.pop('rating_percentage') / 10
        return super().to_internal_value(data)
```

---

## Best Practices

### 1. Use Different Serializers for Different Actions

```python
# List view - light weight
class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'rating']

# Detail view - comprehensive
class MovieDetailSerializer(serializers.ModelSerializer):
    shows = ShowSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'name', 'rating', 'description', 'shows']

# Write operations
class MovieWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['name', 'rating', 'description', 'duration']
```

### 2. Avoid Deep Nesting

**Bad** (performance nightmare):
```python
# Theater → Screen → Show → Movie → Actor → ...
# Results in tons of database queries!
```

**Good**:
```python
# Use separate endpoints:
# GET /theaters/{id}/  - Basic theater info
# GET /theaters/{id}/screens/  - Screens in theater
# GET /screens/{id}/shows/  - Shows in screen
```

### 3. Use select_related/prefetch_related in Views

```python
# In View, not Serializer!
class MovieViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Movie.objects.select_related('category').prefetch_related('actors')
```

### 4. Explicit is Better Than Implicit

```python
# Bad
class Meta:
    fields = '__all__'  # Don't do this!

# Good
class Meta:
    fields = ['id', 'name', 'rating']  # Explicit
```

---

## Common Interview Questions

### Q1: Serializer vs ModelSerializer?
- Serializer: Full control, no model dependency
- ModelSerializer: DRY, auto-generates fields from model

### Q2: How to handle nested writes?
- Use different serializers for read and write
- Or use `create()`/`update()` methods to handle nested data

### Q3: What's the difference between source and SerializerMethodField?
- **source**: Direct attribute access (`source='city.name'`)
- **SerializerMethodField**: Custom method with logic

### Q4: How to validate across multiple fields?
- Use `validate(self, data)` method (object-level validation)

### Q5: Performance optimization?
- Use different serializers for list vs detail
- Avoid deep nesting
- Use select_related/prefetch_related in views
- Cache serialized data if appropriate

### Q6: When to use to_representation()?
- Custom output formatting
- Conditional field inclusion
- Adding computed fields not in model

---

## Serialization Patterns in BookMyShow

### 1. Booking Request (Input DTO)

```python
class BookingRequestSerializer(serializers.Serializer):
    """Non-model serializer for request validation"""
    show_id = serializers.CharField()
    seat_ids = serializers.ListField(child=serializers.CharField())
    payment_mode = serializers.ChoiceField(choices=PaymentMode.choices)

    def validate(self, data):
        # Complex business validation
        return data
```

### 2. Movie Search Response

```python
class MovieSerializer(serializers.ModelSerializer):
    """Rich response with computed fields"""
    show_count = serializers.SerializerMethodField()
    languages_display = serializers.SerializerMethodField()

    def get_show_count(self, obj):
        return obj.shows.filter(start_time__gte=timezone.now()).count()
```

### 3. Ticket Details (Multiple Nested)

```python
class TicketSerializer(serializers.ModelSerializer):
    """Complex nested serializer for detailed view"""
    movie_name = serializers.CharField(source='show.movie.name', read_only=True)
    seats = TicketSeatSerializer(source='ticket_seats', many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)
```

---

## Summary

### Key Takeaways

1. **Serializers = JSON ↔ Python Objects converter**
2. **Use ModelSerializer for models, Serializer for DTOs**
3. **Different serializers for read vs write**
4. **Validation order**: Field → validate_field() → validate() → Model
5. **Nested serializers**: read_only for output, IDs for input
6. **Optimize**: Different serializers for list vs detail
7. **SerializerMethodField**: For computed/custom fields

Remember: **Serializers bridge the gap between your API and your models!**
