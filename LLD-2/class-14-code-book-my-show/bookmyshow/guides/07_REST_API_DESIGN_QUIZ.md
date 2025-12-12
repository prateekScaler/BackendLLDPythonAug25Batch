# REST API Design Quiz - BookMyShow

**Context**: You're designing REST APIs for a BookMyShow-like system. Focus on endpoint design, HTTP methods, payloads, and status codes.

**Instructions**: Try answering each question before expanding the solution. Think about RESTful principles and real-world scenarios.

---

## Section A: HTTP Methods & Resource Design

### Question 1: Booking Endpoint Design

You need to design an endpoint for users to book movie tickets. Which design is correct?

**Option A:**
```http
POST /api/bookings/create
{
  "user_id": 123,
  "show_id": 456,
  "seat_ids": [1, 2, 3]
}
```

**Option B:**
```http
POST /api/users/123/bookings
{
  "show_id": 456,
  "seat_ids": [1, 2, 3]
}
```

**Option C:**
```http
POST /api/bookings
{
  "show_id": 456,
  "seat_ids": [1, 2, 3]
}
```
---
<details>
<summary><strong>Answer</strong></summary>

**Correct: Option C**

**Explanation:**

1. **Option A is wrong:**
   - Avoid verbs in URLs (`/create`, `/delete`, `/update`)
   - HTTP methods already indicate the action
   - `user_id` shouldn't be in payload—use authentication token

2. **Option B is wrong:**
   - While nested resources can work, `/users/123/bookings` implies you're managing a user's bookings collection
   - User ID from token might not match URL parameter (security risk)
   - Overly nested URLs are harder to maintain

3. **Option C is correct:**
   - Clean, resource-oriented URL
   - HTTP POST clearly indicates creation
   - User identified via `Authorization: Bearer <token>` header
   - `user_id` extracted server-side from token
   
---
**Complete correct design:**
```http
POST /api/bookings
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "show_id": "show-123",
  "seat_ids": ["seat-1", "seat-2"],
  "payment_mode": "UPI",
  "coupon_code": "DISCOUNT50"
}
```

**Response (201 Created):**
```json
{
  "ticket_id": "TKT-789",
  "status": "CONFIRMED",
  "total_amount": 450.00,
  "seats": ["A1", "A2"],
  "show": {
    "id": "show-123",
    "movie": "Avengers",
    "theater": "PVR Mumbai",
    "start_time": "2024-12-15T18:00:00Z"
  }
}
```

**Key Principles:**
- Use nouns for resources, verbs for HTTP methods
- User context from authentication, not payload
- Return complete resource representation after creation
</details>

---

### Question 2: Idempotency Challenge

A user's payment succeeds, but their network drops before receiving the response. They retry the booking request with the same data. What should happen?

**Scenario:**
```http
POST /api/bookings
{
  "show_id": "show-123",
  "seat_ids": ["A1", "A2"],
  "payment_mode": "UPI"
}
```

**First attempt:** Payment succeeds, but client times out
**Second attempt:** User retries the exact same request

What's the correct API behavior?

---
<details>
<summary><strong>Answer</strong></summary>

**Correct Behavior: Return 409 Conflict or implement idempotency keys**

