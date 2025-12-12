# Architecture and Data Flow Guide for LLD Interviews

## Table of Contents
1. [Overall Architecture](#overall-architecture)
2. [Django MVT vs MVC](#django-mvt-vs-mvc)
3. [Layer Architecture](#layer-architecture)
4. [Data Flow](#data-flow)
5. [Request-Response Cycle](#request-response-cycle)
6. [Database Flow](#database-flow)

---

## Overall Architecture

### System Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                         CLIENT (Browser/Mobile)                │
└────────────────────────────┬───────────────────────────────────┘
                             │ HTTP Request (JSON)
                             ▼
┌────────────────────────────────────────────────────────────────┐
│                          WEB SERVER                            │
│                     (Django / Gunicorn)                        │
└────────────────────────────┬───────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────┐
│                        URL DISPATCHER                          │
│                      (urls.py)                                 │
│   /api/movies/  ──→  MovieViewSet                             │
│   /api/book/    ──→  book_tickets                             │
└────────────────────────────┬───────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────┐
│                          VIEW LAYER                            │
│                    (views.py - Controller)                     │
│   • Receive HTTP request                                       │
│   • Extract & validate data                                    │
│   • Call service layer                                         │
│   • Return HTTP response                                       │
└────────────────────────────┬───────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────┐
│                       SERIALIZER LAYER                         │
│                    (serializers.py - DTO)                      │
│   • Validate request data                                      │
│   • Convert JSON ↔ Python objects                             │
│   • Field-level validation                                     │
└────────────────────────────┬───────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────┐
│                        SERVICE LAYER                           │
│                  (services/*.py - Business Logic)              │
│   • Business rules                                             │
│   • Concurrency control                                        │
│   • Complex operations                                         │
│   • Transactions                                               │
└────────────────────────────┬───────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────┐
│                         MODEL LAYER                            │
│                    (models.py - ORM)                           │
│   • Database schema                                            │
│   • Relationships                                              │
│   • Simple business logic                                      │
└────────────────────────────┬───────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────┐
│                          DATABASE                              │
│                        (SQLite/PostgreSQL)                     │
└────────────────────────────────────────────────────────────────┘
```

---

## Django MVT vs MVC

### Traditional MVC (Model-View-Controller)

```
┌──────────┐      ┌────────────┐      ┌───────┐
│  Model   │ ◄────│ Controller │◄─────│ View  │
│ (Data)   │      │ (Logic)    │      │ (UI)  │
└──────────┘      └────────────┘      └───────┘
     │                  │
     │                  │
     ▼                  ▼
  Database           Business
                      Logic
```

**MVC Components**:
- **Model**: Data structure and database
- **View**: User interface (HTML/Templates)
- **Controller**: Business logic and flow

### Django MVT (Model-View-Template)

```
┌──────────┐      ┌───────┐      ┌──────────┐
│  Model   │◄─────│ View  │──────│ Template │
│ (Data)   │      │(Logic)│      │  (UI)    │
└──────────┘      └───────┘      └──────────┘
     │               │
     │               │
     ▼               ▼
  Database      Business
                 Logic
```

**MVT Components**:
- **Model**: Same as MVC
- **View**: Acts like Controller (handles logic)
- **Template**: Acts like View (presents data)

### REST API (Our Case) - No Templates

```
┌──────────┐      ┌──────────┐      ┌──────────────┐
│  Model   │◄─────│   View   │──────│ Serializer   │
│ (Data)   │      │(Controller)     │ (JSON DTO)   │
└──────────┘      └──────────┘      └──────────────┘
     │               │                     │
     ▼               ▼                     ▼
  Database      Business              JSON
                 Logic              Response
```

**Our Layers**:
- **Model**: Database schema (models.py)
- **View**: HTTP controller (views.py)
- **Serializer**: JSON ↔ Python converter
- **Service**: Business logic (services/*.py)

### Interview Mapping

| Traditional MVC | Django (Web) | Our REST API | Purpose |
|----------------|--------------|--------------|---------|
| Model          | Model        | Model        | Database/Data |
| Controller     | View         | View         | Request handling |
| View           | Template     | Serializer   | Presentation |
| -              | -            | Service      | Business logic |

**Interview Question**: *Where does Django View fit in MVC?*

**Answer**: Django View = MVC Controller. It handles requests and coordinates flow. In our REST API, Views use Serializers (not Templates) for data presentation.

---

## Layer Architecture

### Layer Responsibilities

```
┌─────────────────────────────────────────────────────────────┐
│ VIEW LAYER (views.py)                                        │
│ ──────────────────────────────────────────────────────────  │
│ ✓ HTTP request/response                                      │
│ ✓ Authentication/Authorization                               │
│ ✓ Call serializers                                           │
│ ✓ Call services                                              │
│ ✗ Business logic (goes in service!)                         │
│ ✗ Direct database queries (use service!)                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ SERIALIZER LAYER (serializers.py)                           │
│ ──────────────────────────────────────────────────────────  │
│ ✓ Input validation                                           │
│ ✓ Data format conversion (JSON ↔ Python)                   │
│ ✓ Field-level rules                                          │
│ ✓ Nested object handling                                     │
│ ✗ Complex business logic (goes in service!)                 │
│ ✗ Database transactions (use service!)                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ SERVICE LAYER (services/*.py)                               │
│ ──────────────────────────────────────────────────────────  │
│ ✓ Business logic                                             │
│ ✓ Transactions                                               │
│ ✓ Concurrency control                                        │
│ ✓ Complex queries                                            │
│ ✓ Cross-model operations                                     │
│ ✗ HTTP concerns (stays in view!)                            │
│ ✗ JSON serialization (use serializer!)                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ MODEL LAYER (models.py)                                     │
│ ──────────────────────────────────────────────────────────  │
│ ✓ Database schema                                            │
│ ✓ Relationships                                              │
│ ✓ Simple properties (@property)                             │
│ ✓ Model-specific validation                                 │
│ ✗ Complex business logic (use service!)                     │
│ ✗ Cross-model operations (use service!)                     │
└─────────────────────────────────────────────────────────────┘
```

### Example: Booking Flow Through Layers

```python
# ━━━━━━━━━━ VIEW LAYER ━━━━━━━━━━
# views.py
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_tickets(request):
    # 1. Validate input (serializer)
    serializer = BookingRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    # 2. Call service (business logic)
    try:
        result = BookingService().book_tickets(
            user=request.user,
            show_id=serializer.validated_data['show_id'],
            seat_ids=serializer.validated_data['seat_ids'],
            payment_mode=serializer.validated_data['payment_mode']
        )

        # 3. Serialize response
        ticket_serializer = TicketSerializer(result['ticket'])
        return Response(ticket_serializer.data, status=201)

    except ValueError as e:
        return Response({'error': str(e)}, status=400)


# ━━━━━━━━━━ SERIALIZER LAYER ━━━━━━━━━━
# serializers.py
class BookingRequestSerializer(serializers.Serializer):
    show_id = serializers.CharField()
    seat_ids = serializers.ListField(child=serializers.CharField())
    payment_mode = serializers.ChoiceField(choices=PaymentMode.choices)

    def validate_seat_ids(self, value):
        # Field validation
        if len(value) > 10:
            raise serializers.ValidationError("Max 10 seats per booking")
        return value


# ━━━━━━━━━━ SERVICE LAYER ━━━━━━━━━━
# services/booking_service.py
class BookingService:
    @transaction.atomic
    def book_tickets(self, user, show_id, seat_ids, payment_mode):
        # Business logic here
        # 1. Concurrency control
        seats = ShowSeat.objects.select_for_update().filter(
            id__in=seat_ids,
            show_id=show_id
        )

        # 2. Availability check
        if seats.filter(status='AVAILABLE').count() != len(seat_ids):
            raise ValueError("Seats not available")

        # 3. Create ticket
        ticket = Ticket.objects.create(...)

        # 4. Create payment
        payment = Payment.objects.create(...)

        return {'ticket': ticket, 'payment': payment}


# ━━━━━━━━━━ MODEL LAYER ━━━━━━━━━━
# models.py
class ShowSeat(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Simple property
    @property
    def is_available(self):
        return self.status == SeatStatus.AVAILABLE
```

---

## Data Flow

### Request Flow (POST /api/book/)

```
1. HTTP Request
   ↓
   POST /api/book/
   Headers: {Authorization: Bearer token}
   Body: {
     "show_id": "SHOW-123",
     "seat_ids": ["SEAT-1", "SEAT-2"],
     "payment_mode": "UPI"
   }

2. URL Dispatcher (urls.py)
   ↓
   path('book/', views.book_tickets)

3. View (views.py)
   ↓
   • Extract user from request.user (authentication middleware)
   • Pass data to serializer

4. Serializer (serializers.py)
   ↓
   BookingRequestSerializer(data=request.data)
   • Validate field types
   • Call validate_seat_ids()
   • Call validate()
   • Return validated_data = {
       'show_id': 'SHOW-123',
       'seat_ids': ['SEAT-1', 'SEAT-2'],
       'payment_mode': 'UPI'
     }

5. Service (services/booking_service.py)
   ↓
   BookingService().book_tickets(...)
   • Start transaction
   • Lock seats (SELECT FOR UPDATE)
   • Validate availability
   • Create ticket
   • Create payment
   • Commit transaction
   • Return {'ticket': ticket, 'payment': payment}

6. Model (models.py)
   ↓
   • ORM translates to SQL
   • Execute queries:
     SELECT * FROM show_seat WHERE id IN (...) FOR UPDATE;
     INSERT INTO ticket (...) VALUES (...);
     INSERT INTO payment (...) VALUES (...);

7. Database
   ↓
   • Execute SQL
   • Return results

8. Response Flow (Reverse)
   ↓
   Service → View → Serializer → JSON

9. HTTP Response
   ↓
   Status: 201 Created
   Body: {
     "ticket": {
       "id": "TKT-123",
       "movie_name": "Avengers",
       "amount": 500.00,
       ...
     }
   }
```

### Visual Data Transformation

```
JSON Request
    ↓
  Python Dict {"show_id": "SHOW-123", ...}
    ↓
[SERIALIZER VALIDATION]
    ↓
  Validated Python Dict
    ↓
[SERVICE LAYER]
    ↓
  Django Model Objects (Ticket, Payment)
    ↓
[ORM]
    ↓
  SQL Statements
    ↓
[DATABASE]
    ↓
  Database Rows
    ↓
[ORM]
    ↓
  Model Instances
    ↓
[SERIALIZER]
    ↓
  Python Dict
    ↓
  JSON Response
```

---

## Request-Response Cycle

### Complete Cycle

```
┌──────────────────────────────────────────────────────────────┐
│  CLIENT                                                       │
│  POST /api/book/ {"show_id": "123", "seat_ids": ["5", "6"]} │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│  MIDDLEWARE STACK                                             │
│  1. SecurityMiddleware                                        │
│  2. SessionMiddleware                                         │
│  3. AuthenticationMiddleware ──► request.user = User(...)    │
│  4. CsrfViewMiddleware                                        │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│  URL ROUTING                                                  │
│  urls.py: path('book/', views.book_tickets)                  │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│  VIEW                                                         │
│  1. Check permissions (@permission_classes)                   │
│  2. Extract data (request.data)                              │
│  3. Validate (serializer.is_valid())                         │
│  4. Execute (service.book_tickets())                         │
│  5. Serialize response (TicketSerializer)                    │
│  6. Return Response(data, status=201)                        │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│  RESPONSE                                                     │
│  Status: 201 Created                                          │
│  Headers: {Content-Type: application/json}                   │
│  Body: {"ticket": {...}}                                     │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│  CLIENT                                                       │
│  Receives JSON response                                       │
└──────────────────────────────────────────────────────────────┘
```

---

## Database Flow

### ORM Translation

```python
# Python Code
ShowSeat.objects.select_for_update().filter(
    show_id='SHOW-123',
    id__in=['SEAT-1', 'SEAT-2']
)

# ↓ Django ORM translates to ↓

# SQL
SELECT *
FROM show_seat
WHERE show_id = 'SHOW-123'
  AND id IN ('SEAT-1', 'SEAT-2')
FOR UPDATE;

# ↓ Database executes ↓

# Result: List of ShowSeat objects
[<ShowSeat: SEAT-1>, <ShowSeat: SEAT-2>]
```

### Transaction Flow

```python
# Python
@transaction.atomic
def book_tickets(...):
    # Query 1: Lock seats
    seats = ShowSeat.objects.select_for_update().filter(...)

    # Query 2: Create ticket
    ticket = Ticket.objects.create(...)

    # Query 3: Create ticket seats
    TicketSeat.objects.bulk_create([...])

    # Query 4: Create payment
    payment = Payment.objects.create(...)

# ↓ Translates to ↓

BEGIN TRANSACTION;

    SELECT * FROM show_seat WHERE ... FOR UPDATE;

    INSERT INTO ticket (...) VALUES (...);

    INSERT INTO ticket_seat (...) VALUES (...), (...);

    INSERT INTO payment (...) VALUES (...);

COMMIT;  -- If no errors
-- OR --
ROLLBACK;  -- If any error
```

---

## Interview Questions

### Q1: Explain Django's MVT pattern.

**Answer**: Django uses Model-View-Template (MVT):
- **Model**: Database layer (ORM)
- **View**: Business logic (like MVC's Controller)
- **Template**: Presentation (like MVC's View)

In our REST API, Template is replaced by Serializers (JSON responses).

### Q2: What's the purpose of the service layer?

**Answer**: Separates business logic from HTTP concerns:
- Views handle HTTP (request/response)
- Services handle business logic (transactions, concurrency)
- Makes code reusable and testable
- Follows Single Responsibility Principle

### Q3: Why use serializers instead of direct JSON?

**Answer**: Serializers provide:
- **Validation**: Ensure data integrity
- **Type conversion**: JSON → Python objects
- **Nested relationships**: Handle related objects
- **Reusability**: Same serializer for multiple endpoints

### Q4: Explain the complete flow of a booking request.

**Answer**:
1. Client sends POST /api/book/ with JSON
2. Django middleware processes (auth, CSRF, etc.)
3. URL dispatcher routes to view
4. View validates with serializer
5. Service layer executes business logic with transaction
6. ORM translates to SQL and executes
7. Response serialized and returned as JSON

### Q5: Where should you put business logic?

**Answer**: **Service layer**. Not in:
- Models (simple properties only)
- Views (HTTP handling only)
- Serializers (validation only)

### Q6: What happens in a database transaction?

**Answer**: Groups multiple queries into atomic unit:
- All succeed → COMMIT
- Any fails → ROLLBACK (undo all)
- Ensures data consistency

---

## Summary

### Architecture Layers (Top to Bottom)

1. **Client** → Sends HTTP requests
2. **URL Dispatcher** → Routes to correct view
3. **View** → HTTP controller
4. **Serializer** → Validates and converts data
5. **Service** → Business logic
6. **Model** → Database abstraction
7. **Database** → Persists data

### Key Principles

- **Separation of Concerns**: Each layer has specific responsibility
- **Thin Views, Fat Services**: Business logic in services
- **DRY**: Serializers and services are reusable
- **Single Responsibility**: Each layer does one thing well

### Data Transformations

```
JSON → Dict → Validated Dict → Model Objects → SQL → Database Rows
                                                      ↓
JSON ← Dict ← Serialized Dict ← Model Objects ← SQL ← Database Rows
```

**Master this flow - it's critical for understanding full-stack development and LLD interviews!**
