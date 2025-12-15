# Ticket Management Guide - View, Cancel & Refund

## Overview

This guide covers **post-booking operations** where users manage their tickets - viewing history, getting details, and cancelling bookings.

**User Journey:**
```
1. View My Tickets (list of all bookings)
2. Get Ticket Details (show specific ticket)
3. Cancel Ticket (with refund rules)
```

**Key Features:**
- User can only access their own tickets (authorization)
- Cancellation allowed up to 1 hour before show
- Automatic refund calculation
- Status transitions (CONFIRMED → CANCELLED)

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Flow 1: List User Tickets](#flow-1-list-user-tickets)
3. [Flow 2: Get Ticket Details](#flow-2-get-ticket-details)
4. [Flow 3: Cancel Ticket](#flow-3-cancel-ticket)
5. [Authorization & Security](#authorization--security)
6. [Complete Sequence Diagram](#complete-sequence-diagram)

---

## Architecture Overview

```
┌──────────────┐
│    Client    │
│  (Frontend)  │
└──────┬───────┘
       │ HTTP Request
       ↓
┌──────────────────────────────────────────┐
│              Django URLs                 │
│         bookmyshow/urls.py              │
└──────┬───────────────────────────────────┘
       │ Route to View
       ↓
┌──────────────────────────────────────────┐
│         Views/ViewSets                   │
│        booking/views.py                  │
│  - TicketViewSet                         │
│    • list()                              │
│    • retrieve()                          │
│    • cancel() [@action]                  │
└──────┬───────────────────────────────────┘
       │ Query & Update
       ↓
┌──────────────────────────────────────────┐
│         Serializers                      │
│    booking/serializers.py                │
│  - TicketSerializer                      │
│  - TicketDetailSerializer                │
└──────┬───────────────────────────────────┘
       │ Database Operations
       ↓
┌──────────────────────────────────────────┐
│              Models                      │
│         booking/models.py                │
│  - Ticket                                │
│  - Payment                               │
│  - TicketSeat                            │
│  - ShowSeat                              │
└──────────────────────────────────────────┘
```

**Key Points:**
- Uses **ViewSet** (standard CRUD fits well here)
- **No Service Layer** - logic is simple enough for views
- **Permission-based** - Users can only see their own tickets
- **Atomic cancellations** - All-or-nothing refunds

---

## Flow 1: List User Tickets

**User Action:** User opens "My Bookings" page

### Sequence Diagram

```
Client          View              Model              Serializer
  │              │                 │                     │
  │──GET /api/tickets/──────────>│                     │
  │  Authorization: Bearer token  │                     │
  │              │                 │                     │
  │              │──Extract user from token              │
  │              │                 │                     │
  │              │──Ticket.objects.filter(user=user)───>│
  │              │                 │                     │
  │              │<──[Ticket, ...]─│                     │
  │              │                 │                     │
  │              │──TicketSerializer(tickets, many=True)─>│
  │              │                 │                     │
  │              │<────JSON [{...}, {...}]───────────────│
  │              │                 │                     │
  │<─200 OK──────│                 │                     │
  │  [tickets]   │                 │                     │
```

### API Endpoint

```http
GET /api/tickets/
Authorization: Bearer <token>
```

**Query Parameters:**
- `status` - Filter by status (CONFIRMED, CANCELLED, EXPIRED)
- `ordering` - Sort by field (-booking_time for latest first)

**Example:**
```http
GET /api/tickets/?status=CONFIRMED&ordering=-booking_time
```

**Response (200 OK):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "TKT-20241215-ABC123",
      "booking_time": "2024-12-15T10:30:00Z",
      "status": "CONFIRMED",
      "show": {
        "id": "show-1",
        "movie": {
          "name": "Avengers Endgame",
          "poster_url": "https://..."
        },
        "theater": {
          "name": "PVR Phoenix",
          "city": "Mumbai"
        },
        "start_time": "2024-12-15T18:00:00Z"
      },
      "seats_count": 2,
      "seat_numbers": ["A1", "A2"],
      "total_amount": 370.00,
      "can_cancel": true,
      "cancel_deadline": "2024-12-15T17:00:00Z"
    },
    {
      "id": "TKT-20241210-XYZ789",
      "booking_time": "2024-12-10T14:20:00Z",
      "status": "CONFIRMED",
      "show": {
        "movie": {
          "name": "Dune Part 2"
        },
        "start_time": "2024-12-10T20:00:00Z"
      },
      "seats_count": 3,
      "seat_numbers": ["C5", "C6", "C7"],
      "total_amount": 600.00,
      "can_cancel": false,
      "cancel_deadline": "2024-12-10T19:00:00Z"
    }
  ]
}
```

### Code Flow

#### 1. URL Configuration
**File:** `bookmyshow/urls.py`

```python
from rest_framework.routers import DefaultRouter
from booking.views import TicketViewSet

router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')

# Generates:
# GET    /api/tickets/           -> list()
# GET    /api/tickets/{id}/      -> retrieve()
# POST   /api/tickets/{id}/cancel/ -> cancel() [@action]
```

#### 2. View (Controller)
**File:** `booking/views.py`

```python
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from booking.models import Ticket, TicketStatus
from booking.serializers import TicketSerializer, TicketDetailSerializer

class TicketViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for user tickets.

    list():     GET /api/tickets/
    retrieve(): GET /api/tickets/{id}/
    cancel():   POST /api/tickets/{id}/cancel/

    Note: ReadOnlyModelViewSet = no create/update/delete
          Custom cancel action added separately
    """
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        """
        Return only tickets for current user.
        Security: Users can't see others' tickets!
        """
        return Ticket.objects.filter(
            user=self.request.user
        ).select_related(
            'show__movie',
            'show__screen__theater__city',
            'payment'
        ).prefetch_related(
            'ticketseat_set__show_seat__seat'
        ).order_by('-booking_time')

    def get_serializer_class(self):
        """Use detailed serializer for single ticket view"""
        if self.action == 'retrieve':
            return TicketDetailSerializer
        return TicketSerializer

    def list(self, request, *args, **kwargs):
        """
        GET /api/tickets/
        List all tickets for current user
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
```

**Location:** `booking/views.py:550-610`

**Key Points:**
1. **Authorization**: `get_queryset()` filters by `request.user`
2. **Query Optimization**: `select_related()` + `prefetch_related()`
3. **Filtering**: `?status=CONFIRMED` via DjangoFilterBackend
4. **Ordering**: Latest bookings first (`-booking_time`)
5. **Different Serializers**: List vs Detail views

#### 3. Serializer
**File:** `booking/serializers.py`

```python
class TicketSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for ticket lists
    """
    show = ShowSummarySerializer(read_only=True)
    seats_count = serializers.SerializerMethodField()
    seat_numbers = serializers.SerializerMethodField()
    can_cancel = serializers.SerializerMethodField()
    cancel_deadline = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id', 'booking_time', 'status', 'show',
            'seats_count', 'seat_numbers', 'total_amount',
            'can_cancel', 'cancel_deadline'
        ]

    def get_seats_count(self, obj):
        """Count of seats in this booking"""
        return obj.ticketseat_set.count()

    def get_seat_numbers(self, obj):
        """List of seat numbers (e.g., ['A1', 'A2'])"""
        return [
            f"{ts.show_seat.seat.row}{ts.show_seat.seat.number}"
            for ts in obj.ticketseat_set.all()
        ]

    def get_can_cancel(self, obj):
        """Can this ticket be cancelled?"""
        if obj.status != TicketStatus.CONFIRMED:
            return False

        # Allow cancellation up to 1 hour before show
        from django.utils import timezone
        from datetime import timedelta

        cutoff_time = obj.show.start_time - timedelta(hours=1)
        return timezone.now() < cutoff_time

    def get_cancel_deadline(self, obj):
        """Last time this ticket can be cancelled"""
        from datetime import timedelta
        return obj.show.start_time - timedelta(hours=1)


class ShowSummarySerializer(serializers.ModelSerializer):
    """Minimal show info for ticket list"""
    movie = MovieSummarySerializer(read_only=True)
    theater = TheaterSummarySerializer(source='screen.theater', read_only=True)

    class Meta:
        model = Show
        fields = ['id', 'movie', 'theater', 'start_time']
```

**Location:** `booking/serializers.py:300-360`

**Computed Fields:**
- `seats_count` - Number of seats
- `seat_numbers` - Human-readable seat labels
- `can_cancel` - Business logic for cancellation eligibility
- `cancel_deadline` - 1 hour before show time

#### 4. Models Involved

**Primary:** `Ticket`

**Related:**
- `Show` → `Movie`, `Theater`, `City`
- `TicketSeat` → `ShowSeat` → `Seat`
- `Payment` (OneToOne)

**Database Query:**
```sql
SELECT t.*, s.*, m.*, th.*, c.*
FROM booking_ticket t
INNER JOIN booking_show s ON t.show_id = s.id
INNER JOIN booking_movie m ON s.movie_id = m.id
INNER JOIN booking_screen sc ON s.screen_id = sc.id
INNER JOIN booking_theater th ON sc.theater_id = th.id
INNER JOIN booking_city c ON th.city_id = c.id
WHERE t.user_id = 123
ORDER BY t.booking_time DESC;
```

**Prefetch (separate query):**
```sql
SELECT ts.*, ss.*, seat.*
FROM booking_ticketseat ts
INNER JOIN booking_showseat ss ON ts.show_seat_id = ss.id
INNER JOIN booking_seat seat ON ss.seat_id = seat.id
WHERE ts.ticket_id IN ('TKT-1', 'TKT-2', ...);
```

---

## Flow 2: Get Ticket Details

**User Action:** User clicks on a ticket to see full details

### API Endpoint

```http
GET /api/tickets/{ticket_id}/
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": "TKT-20241215-ABC123",
  "booking_time": "2024-12-15T10:30:00Z",
  "status": "CONFIRMED",
  "show": {
    "id": "show-1",
    "movie": {
      "id": "movie-1",
      "name": "Avengers Endgame",
      "poster_url": "https://...",
      "duration": 181,
      "rating": 8.4
    },
    "theater": {
      "id": "pvr-mumbai-1",
      "name": "PVR Phoenix",
      "address": "High Street Phoenix, Lower Parel, Mumbai",
      "city": "Mumbai"
    },
    "screen": {
      "name": "Screen 1"
    },
    "start_time": "2024-12-15T18:00:00Z",
    "end_time": "2024-12-15T21:01:00Z"
  },
  "seats": [
    {
      "id": "show-1-seat-A1",
      "row": "A",
      "number": "1",
      "seat_type": "GOLD",
      "price": 200.00
    },
    {
      "id": "show-1-seat-A2",
      "row": "A",
      "number": "2",
      "seat_type": "GOLD",
      "price": 200.00
    }
  ],
  "pricing": {
    "base_amount": 400.00,
    "discount": 50.00,
    "convenience_fee": 20.00,
    "total_amount": 370.00
  },
  "payment": {
    "id": 1,
    "transaction_id": "pay_ABC123XYZ",
    "payment_mode": "UPI",
    "amount": 370.00,
    "status": "SUCCESS",
    "payment_time": "2024-12-15T10:32:00Z"
  },
  "can_cancel": true,
  "cancel_deadline": "2024-12-15T17:00:00Z",
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
}
```

### Code Flow

```python
class TicketViewSet(ReadOnlyModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        """
        GET /api/tickets/{id}/
        Get detailed ticket information
        """
        instance = self.get_object()

        # Security: Verify ownership
        if instance.user != request.user:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
```

**Location:** `booking/views.py:615-630`

**Serializer:**
```python
class TicketDetailSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer with all ticket details
    """
    show = ShowDetailSerializer(read_only=True)
    seats = serializers.SerializerMethodField()
    payment = PaymentSerializer(read_only=True)
    pricing = serializers.SerializerMethodField()
    can_cancel = serializers.SerializerMethodField()
    cancel_deadline = serializers.SerializerMethodField()
    qr_code = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id', 'booking_time', 'status', 'show', 'seats',
            'pricing', 'payment', 'can_cancel', 'cancel_deadline',
            'qr_code'
        ]

    def get_seats(self, obj):
        """All seat details"""
        return [
            {
                "id": ts.show_seat.id,
                "row": ts.show_seat.seat.row,
                "number": ts.show_seat.seat.number,
                "seat_type": ts.show_seat.seat.seat_type,
                "price": ts.show_seat.price
            }
            for ts in obj.ticketseat_set.all()
        ]

    def get_pricing(self, obj):
        """Pricing breakdown"""
        # This would be stored in ticket or calculated
        return {
            "base_amount": obj.total_amount,
            "discount": 0,
            "convenience_fee": 20,
            "total_amount": obj.total_amount
        }

    def get_qr_code(self, obj):
        """Generate QR code for ticket verification"""
        import qrcode
        from io import BytesIO
        import base64

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(obj.id)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return f"data:image/png;base64,{img_str}"
```

**Location:** `booking/serializers.py:365-430`

---

## Flow 3: Cancel Ticket

**User Action:** User cancels their booking

### Sequence Diagram

```
Client          View              Model              Database
  │              │                 │                     │
  │──POST /api/tickets/{id}/cancel/──────────────────>│
  │  Authorization: Bearer token   │                     │
  │              │                 │                     │
  │              │──Get ticket──────>                    │
  │              │<──Ticket─────────│                     │
  │              │                 │                     │
  │              │──Verify ownership│                     │
  │              │──Check can_cancel│                     │
  │              │                 │                     │
  │              │──BEGIN TRANSACTION──────────────────>│
  │              │                 │                     │
  │              │──Update Ticket──>│                     │
  │              │  status=CANCELLED│                     │
  │              │                 │                     │
  │              │──Update Payment─>│                     │
  │              │  status=REFUNDED │                     │
  │              │                 │                     │
  │              │──Update Seats───>│                     │
  │              │  status=AVAILABLE│                     │
  │              │                 │                     │
  │              │──COMMIT TRANSACTION─────────────────>│
  │              │                 │                     │
  │<─200 OK──────│                 │                     │
  │  {refund details}              │                     │
```

### API Endpoint

```http
POST /api/tickets/{ticket_id}/cancel/
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "message": "Ticket cancelled successfully",
  "ticket_id": "TKT-20241215-ABC123",
  "status": "CANCELLED",
  "refund": {
    "original_amount": 370.00,
    "refund_amount": 333.00,
    "cancellation_fee": 37.00,
    "refund_status": "PROCESSING",
    "refund_eta": "3-5 business days"
  },
  "cancelled_at": "2024-12-15T12:00:00Z"
}
```

**Error Responses:**

**Too Late to Cancel:**
```json
HTTP 400 Bad Request
{
  "error": "CANCELLATION_NOT_ALLOWED",
  "message": "Cannot cancel ticket within 1 hour of show time",
  "cancel_deadline": "2024-12-15T17:00:00Z",
  "current_time": "2024-12-15T17:30:00Z"
}
```

**Already Cancelled:**
```json
HTTP 400 Bad Request
{
  "error": "INVALID_STATUS",
  "message": "Ticket is already cancelled",
  "current_status": "CANCELLED"
}
```

### Code Flow

#### View with @action
**File:** `booking/views.py`

```python
class TicketViewSet(ReadOnlyModelViewSet):
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        POST /api/tickets/{id}/cancel/
        Cancel a ticket and refund amount
        """
        ticket = self.get_object()

        # Step 1: Verify ownership
        if ticket.user != request.user:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Step 2: Check ticket status
        if ticket.status != TicketStatus.CONFIRMED:
            return Response({
                "error": "INVALID_STATUS",
                "message": f"Cannot cancel ticket with status '{ticket.status}'",
                "current_status": ticket.status
            }, status=status.HTTP_400_BAD_REQUEST)

        # Step 3: Check cancellation deadline
        from django.utils import timezone
        from datetime import timedelta

        cutoff_time = ticket.show.start_time - timedelta(hours=1)
        if timezone.now() >= cutoff_time:
            return Response({
                "error": "CANCELLATION_NOT_ALLOWED",
                "message": "Cannot cancel ticket within 1 hour of show time",
                "cancel_deadline": cutoff_time,
                "current_time": timezone.now()
            }, status=status.HTTP_400_BAD_REQUEST)

        # Step 4: Calculate refund
        original_amount = ticket.total_amount
        cancellation_fee_percent = 10  # 10% cancellation fee
        cancellation_fee = (original_amount * cancellation_fee_percent) / 100
        refund_amount = original_amount - cancellation_fee

        # Step 5: Cancel ticket (atomic transaction)
        with transaction.atomic():
            # Update ticket status
            ticket.status = TicketStatus.CANCELLED
            ticket.cancelled_at = timezone.now()
            ticket.save()

            # Update payment status
            payment = ticket.payment
            payment.status = PaymentStatus.REFUNDED
            payment.refund_amount = refund_amount
            payment.refund_initiated_at = timezone.now()
            payment.save()

            # Release seats (make them available again)
            ShowSeat.objects.filter(
                ticketseat__ticket=ticket
            ).update(
                status=SeatStatus.AVAILABLE,
                locked_at=None,
                locked_by=None
            )

        # Step 6: Initiate refund with payment gateway (async)
        # refund_payment_task.delay(ticket.id, refund_amount)

        # Step 7: Send cancellation email/SMS (async)
        # send_cancellation_notification.delay(ticket.id)

        return Response({
            "message": "Ticket cancelled successfully",
            "ticket_id": ticket.id,
            "status": ticket.status,
            "refund": {
                "original_amount": float(original_amount),
                "refund_amount": float(refund_amount),
                "cancellation_fee": float(cancellation_fee),
                "refund_status": "PROCESSING",
                "refund_eta": "3-5 business days"
            },
            "cancelled_at": ticket.cancelled_at
        })
```

**Location:** `booking/views.py:640-730`

**Step-by-step:**
1. **Get ticket** - From URL parameter
2. **Verify ownership** - User can only cancel their own tickets
3. **Check status** - Must be CONFIRMED
4. **Check deadline** - Must be >1 hour before show
5. **Calculate refund** - Original amount - 10% fee
6. **Atomic update** - Ticket, Payment, Seats (all or nothing)
7. **Trigger async tasks** - Refund processing, notifications

### Cancellation Rules

**File:** `booking/models.py` or Django settings

```python
# Cancellation Rules
CANCELLATION_CUTOFF_HOURS = 1  # Must cancel 1 hour before show
CANCELLATION_FEE_PERCENT = 10  # 10% cancellation fee

# Refund Timeline
REFUND_PROCESSING_DAYS = 3-5  # Business days
```

### Refund Calculation

```python
def calculate_refund(ticket):
    """
    Calculate refund amount based on cancellation time
    """
    original_amount = ticket.total_amount
    time_to_show = ticket.show.start_time - timezone.now()

    # More than 24 hours: 90% refund
    if time_to_show.total_seconds() > 24 * 3600:
        fee_percent = 10

    # 1-24 hours: 80% refund
    elif time_to_show.total_seconds() > 3600:
        fee_percent = 20

    # Less than 1 hour: No refund
    else:
        return 0, original_amount

    fee = (original_amount * fee_percent) / 100
    refund = original_amount - fee

    return refund, fee
```

---

## Authorization & Security

### 1. Authentication Required

All ticket endpoints require authentication:

```python
permission_classes = [IsAuthenticated]
```

User must send valid token:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 2. Ownership Verification

Users can only access their own tickets:

```python
def get_queryset(self):
    """Filter by current user"""
    return Ticket.objects.filter(user=self.request.user)
```

**If user tries to access another user's ticket:**
```http
GET /api/tickets/TKT-OTHER-USER/

HTTP 404 Not Found
{
  "detail": "Not found."
}
```

**Note:** Returns 404, not 403, to avoid leaking information about ticket existence.

### 3. CSRF Protection

For POST requests from browser, include CSRF token:

```javascript
fetch('/api/tickets/TKT-123/cancel/', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'X-CSRFToken': getCookie('csrftoken')
    }
})
```

### 4. Rate Limiting

Prevent abuse with throttling:

```python
from rest_framework.throttling import UserRateThrottle

class CancellationRateThrottle(UserRateThrottle):
    rate = '5/hour'  # Max 5 cancellations per hour

class TicketViewSet(ReadOnlyModelViewSet):
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        self.throttle_classes = [CancellationRateThrottle]
        ...
```

---

## Complete Sequence Diagram

### End-to-End Ticket Management

```
User → Frontend → Backend → Database

[1] View My Tickets
    │
    ├──GET /api/tickets/
    │      └──TicketViewSet.list()
    │             └──Ticket.objects.filter(user=current_user)
    │
    └──Display list:
        • Avengers - Today 6PM - A1, A2 - ₹370 [Cancel]
        • Dune - Dec 10 - C5, C6, C7 - ₹600 [Past]

[2] View Ticket Details
    │
    ├──GET /api/tickets/TKT-20241215-ABC123/
    │      └──TicketViewSet.retrieve()
    │             └──Verify ownership
    │                    └──Return full details + QR code
    │
    └──Display:
        • Movie poster, theater, timing
        • Seat map with booked seats highlighted
        • QR code for entry
        • Payment details
        • [Cancel] button (if allowed)

[3] Cancel Ticket
    │
    ├──User clicks [Cancel]
    │      └──Confirm dialog: "Cancel booking? ₹37 fee applies"
    │             └──User confirms
    │
    ├──POST /api/tickets/TKT-20241215-ABC123/cancel/
    │      └──TicketViewSet.cancel()
    │             ├──Verify ownership
    │             ├──Check deadline
    │             ├──Calculate refund
    │             ├──BEGIN TRANSACTION
    │             ├──Update ticket → CANCELLED
    │             ├──Update payment → REFUNDED
    │             ├──Release seats → AVAILABLE
    │             └──COMMIT
    │
    └──Display confirmation:
        "Ticket cancelled. ₹333 will be refunded in 3-5 days"
```

---

## Summary: Files & Responsibilities

| Component | File | Responsibility |
|-----------|------|----------------|
| **URLs** | `bookmyshow/urls.py` | Router registration |
| **Views** | `booking/views.py` | TicketViewSet with list/retrieve/cancel |
| **Serializers** | `booking/serializers.py` | TicketSerializer, TicketDetailSerializer |
| **Models** | `booking/models.py` | Ticket, Payment, TicketSeat |
| **Permissions** | Built-in | IsAuthenticated |

---

## Key Takeaways

### 1. ViewSet for CRUD
Tickets fit well into ViewSet pattern (list, retrieve, custom action).

### 2. Security First
- Filter by `request.user` - users only see their tickets
- Verify ownership in cancel action
- Return 404 instead of 403 to avoid info leaks

### 3. Business Rules
- 1 hour cancellation cutoff
- 10% cancellation fee
- Automatic seat release

### 4. Atomic Cancellations
Use `@transaction.atomic` to ensure consistency:
- Ticket cancelled
- Payment refunded
- Seats released
All or nothing!

### 5. Computed Fields
- `can_cancel` - Check time and status
- `cancel_deadline` - Show time - 1 hour
- `qr_code` - Generate on demand

### 6. Different Serializers
- `TicketSerializer` - Lightweight for lists
- `TicketDetailSerializer` - Comprehensive for detail view

---

## Next Steps

**Continue to:** [11_ADMIN_MANAGEMENT_GUIDE.md](./11_ADMIN_MANAGEMENT_GUIDE.md)

This guide covers admin operations like managing movies, theaters, shows, and pricing rules.
