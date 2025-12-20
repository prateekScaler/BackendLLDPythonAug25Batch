# Design Parking Lot

## Overview

A parking lot system manages vehicle parking in a multi-floor facility. It tracks available spots, assigns spots to vehicles, calculates parking fees, and handles entry/exit.

**Key Components:**
- Multiple floors
- Different spot types (Compact, Regular, Large)
- Different vehicle types (Bike, Car, Truck)
- Entry/Exit gates
- Ticketing and payment

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

1. How many floors and spots per floor?
2. What vehicle types are supported?
3. Pricing model (flat rate vs hourly)?
4. Reserved/VIP parking?
5. Multiple entry/exit points?
6. Electric vehicle charging spots?

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

1. Parking lot has multiple floors.
2. Each floor has different types of spots.
3. System tracks available spots by type.
4. Vehicle gets ticket on entry.
5. Spot is assigned based on vehicle type.
6. Fee calculated based on duration.
7. Payment processed on exit.
8. Display shows available spots per floor.

</details>

---

## Class Diagram

**Think about:**
- ParkingLot → Floor → Spot hierarchy
- Vehicle types and Spot types compatibility
- Ticket for tracking
- Fee calculation strategy

**Design Question: Spot-Vehicle Compatibility**
```
Which vehicles can park in which spots?

| Spot     | Bike | Car | Truck |
|----------|------|-----|-------|
| Compact  |      |     |       |
| Regular  |      |     |       |
| Large    |      |     |       |

Fill in and explain your model:

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

**1. Spot Assignment Strategy**
```
Multiple spots available. Which one to assign?

Options: Nearest to entry, First available, Spread evenly

Your choice:

```

**2. Pricing Model**
```
Different rates for different vehicle types?
Hourly vs daily rate?

Your approach:

```

**3. Handling Full Parking Lot**
```
What happens when lot is full?

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
<summary><strong>Hint 1: Spot and Vehicle Hierarchy</strong></summary>

```python
class VehicleType(Enum):
    BIKE = "bike"
    CAR = "car"
    TRUCK = "truck"

class SpotType(Enum):
    COMPACT = "compact"   # Bikes only
    REGULAR = "regular"   # Bikes, Cars
    LARGE = "large"       # All vehicles

class ParkingSpot:
    id: str
    floor: int
    spot_number: str
    type: SpotType
    is_occupied: bool
    vehicle: Optional[Vehicle]

    def can_fit(self, vehicle: Vehicle) -> bool:
        if self.type == SpotType.COMPACT:
            return vehicle.type == VehicleType.BIKE
        elif self.type == SpotType.REGULAR:
            return vehicle.type in [VehicleType.BIKE, VehicleType.CAR]
        else:  # LARGE
            return True
```

</details>

<details>
<summary><strong>Hint 2: Ticket System</strong></summary>

```python
class ParkingTicket:
    id: str
    vehicle: Vehicle
    spot: ParkingSpot
    entry_time: datetime
    exit_time: Optional[datetime]
    fee: Optional[int]
    is_paid: bool

    def calculate_fee(self) -> int:
        duration = (self.exit_time or datetime.now()) - self.entry_time
        hours = math.ceil(duration.total_seconds() / 3600)
        return hours * self.get_hourly_rate()

    def get_hourly_rate(self) -> int:
        rates = {
            VehicleType.BIKE: 10,
            VehicleType.CAR: 20,
            VehicleType.TRUCK: 30
        }
        return rates[self.vehicle.type]
```

</details>

<details>
<summary><strong>Hint 3: Parking Lot Structure</strong></summary>

```
┌─────────────────────────────┐
│        ParkingLot           │
├─────────────────────────────┤
│ - id                        │
│ - name                      │
│ - floors[]                  │
│ - entry_panels[]            │
│ - exit_panels[]             │
├─────────────────────────────┤
│ + getAvailableSpots(type)   │
│ + parkVehicle(vehicle)      │
│ + unparkVehicle(ticket)     │
│ + isFull()                  │
└─────────────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────────────┐
│          Floor              │
├─────────────────────────────┤
│ - floor_number              │
│ - spots[]                   │
├─────────────────────────────┤
│ + getAvailableSpots(type)   │
│ + findSpotForVehicle(v)     │
└─────────────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────────────┐
│       ParkingSpot           │
├─────────────────────────────┤
│ - id                        │
│ - spot_number               │
│ - type: SpotType            │
│ - is_occupied               │
│ - vehicle                   │
├─────────────────────────────┤
│ + canFit(vehicle)           │
│ + park(vehicle)             │
│ + unpark()                  │
└─────────────────────────────┘
```

</details>

<details>
<summary><strong>Hint 4: Entry/Exit Flow</strong></summary>

```python
class ParkingLot:
    def park_vehicle(self, vehicle: Vehicle) -> ParkingTicket:
        # Find available spot
        spot = self.find_available_spot(vehicle)
        if not spot:
            raise ParkingFullError()

        # Park vehicle
        spot.park(vehicle)

        # Create ticket
        ticket = ParkingTicket(
            vehicle=vehicle,
            spot=spot,
            entry_time=datetime.now()
        )
        return ticket

    def unpark_vehicle(self, ticket: ParkingTicket) -> int:
        ticket.exit_time = datetime.now()
        fee = ticket.calculate_fee()

        # Free up spot
        ticket.spot.unpark()

        return fee

    def find_available_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        for floor in self.floors:
            for spot in floor.spots:
                if not spot.is_occupied and spot.can_fit(vehicle):
                    return spot
        return None
```

</details>