**Problem:**
POST is **not idempotent**—each call creates a new resource. Without safeguards:
- User might be charged twice
- Same seats booked multiple times (if seats weren't locked)
- Data inconsistency

**Solution 1: Idempotency Keys (Recommended)**

Client sends unique idempotency key:
```http
POST /api/bookings
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
{
  "show_id": "show-123",
  "seat_ids": ["A1", "A2"]
}
```
---
Server logic:
```python
def book_tickets(request):
    idempotency_key = request.headers.get('Idempotency-Key')

    # Check if this key was already processed
    existing_booking = Booking.objects.filter(
        idempotency_key=idempotency_key
    ).first()

    if existing_booking:
        # Return the same response as before (cached)
        return Response(
            serialize(existing_booking),
            status=200  # or 201, depends on design
        )

    # First time processing this request
    booking = create_booking(...)
    booking.idempotency_key = idempotency_key
    booking.save()

    return Response(serialize(booking), status=201)
```
---
**Solution 2: Natural Idempotency**

Check if booking already exists:
```python
def book_tickets(request):
    user = request.user
    show_id = request.data['show_id']
    seat_ids = request.data['seat_ids']

    # Check for duplicate booking (within short time window)
    recent_booking = Booking.objects.filter(
        user=user,
        show_id=show_id,
        seat_ids__overlap=seat_ids,
        created_at__gte=timezone.now() - timedelta(minutes=5)
    ).first()

    if recent_booking:
        return Response({
            "error": "DUPLICATE_BOOKING",
            "message": "You already booked these seats",
            "existing_booking_id": recent_booking.id
        }, status=409)
```
---
**Best Practice:**
- Always implement idempotency for payment-related endpoints
- Use `Idempotency-Key` header (popularized by Stripe)
- Store keys with expiration (e.g., 24 hours)
- Return same response for duplicate requests

**Status Codes:**
- `201 Created` - First successful booking
- `200 OK` - Returning existing booking (idempotent retry)
- `409 Conflict` - Duplicate detected, cannot proceed

</details>

---

### Question 3: Seat Availability Check

How should you design an endpoint to check seat availability for a show? Consider performance and consistency.

**Option A:**
```http
GET /api/shows/show-123/seats?status=available
```

**Option B:**
```http
POST /api/shows/show-123/check-availability
{
  "seat_ids": ["A1", "A2", "A3"]
}
```

**Option C:**
```http
GET /api/shows/show-123
(Returns full show details including all seats with their status)
```

---
<details>
<summary><strong>Answer</strong></summary>

**Correct: It depends on the use case!**

**For browsing/displaying seat map: Option A or C**

```http
GET /api/shows/show-123/seats?status=available
```

**Why:**
- Safe, cacheable (GET method)
- No side effects
- Can be called repeatedly without issues
- Suitable for displaying seat layout to users

**Response:**
```json
{
  "show_id": "show-123",
  "available_seats": [
    {
      "id": "seat-1",
      "row": "A",
      "number": "1",
      "type": "GOLD",
      "price": 200
    },
    {
      "id": "seat-2",
      "row": "A",
      "number": "2",
      "type": "GOLD",
      "price": 200
    }
  ],
  "total_available": 45,
  "total_capacity": 100
}
```
---
**For pre-booking validation: Option B**

```http
POST /api/shows/show-123/check-availability
{
  "seat_ids": ["seat-1", "seat-2"]
}
```

**Why:**
- Can lock seats temporarily during check
- Returns atomic, consistent snapshot
- Prevents race conditions before actual booking
- User selects seats → check → immediately book (short window)

**Response:**
```json
{
  "all_available": true,
  "seats": [
    {
      "id": "seat-1",
      "available": true,
      "price": 200,
      "locked_until": null
    },
    {
      "id": "seat-2",
      "available": true,
      "price": 200,
      "locked_until": null
    }
  ],
  "total_price": 400,
  "lock_token": "temp-lock-uuid-123"  // Optional: temporarily lock
}
```
---
**Advanced: Option C with ETag for consistency**

```http
GET /api/shows/show-123
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
```

When booking:
```http
POST /api/bookings
If-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"
{
  "show_id": "show-123",
  "seat_ids": ["seat-1"]
}
```

If ETag doesn't match (seats changed):
```http
HTTP/1.1 412 Precondition Failed
{
  "error": "SEAT_AVAILABILITY_CHANGED",
  "message": "Seat status changed, please refresh"
}
```

**Interview Answer:**
"I'd use **GET for displaying the seat map** (Option A) since it's cacheable and safe. For **pre-booking validation**, I'd use **POST** (Option B) to atomically check and optionally lock seats. If we need strong consistency, I'd implement **optimistic locking with ETags** (Option C) to detect concurrent modifications."

**Key Principles:**
- GET for reading/browsing (safe, cacheable)
- POST for operations with side effects (locking, validation with context)
- Use ETags for optimistic concurrency control
- Consider race conditions between check and book

</details>

---

## Section B: Request/Response Design

### Question 4: Payment Confirmation Endpoint

After a user books tickets, they need to confirm payment. Design this endpoint.

**Requirements:**
- User has a pending booking (seats locked, awaiting payment)
- Payment gateway returns success/failure
- Need to finalize booking or release seats

What's your design?

---
<details>
<summary><strong>Answer</strong></summary>

**Recommended Design:**

```http
PATCH /api/bookings/{booking_id}/payment
Authorization: Bearer <token>
Content-Type: application/json

{
  "payment_gateway": "RAZORPAY",
  "transaction_id": "pay_abc123xyz",
  "status": "SUCCESS",
  "amount": 450.00
}
```

**Why PATCH?**
- We're **updating** a specific field (payment status) of an existing resource
- Booking already exists in "PENDING_PAYMENT" state
- Not creating a new resource (not POST)
- Not replacing entire resource (not PUT)

**Response (200 OK):**
```json
{
  "booking_id": "BKG-789",
  "status": "CONFIRMED",
  "payment": {
    "transaction_id": "pay_abc123xyz",
    "amount": 450.00,
    "status": "SUCCESS",
    "timestamp": "2024-12-15T10:30:00Z"
  },
  "seats": ["A1", "A2"],
  "show": {
    "movie": "Avengers",
    "theater": "PVR Mumbai",
    "start_time": "2024-12-15T18:00:00Z"
  }
}
```
---
**Alternative Design (Also Valid):**

```http
POST /api/bookings/{booking_id}/confirm-payment
{
  "transaction_id": "pay_abc123xyz",
  "status": "SUCCESS"
}
```

**Why this works:**
- Some argue payment confirmation is an **action/operation**, not just a field update
- Creates a sub-resource (payment record)
- More explicit: "confirm payment" is clearer than "update booking"

**Comparison:**

| Aspect | PATCH /payment | POST /confirm-payment |
|--------|----------------|----------------------|
| RESTfulness | More RESTful (updating resource state) | Action-oriented (RPC-style) |
| Clarity | Generic (updating fields) | Explicit (clear action) |
| Idempotency | Idempotent by HTTP spec | Needs manual implementation |
| Payloads | More flexible (any payment fields) | Typically fixed structure |
---
**Error Responses:**

**Payment Failed:**
```http
HTTP/1.1 402 Payment Required
{
  "error": "PAYMENT_FAILED",
  "message": "Payment gateway rejected transaction",
  "transaction_id": "pay_abc123xyz",
  "gateway_response": {
    "code": "INSUFFICIENT_FUNDS",
    "message": "Card has insufficient balance"
  },
  "booking_id": "BKG-789",
  "status": "CANCELLED",
  "seats_released": true
}
```
---
**Booking Expired:**
```http
HTTP/1.1 410 Gone
{
  "error": "BOOKING_EXPIRED",
  "message": "Payment window expired, seats released",
  "booking_id": "BKG-789",
  "expired_at": "2024-12-15T10:15:00Z"
}
```
---
**Security Consideration:**
```python
def confirm_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Verify ownership
    if booking.user != request.user:
        return Response(
            {"error": "UNAUTHORIZED"},
            status=403
        )

    # Verify booking status
    if booking.status != 'PENDING_PAYMENT':
        return Response({
            "error": "INVALID_STATE",
            "message": f"Cannot confirm payment for booking in {booking.status} state"
        }, status=400)

    # Verify payment with gateway (don't trust client!)
    gateway_response = razorpay.verify_payment(
        transaction_id=request.data['transaction_id']
    )

    if not gateway_response.is_valid:
        return Response(
            {"error": "PAYMENT_VERIFICATION_FAILED"},
            status=402
        )

    # Update booking
    booking.status = 'CONFIRMED'
    booking.save()

    return Response(serialize(booking), status=200)
```
---
**Key Principles:**
- **PATCH for state updates**, POST for actions (both valid)
- Always **verify payments server-side** (never trust client)
- Return detailed error responses with actionable information
- Use appropriate status codes (402 for payment issues, 410 for expired)

</details>

---

### Question 5: Movie Search with Complex Filters

Design an endpoint to search movies with multiple filters: city, date, language, genre, rating, theater.

**Which design is better?**

**Option A:**
```http
POST /api/movies/search
{
  "city": "mumbai",
  "date": "2024-12-15",
  "language": "English",
  "genre": "Action",
  "min_rating": 8.0,
  "theater": "PVR"
}
```

**Option B:**
```http
GET /api/movies?city=mumbai&date=2024-12-15&language=English&genre=Action&min_rating=8.0&theater=PVR
```

---
<details>
<summary><strong>Answer</strong></summary>

**Correct: Option B (with caveats)**

**Why GET is better:**
- **Searching is a safe, read-only operation** (no side effects)
- **Cacheable**: Browser/CDN/proxy can cache results
- **Bookmarkable**: Users can share URLs
- **HTTP semantics**: GET is for retrieval, POST is for creation/actions
- **RESTful principle**: Use query parameters for filtering collections

**Correct Implementation:**
```http
GET /api/movies?city=mumbai&date=2024-12-15&language=English&genre=Action&min_rating=8.0&theater=PVR
```
---
**Response (200 OK):**
```json
{
  "filters_applied": {
    "city": "mumbai",
    "date": "2024-12-15",
    "language": "English",
    "genre": "Action",
    "min_rating": 8.0,
    "theater": "PVR"
  },
  "results": [
    {
      "id": "movie-1",
      "name": "Avengers: Endgame",
      "rating": 8.4,
      "language": "English",
      "genre": ["Action", "Sci-Fi"],
      "available_shows": [
        {
          "show_id": "show-1",
          "theater": "PVR Phoenix Mumbai",
          "start_time": "2024-12-15T18:00:00Z",
          "available_seats": 45
        }
      ]
    }
  ],
  "total_results": 1,
  "page": 1,
  "page_size": 20
}
```
---
**When POST Might Be Acceptable:**

**Case 1: Extremely complex filters (saved searches)**
```http
POST /api/movies/search
{
  "filters": {
    "city": ["mumbai", "delhi"],
    "date_range": {
      "start": "2024-12-15",
      "end": "2024-12-20"
    },
    "genres": {
      "include": ["Action", "Thriller"],
      "exclude": ["Horror"]
    },
    "rating": {
      "min": 7.0,
      "max": 10.0
    },
    "price_range": {
      "min": 100,
      "max": 500
    },
    "seat_availability": {
      "min_consecutive": 4,
      "types": ["GOLD", "PLATINUM"]
    }
  },
  "sort": [
    {"field": "rating", "order": "desc"},
    {"field": "price", "order": "asc"}
  ],
  "save_search": true
}
```
---

**Case 2: URL length limits**
- Query strings have practical limits (~2000 chars)
- If filters exceed this, POST is pragmatic

**Case 3: Sensitive filters (PII)**
```http
POST /api/recommendations
{
  "user_preferences": {
    "watch_history": ["movie-1", "movie-2"],
    "liked_genres": ["Sci-Fi", "Thriller"]
  }
}
```
- Don't put sensitive data in URLs (logged, cached)
---
**Handling Optional Parameters:**
```python
# Django View
def search_movies(request):
    # All filters optional
    city = request.GET.get('city')
    date = request.GET.get('date')
    language = request.GET.get('language')
    genre = request.GET.get('genre')
    min_rating = request.GET.get('min_rating')
    theater = request.GET.get('theater')

    queryset = Movie.objects.all()

    if city:
        queryset = queryset.filter(
            shows__theater__city__slug=city
        ).distinct()

    if date:
        queryset = queryset.filter(
            shows__start_time__date=date
        ).distinct()

    if language:
        queryset = queryset.filter(language=language)

    if genre:
        queryset = queryset.filter(category=genre)

    if min_rating:
        queryset = queryset.filter(rating__gte=min_rating)

    if theater:
        queryset = queryset.filter(
            shows__theater__name__icontains=theater
        ).distinct()

    return Response(MovieSerializer(queryset, many=True).data)
```
---
**Pagination & Sorting:**
```http
GET /api/movies?city=mumbai&language=English&page=2&page_size=20&sort=-rating,name
```

**Response Headers:**
```http
HTTP/1.1 200 OK
X-Total-Count: 157
X-Page: 2
X-Page-Size: 20
Link: </api/movies?city=mumbai&page=3>; rel="next",
      </api/movies?city=mumbai&page=1>; rel="prev"
```

**Interview Answer:**
"I'd use **GET with query parameters** (Option B) because searching is a **safe, idempotent operation**. This allows **caching**, **bookmarking**, and follows **RESTful principles**. However, if filters become extremely complex or hit URL length limits, I'd use **POST with a request body**, but document that it's not creating a resource—it's a pragmatic compromise."

**Key Principles:**
- Use GET for reads, even with complex filters
- Query params for simple filters
- Consider POST for very complex/sensitive filters
- Always support pagination for collections
- Make filters optional and composable

</details>

---

## Section C: Advanced Scenarios

### Question 6: Concurrency Conflict Response

Two users simultaneously try to book the last seat (A1) for a show. User 1's request arrives first and succeeds. User 2's request arrives 100ms later.

What should User 2 receive?

**Your endpoint:**
```http
POST /api/bookings
{
  "show_id": "show-123",
  "seat_ids": ["A1"]
}
```

**User 1:** Succeeds (200ms)
**User 2:** Arrives 100ms later

Design the error response for User 2.

---
<details>
<summary><strong>Answer</strong></summary>

**Correct Response: 409 Conflict**

```http
HTTP/1.1 409 Conflict
Content-Type: application/json

{
  "error": "SEAT_UNAVAILABLE",
  "message": "One or more selected seats are no longer available",
  "unavailable_seats": [
    {
      "id": "seat-1",
      "row": "A",
      "number": "1",
      "status": "BOOKED",
      "booked_at": "2024-12-15T10:30:15Z"
    }
  ],
  "alternative_seats": [
    {
      "id": "seat-2",
      "row": "A",
      "number": "2",
      "type": "GOLD",
      "price": 200,
      "available": true
    },
    {
      "id": "seat-3",
      "row": "A",
      "number": "3",
      "type": "GOLD",
      "price": 200,
      "available": true
    }
  ],
  "retry_possible": true,
  "show_id": "show-123"
}
```
---
**Why 409 Conflict?**
- **409** indicates: "Request conflicts with current state of the resource"
- Perfect for concurrency conflicts (seat status changed)
- More specific than 400 (Bad Request)
- Tells client this is a **state conflict**, not a validation error

**Alternative Status Codes (Less Ideal):**

**400 Bad Request:**
```json
{
  "error": "Seats not available"
}
```
❌ **Too generic**: Doesn't convey it's a concurrency issue
❌ **Implies client error**: But client's request was valid at the time

**423 Locked:**
```json
{
  "error": "Seats are locked by another user"
}
```
✅ **Could work**: Indicates temporary lock
❌ **Less common**: 423 typically for WebDAV locking
✅ **Use if**: Seats are *temporarily* locked (5-min payment window)

**428 Precondition Required:**
```json
{
  "error": "Seat availability changed, ETag required"
}
```
✅ **For optimistic locking**: When using If-Match headers
❌ **Overkill**: If not using ETags
---

**Interview Answer:**
"I'd return **409 Conflict** to clearly indicate a concurrency conflict. The response would include the **unavailable seats**, **alternative suggestions**, and a **retry_possible flag** to guide the user. On the server side, I'd use **SELECT FOR UPDATE** (pessimistic locking) to prevent race conditions in the first place."

**Key Principles:**
- **409 Conflict** for resource state conflicts
- Provide **actionable alternatives** in error responses
- Use **database-level locking** to minimize conflicts
- Include enough context for client to **retry intelligently**
- Clear, user-friendly error messages

</details>

---

### Question 7: Partial Updates - PATCH vs PUT

A user wants to change only their phone number, keeping email and name unchanged.

**Current user:**
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "9876543210"
}
```

**Request:**
```http
??? /api/users/123
{
  "phone": "9999999999"
}
```

Should you use PATCH or PUT? Why? What happens if you use the wrong one?

---
<details>
<summary><strong>Answer</strong></summary>

**Correct: Use PATCH**

```http
PATCH /api/users/123
Authorization: Bearer <token>
Content-Type: application/json

