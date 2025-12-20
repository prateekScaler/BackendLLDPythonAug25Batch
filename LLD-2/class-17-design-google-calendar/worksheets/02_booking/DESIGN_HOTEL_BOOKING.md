# Design Hotel Booking System

## Overview

A hotel booking system allows users to search for hotels, check room availability for date ranges, and make reservations. The system manages hotels, room types, inventory, and bookings.

**Key Difference from Movie Booking:** Date ranges, not single time slots.

---

## Expectations

* Code should be functionally correct.
* Code should be modular and readable.
* Code should be extensible and scalable.
* Code should have good OOP design principles.

---

## Requirements Gathering

What are some questions you would ask?

```
1.
2.
3.
4.
5.
```

<details>
<summary><strong>Sample clarifying questions</strong></summary>

1. Can users book multiple rooms in one reservation?
2. How is room inventory managed (specific room vs room type)?
3. What's the cancellation policy?
4. Are there different rate types (refundable, non-refundable)?
5. How are amenities handled?
6. Is there dynamic pricing based on demand/season?

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

1. Users can search hotels by location, dates, and guest count.
2. System shows available room types with prices.
3. Users can select room type and quantity.
4. System checks availability for the entire date range.
5. Users can make reservation with guest details.
6. Booking confirmation sent to user.
7. Users can cancel with applicable charges.
8. Hotel admin can manage room inventory and pricing.

</details>

---

## Class Diagram

**Think about:**
- Hotel → RoomType → Room (inventory)
- Booking spans multiple dates
- Room availability per date

**Critical Question: How to track availability?**
```
Option A: Track each room's bookings
Option B: Track inventory count per room type per date
Option C: Both

Your choice:

```

List your classes:

```
Class 1:

Class 2:

Class 3:

Class 4:

Class 5:
```

Draw the class diagram:

```




```

---

## Key Design Decisions

**1. Inventory Model**
```
How to check: "3 Deluxe rooms available Jan 15-18"?

Your approach:

```

**2. Overlapping Bookings**
```
Booking A: Jan 15-18
Booking B: Jan 17-20
How to detect conflict?

```

**3. Pricing Model**
```
Base price + seasonal rate + weekend rate + taxes

How to structure?

```

---

## API Design

```
1.
2.
3.
4.
```

---

## Hints

<details>
<summary><strong>Hint 1: Inventory Tracking</strong></summary>

```python
class RoomTypeInventory:
    """Track available count per room type per date"""
    room_type_id: str
    date: date
    total_rooms: int
    booked_rooms: int

    @property
    def available(self):
        return self.total_rooms - self.booked_rooms

def check_availability(room_type_id, check_in, check_out, count):
    dates = get_date_range(check_in, check_out)
    for d in dates:
        inventory = RoomTypeInventory.get(room_type_id, d)
        if inventory.available < count:
            return False
    return True
```

</details>

<details>
<summary><strong>Hint 2: Date Range Overlap</strong></summary>

```python
def dates_overlap(a_start, a_end, b_start, b_end):
    return a_start < b_end and b_start < a_end

# Check-out date is NOT included in stay
# Jan 15-18 means nights of 15, 16, 17
```

</details>

<details>
<summary><strong>Hint 3: Class Structure</strong></summary>

```
┌─────────────┐      ┌─────────────┐
│    Hotel    │      │  RoomType   │
├─────────────┤      ├─────────────┤
│ - id        │ 1:N  │ - id        │
│ - name      │─────▶│ - name      │
│ - location  │      │ - max_guests│
│ - amenities │      │ - base_price│
└─────────────┘      │ - amenities │
                     └─────────────┘
                           │
                           │ 1:N
                           ▼
                     ┌─────────────────┐
                     │ RoomInventory   │
                     ├─────────────────┤
                     │ - room_type_id  │
                     │ - date          │
                     │ - total         │
                     │ - booked        │
                     └─────────────────┘

┌─────────────────────────┐
│       Reservation       │
├─────────────────────────┤
│ - id                    │
│ - hotel_id              │
│ - room_type_id          │
│ - check_in              │
│ - check_out             │
│ - room_count            │
│ - guest_details[]       │
│ - total_amount          │
│ - status                │
└─────────────────────────┘
```

</details>
