# Booking Flow Guide - Complete Ticket Booking Process

## Overview

This guide walks through the **most critical flow** in BookMyShow - the ticket booking process with **concurrency control**, payment handling, and ticket generation.

**User Journey:**
```
1. User selects show and seats
2. System validates and locks seats (5 min window)
3. User applies coupon (optional)
4. User proceeds to payment
5. Payment gateway processes payment
6. System confirms booking and generates ticket
```

**Key Challenge:** Multiple users trying to book the same seat simultaneously!

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Step 1: Book Tickets (Lock Seats)](#step-1-book-tickets-lock-seats)
3. [Step 2: Validate Coupon](#step-2-validate-coupon-optional)
4. [Step 3: Confirm Payment](#step-3-confirm-payment)
5. [Concurrency Control Deep Dive](#concurrency-control-deep-dive)
6. [Complete Sequence Diagram](#complete-sequence-diagram)
7. [Error Scenarios](#error-scenarios)

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
│         Views (Controllers)              │
│        booking/views.py                  │
│  - book_tickets()                        │
│  - validate_coupon()                     │
│  - confirm_payment()                     │
└──────┬───────────────────────────────────┘
       │ Call Service Layer
       ↓
┌──────────────────────────────────────────┐
│        Service Layer (Business Logic)    │
│     booking/services/                    │
│  - BookingServicePessimistic             │
│  - BookingServiceOptimistic              │
│  - BookingServiceThread                  │
│                                          │
│  Contains:                               │
│  - Seat validation                       │
│  - Concurrency control                   │
│  - Price calculation                     │
│  - Coupon application                    │
│  - Ticket generation                     │
└──────┬───────────────────────────────────┘
       │ Database Operations
       ↓
┌──────────────────────────────────────────┐
│              Models (ORM)                │
│         booking/models.py                │
│  - ShowSeat (with locks)                 │
│  - Ticket                                │
│  - Payment                               │
│  - Coupon                                │
└──────────────────────────────────────────┘
```

**Key Difference from Browse Flow:**
- Uses **Service Layer** for complex business logic
- Implements **3 concurrency strategies** (pessimistic, optimistic, thread-based)
- **Atomic transactions** to maintain consistency
- **Error handling** for race conditions

---

## Step 1: Book Tickets (Lock Seats)

**User Action:** User selects seats and clicks "Book Now"

### Sequence Diagram

```
Client          View              Service           Model           Database
  │              │                  │                │                 │
  │──POST /api/book/─────────────>│                  │                 │
  │  {show_id, seat_ids}           │                  │                 │
  │              │                  │                  │                 │
  │              │──validate input──│                  │                 │
  │              │                  │                  │                 │
  │              │──book_tickets()──>│                 │                 │
  │              │                  │                  │                 │
  │              │                  │──BEGIN TRANSACTION──────────────>│
  │              │                  │                  │                 │
  │              │                  │──SELECT seats    │                 │
  │              │                  │  FOR UPDATE      │                 │
  │              │                  │<─────LOCK ACQUIRED───────────────│
  │              │                  │                  │                 │
  │              │                  │──Check status────>│                 │
  │              │                  │  (AVAILABLE?)    │                 │
  │              │                  │<──Yes/No─────────│                 │
  │              │                  │                  │                 │
  │              │    [If Available]│                  │                 │
  │              │                  │──Update seats────>│                 │
  │              │                  │  status=LOCKED   │                 │
  │              │                  │<──Updated────────│                 │
  │              │                  │                  │                 │
  │              │                  │──Calculate price─>│                 │
  │              │                  │<──Total amount───│                 │
  │              │                  │                  │                 │
  │              │                  │──Apply coupon────>│                 │
  │              │                  │<──Discounted amt─│                 │
  │              │                  │                  │                 │
  │              │                  │──Create Ticket───>│                 │
  │              │                  │──Create Payment──>│                 │
  │              │                  │──Link seats──────>│                 │
  │              │                  │<──Ticket created─│                 │
  │              │                  │                  │                 │
  │              │                  │──COMMIT TRANSACTION─────────────>│
  │              │                  │                  │                 │
  │              │<──Ticket object──│                  │                 │
  │              │                  │                  │                 │
  │<─201 Created─│                  │                  │                 │
  │  {ticket_id, │                  │                  │                 │
  │   seats,     │                  │                  │                 │
  │   amount}    │                  │                  │                 │
  │              │                  │                  │                 │
  │      [If Not Available - Race Condition Detected]                   │
  │              │                  │                  │                 │
  │              │                  │──ROLLBACK TRANSACTION──────────>│
  │              │<──Exception──────│                  │                 │
  │<─400/409─────│                  │                  │                 │
  │  {error msg} │                  │                  │                 │
```

### API Endpoint

```http
POST /api/book/
Authorization: Bearer <token>
Content-Type: application/json

{
  "show_id": "show-1",
  "seat_ids": [
    "show-1-pvr-mumbai-1-screen-1-A1",
    "show-1-pvr-mumbai-1-screen-1-A2"
  ],
  "payment_mode": "UPI",
  "coupon_code": "DISCOUNT50"
}
```

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `show_id` | string | Yes | Show identifier |
| `seat_ids` | array | Yes | List of ShowSeat IDs |
| `payment_mode` | string | Yes | UPI, CARD, NET_BANKING, WALLET |
| `coupon_code` | string | No | Discount coupon code |

**Response (201 Created):**
```json
{
  "ticket_id": "TKT-20241215-ABC123",
  "booking_time": "2024-12-15T10:30:00Z",
  "status": "PENDING_PAYMENT",
  "show": {
    "id": "show-1",
    "movie": "Avengers Endgame",
    "theater": "PVR Phoenix Mumbai",
    "start_time": "2024-12-15T18:00:00Z"
  },
  "seats": [
    {
      "id": "show-1-seat-A1",
      "row": "A",
      "number": "1",
      "type": "GOLD",
      "price": 200.00
    },
    {
      "id": "show-1-seat-A2",
      "row": "A",
      "number": "2",
      "type": "GOLD",
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
    "mode": "UPI",
    "status": "PENDING",
    "expires_at": "2024-12-15T10:35:00Z"
  }
}
```

### Code Flow

#### 1. URL Configuration
**File:** `bookmyshow/urls.py`

```python
from booking.views import book_tickets

urlpatterns = [
    path('api/book/', book_tickets, name='book-tickets'),
]
```

**Location:** `bookmyshow/urls.py:25`

#### 2. View (Controller)
**File:** `booking/views.py`

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from booking.serializers import BookingRequestSerializer, TicketSerializer
from booking.services import get_booking_service
from booking.exceptions import SeatNotAvailableException, OptimisticLockException

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_tickets(request):
    """
    Book tickets for a show.

    POST /api/book/
    {
        "show_id": "show-1",
        "seat_ids": ["seat-1", "seat-2"],
        "payment_mode": "UPI",
        "coupon_code": "DISCOUNT50"
    }

    Returns:
        201 Created: Ticket successfully booked
        400 Bad Request: Invalid input or seats not available
        409 Conflict: Concurrency conflict (optimistic locking)
    """
    # Step 1: Validate input
    serializer = BookingRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Step 2: Get the appropriate booking service
    # This returns one of: Pessimistic, Optimistic, or Thread-based service
    service = get_booking_service()

    # Step 3: Call service to book tickets
    try:
        ticket = service.book_tickets(
            user=request.user,
            show_id=serializer.validated_data['show_id'],
            seat_ids=serializer.validated_data['seat_ids'],
            payment_mode=serializer.validated_data['payment_mode'],
            coupon_code=serializer.validated_data.get('coupon_code')
        )

        # Step 4: Return success response
        return Response(
            TicketSerializer(ticket).data,
            status=status.HTTP_201_CREATED
        )

    except SeatNotAvailableException as e:
        # Seats already booked by someone else
        return Response(
            {
                "error": "SEAT_NOT_AVAILABLE",
                "message": str(e),
                "details": "One or more selected seats are no longer available"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    except OptimisticLockException as e:
        # Concurrency conflict (optimistic locking)
        return Response(
            {
                "error": "CONCURRENT_MODIFICATION",
                "message": str(e),
                "details": "Seat availability changed. Please refresh and try again."
            },
            status=status.HTTP_409_CONFLICT
        )

    except Exception as e:
        # Unexpected error
        return Response(
            {
                "error": "BOOKING_FAILED",
                "message": "An unexpected error occurred",
                "details": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
```

**Location:** `booking/views.py:300-370`

**Step-by-step:**
1. **Validate input** - Use `BookingRequestSerializer`
2. **Get service** - Factory pattern returns configured service
3. **Call service** - Delegates business logic to service layer
4. **Handle errors** - Different status codes for different errors
5. **Return response** - Serialize ticket to JSON

#### 3. Input Validation (Serializer)
**File:** `booking/serializers.py`

```python
class BookingRequestSerializer(serializers.Serializer):
    """
    Validates booking request input
    """
    show_id = serializers.CharField(max_length=100)
    seat_ids = serializers.ListField(
        child=serializers.CharField(max_length=100),
        min_length=1,
        max_length=10  # Max 10 seats per booking
    )
    payment_mode = serializers.ChoiceField(
        choices=['UPI', 'CARD', 'NET_BANKING', 'WALLET']
    )
    coupon_code = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True
    )

    def validate_show_id(self, value):
        """Verify show exists"""
        try:
            Show.objects.get(id=value)
        except Show.DoesNotExist:
            raise serializers.ValidationError("Show not found")
        return value

    def validate_seat_ids(self, value):
        """Verify seats exist and belong to the show"""
        if not value:
            raise serializers.ValidationError("At least one seat must be selected")

        # Check for duplicates
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Duplicate seat IDs not allowed")

        return value

    def validate(self, data):
        """Cross-field validation"""
        show_id = data['show_id']
        seat_ids = data['seat_ids']

        # Verify all seats belong to this show
        seats = ShowSeat.objects.filter(id__in=seat_ids, show_id=show_id)
        if seats.count() != len(seat_ids):
            raise serializers.ValidationError(
                "Some seats do not belong to this show"
            )

        return data
```

**Location:** `booking/serializers.py:200-250`

**Validation Logic:**
1. **Show exists** - Query database
2. **Seats valid** - No duplicates, at least 1, max 10
3. **Seats belong to show** - Cross-reference ShowSeat.show_id
4. **Payment mode valid** - One of allowed choices

#### 4. Service Layer (Business Logic)
**File:** `booking/services/booking_service_pessimistic.py`

```python
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from booking.models import (
    Show, ShowSeat, Ticket, Payment, TicketSeat,
    Coupon, SeatStatus, PaymentStatus
)
from booking.exceptions import SeatNotAvailableException

class BookingServicePessimistic:
    """
    Implements pessimistic locking using SELECT FOR UPDATE.

    How it works:
    - Acquires database-level lock on seat rows
    - Other transactions wait until lock is released
    - Guarantees no two bookings for same seat
    - Best for high contention scenarios
    """

    @transaction.atomic
    def book_tickets(self, user, show_id, seat_ids, payment_mode, coupon_code=None):
        """
        Book tickets with pessimistic locking.

        Args:
            user: User object
            show_id: Show identifier
            seat_ids: List of ShowSeat IDs
            payment_mode: Payment method
            coupon_code: Optional coupon code

        Returns:
            Ticket object

        Raises:
            SeatNotAvailableException: If seats are not available
        """
        # Step 1: Get the show
        try:
            show = Show.objects.select_related('movie', 'screen__theater').get(id=show_id)
        except Show.DoesNotExist:
            raise ValueError("Show not found")

        # Step 2: Lock and fetch seats (CRITICAL SECTION)
        # SELECT * FROM booking_showseat
        # WHERE id IN (seat_ids) AND show_id = show_id
        # FOR UPDATE;
        #
        # FOR UPDATE acquires row-level locks
        # Other transactions trying to lock same rows will WAIT
        seats = ShowSeat.objects.select_for_update().filter(
            id__in=seat_ids,
            show=show
        )

        # Convert to list to execute query (and acquire locks)
        seats = list(seats)

        # Step 3: Validate seats
        if len(seats) != len(seat_ids):
            raise SeatNotAvailableException("Some seats not found")

        # Check if all seats are available
        unavailable_seats = [s for s in seats if s.status != SeatStatus.AVAILABLE]
        if unavailable_seats:
            seat_numbers = [s.seat.number for s in unavailable_seats]
            raise SeatNotAvailableException(
                f"Seats {', '.join(seat_numbers)} are not available"
            )

        # Step 4: Calculate pricing
        base_amount = sum(seat.price for seat in seats)
        discount_amount = 0

        # Apply coupon if provided
        if coupon_code:
            try:
                coupon = Coupon.objects.get(
                    code=coupon_code,
                    is_active=True,
                    valid_from__lte=timezone.now(),
                    valid_until__gte=timezone.now()
                )
                discount_amount = (base_amount * coupon.discount_percent) / 100
            except Coupon.DoesNotExist:
                pass  # Invalid coupon, proceed without discount

        convenience_fee = len(seats) * 10  # ₹10 per seat
        total_amount = base_amount - discount_amount + convenience_fee

        # Step 5: Create ticket
        ticket = Ticket.objects.create(
            id=self._generate_ticket_id(),
            user=user,
            show=show,
            booking_time=timezone.now(),
            total_amount=total_amount,
            status='PENDING_PAYMENT'
        )

        # Step 6: Create payment record
        Payment.objects.create(
            ticket=ticket,
            amount=total_amount,
            payment_mode=payment_mode,
            status=PaymentStatus.PENDING,
            transaction_id=None  # Set after payment gateway response
        )

        # Step 7: Update seat status and link to ticket
        for seat in seats:
            seat.status = SeatStatus.LOCKED
            seat.locked_at = timezone.now()
            seat.locked_by = user
            seat.save()

            # Create TicketSeat (many-to-many through model)
            TicketSeat.objects.create(
                ticket=ticket,
                show_seat=seat
            )

        # Step 8: Schedule seat release (celery task in production)
        # If payment not confirmed in 5 minutes, release seats
        # ticket.expires_at = timezone.now() + timedelta(minutes=5)
        # release_seats_task.apply_async((ticket.id,), countdown=300)

        return ticket

    def _generate_ticket_id(self):
        """Generate unique ticket ID"""
        import uuid
        date_str = timezone.now().strftime('%Y%m%d')
        unique_id = str(uuid.uuid4())[:8].upper()
        return f"TKT-{date_str}-{unique_id}"
```

**Location:** `booking/services/booking_service_pessimistic.py:1-150`

**Key Concepts:**

**1. @transaction.atomic**
- Wraps entire method in database transaction
- All-or-nothing: Either all changes commit, or all rollback
- If exception raised, automatic rollback

**2. select_for_update()**
- Acquires database lock on rows
- Other transactions **wait** until lock released
- Prevents race conditions at database level

**3. Lock Duration**
- Lock held until transaction commits/rolls back
- Typically milliseconds
- No deadlock if proper ordering maintained

**4. Seat Status Lifecycle**
```
AVAILABLE → LOCKED → BOOKED
            ↓ (timeout)
          AVAILABLE
```

#### 5. Models Involved

**Primary Models:**

**ShowSeat** - Seat instance for a show
```python
class ShowSeat(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=SeatStatus.choices,
        default=SeatStatus.AVAILABLE
    )
    version = models.IntegerField(default=0)  # For optimistic locking
    locked_at = models.DateTimeField(null=True, blank=True)
    locked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'booking_showseat'
        unique_together = ['show', 'seat']
```

**Ticket** - Booking record
```python
class Ticket(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='tickets')
    booking_time = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=TicketStatus.choices,
        default=TicketStatus.PENDING_PAYMENT
    )

    class Meta:
        db_table = 'booking_ticket'
```

**Payment** - Payment record (1:1 with Ticket)
```python
class Payment(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    payment_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'booking_payment'
```

**TicketSeat** - Links tickets to seats (many-to-many)
```python
class TicketSeat(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    show_seat = models.ForeignKey(ShowSeat, on_delete=models.CASCADE)

    class Meta:
        db_table = 'booking_ticketseat'
        unique_together = ['ticket', 'show_seat']
```

**Location:** `booking/models.py:200-350`

### Database Queries

**What actually happens in database:**

```sql
-- Step 1: Begin transaction
BEGIN;

-- Step 2: Lock seats (blocks other transactions)
SELECT * FROM booking_showseat
WHERE id IN ('show-1-seat-A1', 'show-1-seat-A2')
  AND show_id = 'show-1'
FOR UPDATE;  -- ← LOCKS these rows

-- Step 3: Check status (still in transaction, lock held)
-- (Done in Python after fetch)

-- Step 4: Update seats
UPDATE booking_showseat
SET status = 'LOCKED',
    locked_at = NOW(),
    locked_by_id = 123
WHERE id IN ('show-1-seat-A1', 'show-1-seat-A2');

-- Step 5: Create ticket
INSERT INTO booking_ticket (id, user_id, show_id, total_amount, status)
VALUES ('TKT-20241215-ABC123', 123, 'show-1', 370.00, 'PENDING_PAYMENT');

-- Step 6: Create payment
INSERT INTO booking_payment (ticket_id, amount, payment_mode, status)
VALUES ('TKT-20241215-ABC123', 370.00, 'UPI', 'PENDING');

-- Step 7: Link seats to ticket
INSERT INTO booking_ticketseat (ticket_id, show_seat_id)
VALUES ('TKT-20241215-ABC123', 'show-1-seat-A1'),
       ('TKT-20241215-ABC123', 'show-1-seat-A2');

-- Step 8: Commit (releases locks)
COMMIT;
```

**Timeline with concurrent requests:**

```
Time  Transaction A                 Transaction B
0ms   BEGIN;
10ms  SELECT ... FOR UPDATE;        BEGIN;
      (Locks acquired)
20ms  UPDATE seats...               SELECT ... FOR UPDATE;
30ms  INSERT ticket...              (WAITING for lock...)
40ms  INSERT payment...             (STILL WAITING...)
50ms  COMMIT;                       (Lock released!)
      (Locks released)
60ms                                 (Lock acquired!)
70ms                                 Sees seats as LOCKED
80ms                                 ROLLBACK;
                                     Returns error
```

---

## Step 2: Validate Coupon (Optional)

**User Action:** User enters coupon code before payment

### API Endpoint

```http
POST /api/validate-coupon/
Authorization: Bearer <token>

{
  "coupon_code": "DISCOUNT50",
  "booking_amount": 400.00
}
```

**Response (200 OK):**
```json
{
  "valid": true,
  "coupon": {
    "code": "DISCOUNT50",
    "discount_percent": 10,
    "max_discount": 100
  },
  "original_amount": 400.00,
  "discount_amount": 40.00,
  "final_amount": 360.00
}
```

### Code Flow

```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_coupon(request):
    """Validate coupon code"""
    coupon_code = request.data.get('coupon_code')
    amount = request.data.get('booking_amount')

    try:
        coupon = Coupon.objects.get(
            code=coupon_code,
            is_active=True,
            valid_from__lte=timezone.now(),
            valid_until__gte=timezone.now()
        )

        discount = min(
            (amount * coupon.discount_percent) / 100,
            coupon.max_discount
        )

        return Response({
            "valid": True,
            "coupon": CouponSerializer(coupon).data,
            "original_amount": amount,
            "discount_amount": discount,
            "final_amount": amount - discount
        })

    except Coupon.DoesNotExist:
        return Response({
            "valid": False,
            "message": "Invalid or expired coupon code"
        }, status=400)
```

**Location:** `booking/views.py:400-435`

---

## Step 3: Confirm Payment

**User Action:** Payment gateway returns success, system confirms booking

### Sequence Diagram

```
Client          View              Service           Model           Payment Gateway
  │              │                  │                │                      │
  │──POST /api/tickets/{id}/confirm-payment/──────>│                      │
  │  {payment_success: true,       │                │                      │
  │   transaction_id: "pay_123"}   │                │                      │
  │              │                  │                │                      │
  │              │──Verify payment──────────────────────────────────────>│
  │              │  with gateway    │                │                      │
  │              │<──────────────Payment verified────────────────────────│
  │              │                  │                │                      │
  │              │──Update ticket───────────────────>│                      │
  │              │  status=CONFIRMED│                │                      │
  │              │                  │                │                      │
  │              │──Update seats────────────────────>│                      │
  │              │  status=BOOKED   │                │                      │
  │              │                  │                │                      │
  │              │──Update payment──────────────────>│                      │
  │              │  status=SUCCESS  │                │                      │
  │              │                  │                │                      │
  │<─200 OK──────│                  │                │                      │
  │  {ticket confirmed}             │                │                      │
```

### API Endpoint

```http
POST /api/tickets/{ticket_id}/confirm-payment/
Authorization: Bearer <token>

{
  "payment_success": true,
  "transaction_id": "pay_ABC123XYZ",
  "payment_gateway_response": {
    "status": "SUCCESS",
    "amount": 370.00
  }
}
```

**Response (200 OK):**
```json
{
  "ticket_id": "TKT-20241215-ABC123",
  "status": "CONFIRMED",
  "confirmation_time": "2024-12-15T10:32:00Z",
  "payment": {
    "transaction_id": "pay_ABC123XYZ",
    "amount": 370.00,
    "status": "SUCCESS"
  },
  "seats": ["A1", "A2"],
  "show": {
    "movie": "Avengers Endgame",
    "theater": "PVR Phoenix Mumbai",
    "start_time": "2024-12-15T18:00:00Z"
  }
}
```

### Code Flow

```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_payment(request, ticket_id):
    """
    Confirm payment and finalize booking
    """
    try:
        ticket = Ticket.objects.select_related('payment').get(id=ticket_id)
    except Ticket.DoesNotExist:
        return Response({"error": "Ticket not found"}, status=404)

    # Verify ownership
    if ticket.user != request.user:
        return Response({"error": "Unauthorized"}, status=403)

    # Check ticket status
    if ticket.status != TicketStatus.PENDING_PAYMENT:
        return Response({
            "error": "Invalid ticket status",
            "current_status": ticket.status
        }, status=400)

    payment_success = request.data.get('payment_success')
    transaction_id = request.data.get('transaction_id')

    if not payment_success:
        # Payment failed, release seats
        with transaction.atomic():
            ShowSeat.objects.filter(
                ticketseat__ticket=ticket
            ).update(
                status=SeatStatus.AVAILABLE,
                locked_at=None,
                locked_by=None
            )
            ticket.status = TicketStatus.CANCELLED
            ticket.save()
            ticket.payment.status = PaymentStatus.FAILED
            ticket.payment.save()

        return Response({
            "message": "Payment failed, seats released"
        }, status=402)

    # TODO: Verify payment with gateway
    # gateway_response = razorpay.verify_payment(transaction_id)
    # if not gateway_response.is_valid:
    #     return Response({"error": "Payment verification failed"}, status=400)

    # Payment successful, confirm booking
    with transaction.atomic():
        # Update ticket
        ticket.status = TicketStatus.CONFIRMED
        ticket.save()

        # Update payment
        ticket.payment.transaction_id = transaction_id
        ticket.payment.status = PaymentStatus.SUCCESS
        ticket.payment.payment_time = timezone.now()
        ticket.payment.save()

        # Update seats to BOOKED
        ShowSeat.objects.filter(
            ticketseat__ticket=ticket
        ).update(
            status=SeatStatus.BOOKED,
            locked_at=None,
            locked_by=None
        )

    # Send confirmation email/SMS (async task)
    # send_booking_confirmation.delay(ticket.id)

    return Response(TicketSerializer(ticket).data)
```

**Location:** `booking/views.py:450-530`

---

## Concurrency Control Deep Dive

### Three Strategies Implemented

#### 1. Pessimistic Locking (Recommended)

**File:** `booking/services/booking_service_pessimistic.py`

**How it works:**
- Uses `SELECT FOR UPDATE` to lock rows
- Database-level locking
- Other transactions **wait** for lock to be released

**Pros:**
- ✅ Guaranteed consistency
- ✅ No retries needed
- ✅ Works in distributed systems

**Cons:**
- ❌ Slower (transactions wait)
- ❌ Potential for deadlocks

**Best for:** High contention (popular shows, limited seats)

#### 2. Optimistic Locking

**File:** `booking/services/booking_service_optimistic.py`

**How it works:**
- Uses `version` field to detect conflicts
- No database locks
- Detects conflicts after the fact, requires retry

```python
@transaction.atomic
def book_tickets(self, user, show_id, seat_ids, ...):
    # Fetch seats without locking
    seats = ShowSeat.objects.filter(id__in=seat_ids)

    # Try to update with version check
    updated = ShowSeat.objects.filter(
        id__in=seat_ids,
        status=SeatStatus.AVAILABLE,
        version=F('version')  # Current version
    ).update(
        status=SeatStatus.LOCKED,
        version=F('version') + 1  # Increment atomically
    )

    if updated != len(seat_ids):
        # Someone else modified these seats!
        raise OptimisticLockException("Seats were modified by another user")

    # Continue with booking...
```

**Pros:**
- ✅ Better performance (no waiting)
- ✅ Higher throughput

**Cons:**
- ❌ Requires retry logic in client
- ❌ Wasted work on conflicts

**Best for:** Low contention (many seats, few users)

#### 3. Thread-Based Locking (Educational Only)

**File:** `booking/services/booking_service_thread.py`

**How it works:**
- Uses Python `threading.Lock()`
- In-memory lock per seat

**Pros:**
- ✅ Simple to understand

**Cons:**
- ❌ Only works in single process
- ❌ Doesn't work with multiple servers
- ❌ Not production-ready

**Best for:** Teaching, local development

### Comparison

| Strategy | Consistency | Performance | Scalability | Retries |
|----------|-------------|-------------|-------------|---------|
| Pessimistic | 🟢 Guaranteed | 🟡 Medium | 🟢 Yes | ❌ No |
| Optimistic | 🟢 Guaranteed | 🟢 High | 🟢 Yes | ✅ Yes |
| Thread-based | 🔴 No | 🟢 High | 🔴 No | ❌ No |

### Configuration

**File:** `bookmyshow/settings.py`

```python
# Choose concurrency strategy
BOOKING_SERVICE = 'pessimistic'  # or 'optimistic' or 'thread'
```

**Factory Function:**
```python
def get_booking_service():
    """Factory to return configured service"""
    from django.conf import settings

    strategy = settings.BOOKING_SERVICE

    if strategy == 'pessimistic':
        from booking.services.booking_service_pessimistic import BookingServicePessimistic
        return BookingServicePessimistic()
    elif strategy == 'optimistic':
        from booking.services.booking_service_optimistic import BookingServiceOptimistic
        return BookingServiceOptimistic()
    else:
        from booking.services.booking_service_thread import BookingServiceThread
        return BookingServiceThread()
```

---

## Complete Sequence Diagram

### End-to-End Booking Flow

```
User → Frontend → Backend → Service → Database

[1] User selects seats
    │
    └──Show seat map with colors
        Green = Available
        Gray = Booked
        Yellow = Locked (by others)

[2] User clicks "Book"
    │
    ├──POST /api/book/
    │      └──book_tickets()
    │             └──BookingService.book_tickets()
    │                    ├──BEGIN TRANSACTION
    │                    ├──SELECT seats FOR UPDATE (LOCK)
    │                    ├──Check status == AVAILABLE
    │                    ├──Calculate price
    │                    ├──Apply coupon
    │                    ├──Create Ticket (PENDING_PAYMENT)
    │                    ├──Create Payment (PENDING)
    │                    ├──Update seats to LOCKED
    │                    └──COMMIT
    │
    └──201 Created
        {ticket_id, amount, expires_in: 300s}

[3] User proceeds to payment
    │
    ├──Redirect to payment gateway
    │      └──User enters card/UPI details
    │             └──Payment processed
    │
    └──Gateway redirects back with status

[4] Frontend confirms payment
    │
    ├──POST /api/tickets/{id}/confirm-payment/
    │      └──confirm_payment()
    │             ├──BEGIN TRANSACTION
    │             ├──Update Ticket → CONFIRMED
    │             ├──Update Payment → SUCCESS
    │             ├──Update seats → BOOKED
    │             └──COMMIT
    │
    └──200 OK
        {ticket confirmed, QR code}

[5] User receives confirmation
    │
    ├──Email sent (async)
    ├──SMS sent (async)
    └──Ticket shown in app
```

---

## Error Scenarios

### Scenario 1: Seats Already Booked (Race Condition)

**What happens:**
1. User A and User B both try to book seat A1
2. User A's request arrives first
3. User A acquires lock, books seat
4. User B's request arrives 100ms later
5. User B tries to acquire lock → **waits**
6. User A commits → releases lock
7. User B acquires lock, checks status → **LOCKED**
8. User B's booking fails

**Response to User B:**
```json
HTTP 400 Bad Request
{
  "error": "SEAT_NOT_AVAILABLE",
  "message": "Seats A1 are not available",
  "details": "One or more selected seats are no longer available"
}
```

### Scenario 2: Payment Timeout

**What happens:**
1. User books seats (status = LOCKED)
2. Redirected to payment gateway
3. User closes browser / payment takes too long
4. After 5 minutes, seats auto-released

**Implementation:**
```python
# In production, use Celery
from celery import shared_task

@shared_task
def release_expired_seats():
    """
    Run every minute, release seats locked > 5 min ago
    """
    cutoff = timezone.now() - timedelta(minutes=5)

    expired_tickets = Ticket.objects.filter(
        status=TicketStatus.PENDING_PAYMENT,
        booking_time__lt=cutoff
    )

    for ticket in expired_tickets:
        with transaction.atomic():
            ShowSeat.objects.filter(
                ticketseat__ticket=ticket
            ).update(
                status=SeatStatus.AVAILABLE,
                locked_at=None,
                locked_by=None
            )
            ticket.status = TicketStatus.EXPIRED
            ticket.save()
```

### Scenario 3: Invalid Coupon

**Response:**
```json
HTTP 400 Bad Request
{
  "error": "INVALID_COUPON",
  "message": "Coupon code 'INVALID123' is not valid or has expired"
}
```

Booking proceeds without discount.

### Scenario 4: Optimistic Lock Conflict

**Response:**
```json
HTTP 409 Conflict
{
  "error": "CONCURRENT_MODIFICATION",
  "message": "Seat availability changed",
  "details": "Please refresh and try again"
}
```

Client should retry with updated seat data.

---

## Summary: Files & Responsibilities

| Component | File | Responsibility |
|-----------|------|----------------|
| **URLs** | `bookmyshow/urls.py` | Route booking endpoints |
| **Views** | `booking/views.py` | Handle HTTP, validate, call services |
| **Serializers** | `booking/serializers.py` | Input validation, JSON transform |
| **Services** | `booking/services/*.py` | Business logic, concurrency control |
| **Models** | `booking/models.py` | Database structure |
| **Exceptions** | `booking/exceptions.py` | Custom exceptions |

---

## Key Takeaways

### 1. Service Layer Pattern
Complex business logic (booking) belongs in **service layer**, not views.

### 2. Atomic Transactions
Use `@transaction.atomic` to ensure all-or-nothing operations.

### 3. Pessimistic Locking
`SELECT FOR UPDATE` prevents race conditions at database level.

### 4. Error Handling
Different errors return different status codes:
- 400: Bad input, seats unavailable
- 409: Concurrency conflict (optimistic)
- 402: Payment failed
- 500: Unexpected error

### 5. Timeouts
Locked seats must be released if payment not completed in time.

---

## Next Steps

**Continue to:** [10_TICKET_MANAGEMENT_GUIDE.md](./10_TICKET_MANAGEMENT_GUIDE.md)

This guide covers viewing tickets, cancellations, and refunds.