{
  "phone": "9999999999"
}
```

**Why PATCH?**
- **PATCH**: Partial update (modify specific fields)
- **PUT**: Full replacement (must send complete resource)

**With PATCH (Correct):**
```http
PATCH /api/users/123
{
  "phone": "9999999999"
}
```

**Result:**
```json
{
  "id": 123,
  "name": "John Doe",           // ✅ Unchanged
  "email": "john@example.com",  // ✅ Unchanged
  "phone": "9999999999"          // ✅ Updated
}
```

**With PUT (Wrong):**
```http
PUT /api/users/123
{
  "phone": "9999999999"
}
```
---
**Result (Incorrect Behavior):**
```json
{
  "id": 123,
  "name": null,                  // ❌ Cleared!
  "email": null,                 // ❌ Cleared!
  "phone": "9999999999"          // ✅ Updated
}
```

**Or (Correct PUT usage):**
```http
PUT /api/users/123
{
  "name": "John Doe",           // Must send all fields
  "email": "john@example.com",
  "phone": "9999999999"
}
```

**Key Difference:**

| Method | Purpose | Payload | Idempotent | Use Case |
|--------|---------|---------|-----------|----------|
| **PATCH** | Partial update | Only changed fields | Yes* | Update phone, change password |
| **PUT** | Full replacement | Complete resource | Yes | Replace entire profile |

*PATCH is idempotent in practice, though not strictly required by HTTP spec
---
**Server Implementation:**

**PATCH (partial_update):**
```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['PATCH'])
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Verify ownership
    if user != request.user:
        return Response({"error": "UNAUTHORIZED"}, status=403)

    # Update only provided fields
    if 'phone' in request.data:
        user.phone = request.data['phone']

    if 'email' in request.data:
        user.email = request.data['email']

    if 'name' in request.data:
        user.name = request.data['name']

    user.save()

    return Response({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone
    }, status=200)
