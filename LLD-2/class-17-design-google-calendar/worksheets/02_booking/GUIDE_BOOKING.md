# Category Guide: Booking & Reservation Systems

## Overview

Booking systems are among the most asked LLD problems. They test your understanding of **concurrency, seat/resource selection, and payment flows**. The core challenge is handling multiple users trying to book the same resource simultaneously.

---

## Common Entities

| Entity | Purpose | Example |
|--------|---------|---------|
| User/Customer | Person making booking | Registered user, Guest |
| Resource | What's being booked | Seat, Room, Flight seat |
| Booking/Reservation | The actual booking record | MovieBooking, HotelReservation |
| Schedule/Show | Time-based availability | Movie show, Flight schedule |
| Payment | Payment processing | CreditCard, UPI, Wallet |
| Venue/Location | Physical location | Theater, Hotel, Airport |

---

## Key Design Patterns

### 1. State Pattern - For Booking Lifecycle
```
                    ┌─────────────────┐
                    │  BookingState   │ (ABC)
                    │  + proceed()    │
                    │  + cancel()     │
                    └────────┬────────┘
                             │
    ┌────────────────────────┼────────────────────┐
    ▼                        ▼                    ▼
┌──────────┐         ┌───────────┐        ┌───────────┐
│ Pending  │ ──────▶ │ Confirmed │ ──────▶│ Completed │
└──────────┘         └───────────┘        └───────────┘
     │                     │
     ▼                     ▼
┌──────────┐         ┌───────────┐
│ Expired  │         │ Cancelled │
└──────────┘         └───────────┘
```

### 2. Strategy Pattern - For Pricing
```
class PricingStrategy(ABC):
    def calculate_price(base_price, booking) -> float

class WeekendPricing(PricingStrategy): ...
class PeakHourPricing(PricingStrategy): ...
class EarlyBirdPricing(PricingStrategy): ...
```

### 3. Factory Pattern - For Seat Types
```
class SeatFactory:
    def create_seat(type):
        if type == "REGULAR": return RegularSeat()
        if type == "PREMIUM": return PremiumSeat()
        if type == "VIP": return VIPSeat()
```

---

## Class Design Tips

### Seat/Resource Hierarchy
```
         ┌────────────┐
         │    Seat    │ (ABC)
         │ - id       │
         │ - row      │
         │ - number   │
         │ + getPrice()│
         └─────┬──────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
 Regular    Premium      VIP
  Seat       Seat       Seat
```

### Show/Schedule Design
```
┌─────────────────────┐       ┌─────────────────────┐
│       Movie         │       │        Show         │
├─────────────────────┤       ├─────────────────────┤
│ - id                │       │ - id                │
│ - title             │◀──────│ - movie_id          │
│ - duration          │       │ - screen_id         │
│ - language          │       │ - start_time        │
└─────────────────────┘       │ - end_time          │
                              │ - seat_status: Map  │
                              └─────────────────────┘
```

### Booking Entity
```
┌─────────────────────────────┐
│          Booking            │
├─────────────────────────────┤
│ - id                        │
│ - user_id                   │
│ - show_id                   │
│ - seats: List[Seat]         │
│ - status: BookingStatus     │
│ - total_amount              │
│ - payment_id                │
│ - booked_at                 │
│ - expires_at (for temp lock)│
└─────────────────────────────┘
```

---

## Critical: Handling Concurrency

### The Problem
```
User A selects Seat 5 ──┐
                        ├──▶ Both see seat as available!
User B selects Seat 5 ──┘
```

### Solutions

**1. Pessimistic Locking (Temporary Hold)**
```
1. User selects seats → Lock seats for 10 mins
2. If payment succeeds → Confirm booking
3. If timeout/failure → Release seats
```

**2. Optimistic Locking (Version check)**
```sql
UPDATE seats SET status='BOOKED', version=version+1
WHERE id IN (1,2,3) AND status='AVAILABLE' AND version=5
-- Check affected rows == number of seats
```

