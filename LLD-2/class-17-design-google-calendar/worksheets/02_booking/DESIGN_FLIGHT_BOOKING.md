# Design Flight Booking System

## Overview

A flight booking system allows users to search flights, select seats, add passengers, and book tickets. The system manages airlines, flights, schedules, and generates PNR for bookings.

**Key Complexities:**
- Multiple passengers per booking
- Seat classes (Economy, Business, First)
- Connecting flights
- PNR generation

---

## Expectations

* Code should be functionally correct.
* Code should be modular and readable.
* Code should be extensible and scalable.
* Code should have good OOP design principles.

---

## Requirements Gathering

```
1.
2.
3.
4.
5.
```

<details>
<summary><strong>Sample clarifying questions</strong></summary>

1. One-way or round-trip bookings?
2. How are connecting flights handled?
3. What passenger details are required?
4. Seat selection mandatory or optional?
5. Baggage allowance per class?
6. Cancellation and refund policy?
7. Child/infant pricing?

</details>

---

## Requirements

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

1. Users can search flights by source, destination, date, passengers.
2. System shows available flights with prices per class.
3. Users can select flight and seat class.
4. Users can add passenger details (name, age, passport).
5. Optional seat selection from available seats.
6. System generates unique PNR on booking.
7. Booking confirmation with e-ticket.
8. Support for booking cancellation.

</details>

---

## Class Diagram

**Think about:**
- Flight vs FlightSchedule (same flight, different dates)
- Aircraft → Seat layout
- Booking → Passengers → Seats

**Design Question: Flight vs FlightSchedule**
```
AI-101 flies Delhi→Mumbai daily at 10 AM.
How to model?

```

List your classes:

```
Class 1:

Class 2:

Class 3:

Class 4:

Class 5:

Class 6:
```

Draw the class diagram:

```




```

---

## Key Design Decisions

**1. PNR Generation**
```
How to generate unique, readable PNR like "ABC123"?

Your approach:

```

**2. Multiple Passengers**
```
One booking, 3 passengers, different meal preferences.
How to model?

```

**3. Seat Classes & Pricing**
```
Same flight: Economy=$200, Business=$500, First=$1200
How to structure?

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
<summary><strong>Hint 1: Flight vs Schedule</strong></summary>

```python
class Flight:
    """Template - AI-101 Delhi→Mumbai"""
    flight_number: str
    airline: Airline
    source: Airport
    destination: Airport
    departure_time: time  # 10:00
    arrival_time: time    # 12:00
    aircraft_type: str

class FlightSchedule:
    """Actual instance - AI-101 on Jan 15"""
    flight: Flight
    date: date
    status: FlightStatus  # SCHEDULED, DELAYED, CANCELLED
    seats: List[ScheduledSeat]
```

</details>

<details>
<summary><strong>Hint 2: Booking Structure</strong></summary>

```
┌─────────────────────────┐
│       Booking           │
├─────────────────────────┤
│ - pnr: str              │
│ - flight_schedule_id    │
│ - passengers[]          │
│ - contact_email         │
│ - contact_phone         │
│ - total_amount          │
│ - status                │
│ - booked_at             │
└─────────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────────┐
│      Passenger          │
├─────────────────────────┤
│ - name                  │
│ - age                   │
│ - passport_number       │
│ - seat_class            │
│ - seat_number           │
│ - meal_preference       │
│ - baggage_weight        │
└─────────────────────────┘
```

</details>

<details>
<summary><strong>Hint 3: Seat Class Pricing</strong></summary>

```python
class SeatClass(Enum):
    ECONOMY = "economy"
    BUSINESS = "business"
    FIRST = "first"

class FlightPricing:
    flight_schedule_id: str
    seat_class: SeatClass
    base_price: int
    available_seats: int

# Query: Get prices for flight
prices = FlightPricing.query.filter(flight_schedule_id=X)
# Returns: [{class: ECONOMY, price: 200, available: 50}, ...]
```

</details>

<details>
<summary><strong>Hint 4: PNR Generation</strong></summary>

```python
import random
import string

def generate_pnr():
    """Generate 6-character alphanumeric PNR"""
    chars = string.ascii_uppercase + string.digits
    while True:
        pnr = ''.join(random.choices(chars, k=6))
        if not Booking.exists(pnr=pnr):
            return pnr
```

</details>