```
---

**Better: Using DRF Serializer:**
```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only access their own profile
        return User.objects.filter(id=self.request.user.id)

    def partial_update(self, request, *args, **kwargs):
        # PATCH request
        # DRF automatically handles partial updates
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # PUT request
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial  # Key difference!
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
```
---
**Serializer:**
```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone']
        read_only_fields = ['id']

    def validate_phone(self, value):
        # Custom validation
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError(
                "Phone must be 10 digits"
            )
        return value
```

**Real-World Example: Booking Status Update**

**PATCH (Partial - Correct):**
```http
PATCH /api/bookings/BKG-789
{
  "status": "CANCELLED"
}
```
✅ **Only updates status**, leaves payment, seats, etc. unchanged

**PUT (Full - Wrong for this use case):**
```http
PUT /api/bookings/BKG-789
{
  "status": "CANCELLED"
}
```
❌ **Would erase payment info, seats, etc.** unless all fields sent
---
**Edge Case: Nullable Fields**

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'bio']

    def update(self, instance, validated_data):
        # For PATCH, only update provided fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
```

**Client wants to clear bio:**
```http
PATCH /api/users/123
{
  "bio": null
}
```
---
**Distinguish between:**
- Field not sent (don't update): `{}`
- Field sent as null (clear it): `{"bio": null}`

**Interview Answer:**
"I'd use **PATCH** because we're updating only the phone number, not replacing the entire user resource. **PATCH is for partial updates**—you send only changed fields. **PUT is for full replacement**—you must send the complete resource representation. Using PUT for partial updates would either fail validation or accidentally clear other fields."

**Key Principles:**
- **PATCH**: Partial updates (only send changed fields)
- **PUT**: Full replacement (send complete resource)
- Both are idempotent in practice
- Use DRF's `partial=True` for serializer flexibility
- Distinguish between "field not sent" and "field set to null"

</details>

---

## Key Takeaways

### HTTP Method Selection
- **GET**: Reading data (safe, cacheable, idempotent)
- **POST**: Creating resources, non-idempotent actions
- **PUT**: Full resource replacement
- **PATCH**: Partial resource updates
- **DELETE**: Remove resources

### Status Codes Matter
- **201 Created**: Resource successfully created
- **200 OK**: Successful GET/PATCH/PUT
- **204 No Content**: Successful DELETE (no body)
- **400 Bad Request**: Validation error
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Authenticated but not authorized
- **404 Not Found**: Resource doesn't exist
- **409 Conflict**: Resource state conflict (concurrency)
- **410 Gone**: Resource permanently deleted/expired
- **422 Unprocessable Entity**: Semantic validation error
- **428 Precondition Required**: Need If-Match header
---

### Resource Design Principles
1. **Use nouns, not verbs**: `/bookings` not `/book`
2. **Plural resources**: `/movies` not `/movie`
3. **Nesting for relationships**: `/shows/{id}/seats`
4. **Query params for filters**: `?city=mumbai&date=2024-12-15`
5. **Avoid deep nesting**: Max 2 levels

### Error Response Structure
```json
{
  "error": "ERROR_CODE",
  "message": "Human-readable explanation",
  "details": {
    "field": "specific_issue"
  },
  "retry_possible": true,
  "alternatives": []
}
```
---
### Idempotency
- Use `Idempotency-Key` header for critical operations
- Implement natural idempotency checks
- Return same response for duplicate requests

### Concurrency
- **409 Conflict** for race conditions
- Use database-level locking (SELECT FOR UPDATE)
- Provide alternatives in conflict responses
- Consider optimistic locking with ETags

---

**Practice Resources:**
- Implement these endpoints in your BookMyShow project
- Test with Postman (concurrent requests)
- Review existing APIs: Stripe, GitHub, Twilio
- Read REST API design books: "Web API Design" by Brian Mulloy

**Next Steps:**
- Design APIs for different domains (e-commerce, social media)
- Practice explaining trade-offs in interviews
- Learn GraphQL as an alternative to REST
- Study API versioning strategies

---