**3. Database Transaction**
```python
with transaction():
    seats = Seat.select_for_update(ids=[1,2,3])  # Row lock
    if all(s.status == 'AVAILABLE' for s in seats):
        for s in seats:
            s.status = 'BOOKED'
        create_booking(...)
    else:
        raise SeatUnavailableError()
```

---

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| No seat locking | Double booking | Temporary lock with expiry |
| Show in Movie class | Tight coupling | Separate Show entity |
| Price in Seat | Can't change pricing | Use PricingStrategy |
| No booking expiry | Orphaned pending bookings | Background job to expire |
| Missing status transitions | Invalid state changes | State pattern with guards |

---

## Coding Hacks for Demo

### 1. Seat Status Enum
```python
class SeatStatus(Enum):
    AVAILABLE = "available"
    LOCKED = "locked"      # Temporarily held
    BOOKED = "booked"
```

### 2. Quick Seat Map
```python
# For a show, track seat status
seat_status = {
    "A1": SeatStatus.AVAILABLE,
    "A2": SeatStatus.BOOKED,
    "A3": SeatStatus.LOCKED,
}
```

### 3. Booking with Expiry
```python
class Booking:
    def __init__(self, user, show, seats):
        self.status = BookingStatus.PENDING
        self.expires_at = datetime.now() + timedelta(minutes=10)

    def is_expired(self):
        return datetime.now() > self.expires_at and self.status == BookingStatus.PENDING
```

### 4. Price Calculation
```python
def calculate_total(seats, show):
    base = sum(seat.get_price() for seat in seats)
    # Apply show-time pricing
    if show.is_weekend():
        base *= 1.2
    if show.is_prime_time():
        base *= 1.1
    return base
```

---

## API Design

### Core Endpoints
```
# Discovery
GET    /movies                         # List movies
GET    /movies/{id}/shows              # Shows for a movie
GET    /shows/{id}/seats               # Available seats

# Booking Flow
POST   /bookings/initiate              # Lock seats, create pending booking
POST   /bookings/{id}/confirm          # Confirm after payment
DELETE /bookings/{id}                  # Cancel booking

# Payment
POST   /payments                       # Process payment
```

### Booking Flow
```
1. GET /shows/{id}/seats               → See available seats
2. POST /bookings/initiate             → Lock seats (10 min)
   {show_id, seat_ids}
   Response: {booking_id, amount, expires_at}
3. POST /payments                      → Pay
   {booking_id, payment_method, ...}
4. POST /bookings/{id}/confirm         → Confirm
```

### Seat Availability Response
```json
{
    "show_id": "show-123",
    "seats": [
        {"id": "A1", "row": "A", "number": 1, "type": "REGULAR", "status": "AVAILABLE", "price": 200},
        {"id": "A2", "row": "A", "number": 2, "type": "REGULAR", "status": "BOOKED", "price": 200},
        {"id": "B1", "row": "B", "number": 1, "type": "PREMIUM", "status": "AVAILABLE", "price": 350}
    ]
}
```

---

## Interview Questions to Expect

1. "How do you handle **two users booking same seat**?"
   → Pessimistic locking with timeout OR optimistic locking with version

2. "How would you add **seat selection UI hints**?"
   → Return seat layout with status, let UI render

3. "How would you implement **dynamic pricing**?"
   → Strategy pattern for pricing, factor in demand/time

4. "How to handle **partial refunds**?"
   → Cancellation policy based on time before show

5. "How to support **multiple theaters/cities**?"
   → Add City → Theater → Screen → Show hierarchy

---

## Checklist Before Interview

- [ ] Can explain seat locking mechanism
- [ ] Know booking state transitions
- [ ] Can handle concurrent bookings
- [ ] Understand Show vs Movie separation
- [ ] Can design seat hierarchy (Regular/Premium/VIP)
- [ ] Know payment flow integration points
- [ ] Can explain booking expiry handling
