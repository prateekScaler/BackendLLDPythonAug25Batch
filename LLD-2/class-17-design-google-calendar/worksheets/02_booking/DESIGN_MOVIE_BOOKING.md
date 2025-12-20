# Design Movie Ticket Booking (BookMyShow)

## Overview

A movie ticket booking system allows users to browse movies, view showtimes, select seats, and book tickets. The system manages theaters, screens, shows, and handles concurrent booking requests.

**Key Participants:**
- **Customer** - Browses movies, books tickets
- **Theater Admin** - Manages shows, screens, pricing
- **System** - Handles seat locking, payments

---

## Expectations

* Code should be functionally correct.
* Code should be modular and readable. Clean and professional level code.
* Code should be extensible and scalable.
* Code should have good OOP design principles.

---

## Requirements Gathering

What are some questions you would ask to gather requirements?

```
1.
2.
3.
4.
5.
```

<details>
<summary><strong>Sample clarifying questions</strong></summary>

1. Can users select specific seats or is it auto-assigned?
2. How long are seats held during booking process?
3. Are there different seat types (Regular, Premium, VIP)?
4. Can multiple users book for same show simultaneously?
5. Is there dynamic pricing (weekend, peak hours)?
6. Can bookings be cancelled? Refund policy?
7. Multiple payment methods supported?

</details>

---

## Requirements

What will be 8-10 requirements of the system?

```
1.
2.
3.
4.
5.
6.
7.
8.
```

<details>
<summary><strong>Click to see requirements</strong></summary>

1. Users can browse movies currently showing.
2. Users can view available shows for a movie at different theaters.
3. Users can see seat layout and availability for a show.
4. Users can select seats and initiate booking.
5. Selected seats are temporarily locked (10 mins) during payment.
6. Booking is confirmed after successful payment.
7. Different seat types have different prices.
8. Users can cancel booking (with cancellation policy).
9. System prevents double booking of same seat.
10. Users receive booking confirmation with ticket details.

</details>

---

## Use Case Diagrams

### Actors

```
1.
2.
3.
```

### Use Cases

#### Customer
```
1.
2.
3.
4.
5.
```

#### Theater Admin
```
1.
2.
3.
```

---

## Class Diagram

**Think about:**
- Movie vs Show (same movie, different times)
- Theater → Screen → Show → Seats
- Booking lifecycle
- Seat status management

List your classes:

```
Class 1:

Class 2:

Class 3:

Class 4:

Class 5:

Class 6:

Class 7:
```

**Design Question: How to prevent double booking?**
```
Your approach:

```

Draw the class diagram:

```




```

---

## Key Design Decisions

**1. Seat Locking Mechanism**
```
How do you handle: User A and User B both try to book Seat 5?

Your approach:

```

**2. Show vs Movie**
```
Why separate these? What belongs where?

```

**3. Pricing Strategy**
```
How to handle: Regular=$10, Premium=$15, Weekend=+20%

```

---

## API Design

```
1.
2.
3.
4.
5.
```

---

## Hints

<details>
<summary><strong>Hint 1: Core Entities</strong></summary>

```
Movie → has many Shows
Theater → has many Screens
Screen → has many Seats, hosts Shows
Show → Movie + Screen + Time + SeatStatus
Booking → User + Show + Seats + Payment
```

</details>

<details>
<summary><strong>Hint 2: Seat Status</strong></summary>

```python
class SeatStatus(Enum):
    AVAILABLE = "available"
    LOCKED = "locked"      # Temporarily held
    BOOKED = "booked"      # Confirmed

class ShowSeat:
    seat: Seat
    show: Show
    status: SeatStatus
    locked_until: Optional[datetime]
    booking_id: Optional[str]
```

</details>

<details>
<summary><strong>Hint 3: Booking Flow</strong></summary>

```
1. GET /shows/{id}/seats → Available seats
2. POST /bookings/initiate → Lock seats, return booking_id
   {show_id, seat_ids[]}
3. POST /payments → Process payment
4. POST /bookings/{id}/confirm → Confirm booking
   OR timeout → Release seats
```

</details>

<details>
<summary><strong>Hint 4: Concurrency Handling</strong></summary>

```python
def lock_seats(show_id, seat_ids, user_id):
    with db.transaction():
        seats = ShowSeat.select_for_update(show_id, seat_ids)
        if any(s.status != SeatStatus.AVAILABLE for s in seats):
            raise SeatsNotAvailableError()

        for seat in seats:
            seat.status = SeatStatus.LOCKED
            seat.locked_until = now() + timedelta(minutes=10)

        return create_pending_booking(seats, user_id)
```

</details>
