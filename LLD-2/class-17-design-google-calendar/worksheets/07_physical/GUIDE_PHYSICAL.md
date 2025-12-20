# Category Guide: Real-world Physical Systems

## Overview

Physical system LLD problems model **real-world entities with constraints**. They test resource allocation, state management, and handling of physical constraints (capacity, proximity, etc.).

---

## Common Entities

| Entity | Purpose | Example |
|--------|---------|---------|
| Resource | Physical item being managed | Parking spot, Elevator, Product slot |
| Controller | Manages resources | ParkingLotManager, ElevatorController |
| Request | User's need | ParkRequest, ElevatorRequest |
| Ticket/Token | Proof of allocation | ParkingTicket |

---

## Key Design Patterns

### 1. Strategy Pattern - For Allocation
```
                    ┌───────────────────────┐
                    │ AllocationStrategy    │ (ABC)
                    │ + allocate(request)   │
                    └───────────┬───────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│ NearestFirst  │      │ FirstAvailable│      │ SpreadEvenly  │
└───────────────┘      └───────────────┘      └───────────────┘
```

### 2. State Pattern - For Resource States
```
                    ┌─────────────────┐
                    │  ElevatorState  │ (ABC)
                    │  + move()       │
                    │  + stop()       │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│     Idle      │   │   MovingUp    │   │  MovingDown   │
└───────────────┘   └───────────────┘   └───────────────┘
```

### 3. Factory Pattern - For Resource Types
```
class SpotFactory:
    def create_spot(type, floor, number):
        if type == "COMPACT": return CompactSpot(floor, number)
        if type == "REGULAR": return RegularSpot(floor, number)
        if type == "LARGE": return LargeSpot(floor, number)
```

---

## System 1: Parking Lot

### Class Hierarchy
```
┌─────────────────────┐
│    ParkingLot       │
├─────────────────────┤
│ - floors[]          │
│ - entry_panels[]    │
│ - exit_panels[]     │
│ + getAvailableSpot()│
│ + parkVehicle()     │
│ + unparkVehicle()   │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐       ┌─────────────────────┐
│      Floor          │       │    ParkingSpot      │ (ABC)
├─────────────────────┤       ├─────────────────────┤
│ - floor_number      │       │ - id                │
│ - spots[]           │──────▶│ - floor             │
│ + getAvailableSpots()       │ - is_occupied       │
└─────────────────────┘       │ - vehicle           │
                              │ + canFit(vehicle)   │
                              └─────────┬───────────┘
                                        │
                        ┌───────────────┼───────────────┐
                        ▼               ▼               ▼
                   Compact         Regular          Large
                    Spot            Spot            Spot

┌─────────────────────┐
│      Vehicle        │ (ABC)
├─────────────────────┤
│ - license_plate     │
│ - type              │
│ + getType()         │
└─────────┬───────────┘
          │
    ┌─────┼─────┬─────────┐
    ▼     ▼     ▼         ▼
  Bike   Car   Truck    Bus
```

### Spot-Vehicle Compatibility
```
| Spot Type | Bike | Car | Truck | Bus |
|-----------|------|-----|-------|-----|
| Compact   |  ✓   |  ✗  |   ✗   |  ✗  |
| Regular   |  ✓   |  ✓  |   ✗   |  ✗  |
| Large     |  ✓   |  ✓  |   ✓   |  ✓  |
```

---

## System 2: Elevator

### Class Design
```
┌─────────────────────────┐
│   ElevatorController    │
├─────────────────────────┤
│ - elevators[]           │
│ - pending_requests[]    │
│ + requestElevator(floor, direction)
│ + assignElevator(request)
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│       Elevator          │
├─────────────────────────┤
│ - id                    │
│ - current_floor         │
│ - direction             │
│ - state                 │
│ - destinations[]        │
│ + move()                │
│ + addDestination(floor) │
│ + openDoors()           │
└─────────────────────────┘
```

### Elevator Scheduling Algorithms

**1. FCFS (First Come First Serve)**
- Simple, but inefficient
- Elevator goes to floors in request order

**2. SCAN (Elevator Algorithm)**
- Move in one direction, serve all requests
- Reverse at end
- Like a disk seek algorithm

**3. LOOK**
- Like SCAN but reverse when no more requests in current direction

```python
class ScanScheduler:
    def get_next_floor(self, elevator, requests):
        current = elevator.current_floor
        direction = elevator.direction

        # Get requests in current direction
        if direction == Direction.UP:
            ahead = [r for r in requests if r.floor > current]
            if ahead:
                return min(ahead, key=lambda r: r.floor).floor
            # Reverse direction
            return None  # Signal to reverse

        # Similar for DOWN
```

---

## System 3: Vending Machine

### State Machine
```
     ┌─────────────────────────────────────────────────────────┐
     │                                                         │
     ▼                                                         │
┌─────────┐  insertMoney  ┌────────────┐  selectProduct  ┌─────────────┐
│  Idle   │ ────────────▶ │ HasMoney   │ ─────────────▶  │ Dispensing  │
└─────────┘               └────────────┘                 └─────────────┘
     ▲                          │                              │
     │                          │ cancel                       │ done
     │                          ▼                              │
     │                    ┌────────────┐                       │
     └────────────────────│  Refunding │◀──────────────────────┘
                          └────────────┘
```

### Class Design
```
┌─────────────────────────┐
│    VendingMachine       │
├─────────────────────────┤
│ - inventory: Map        │
│ - current_balance       │
│ - state: State          │
│ + insertMoney(amount)   │
│ + selectProduct(code)   │
│ + dispense()            │
│ + refund()              │
└─────────────────────────┘

┌─────────────────────────┐
│       Product           │
├─────────────────────────┤
│ - code: String          │
│ - name: String          │
│ - price: int            │
└─────────────────────────┘

┌─────────────────────────┐
│        Slot             │
├─────────────────────────┤
│ - code: String          │
│ - product: Product      │
│ - quantity: int         │
└─────────────────────────┘
```

---

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| No spot types | All spots same | Create hierarchy |
| Singleton abuse | Hard to test | Use dependency injection |
| Missing ticket | Can't track duration | Issue ticket on entry |
| No floor concept | Can't find nearest | Add floor hierarchy |
| Elevator god class | Does everything | Extract Scheduler, State |

---

## Coding Hacks for Demo

### 1. Parking Spot Finder
```python
def find_nearest_spot(vehicle, entry_floor):
    for floor in sorted(floors, key=lambda f: abs(f.number - entry_floor)):
        for spot in floor.spots:
            if spot.is_available() and spot.can_fit(vehicle):
                return spot
    return None
```

### 2. Parking Fee Calculation
```python
class FeeCalculator:
    RATES = {
        VehicleType.BIKE: 10,    # per hour
        VehicleType.CAR: 20,
        VehicleType.TRUCK: 30,
    }

    def calculate(self, ticket):
        hours = ceil((exit_time - ticket.entry_time).seconds / 3600)
        return hours * self.RATES[ticket.vehicle.type]
```

### 3. Elevator Direction Logic
```python
def should_stop(self, floor):
    # Stop if this floor is in our destinations
    if floor in self.destinations:
        return True
    # Stop if someone on this floor wants to go our direction
    if self.has_pickup_at(floor, self.direction):
        return True
    return False
```

### 4. Vending Machine Inventory
```python
class Inventory:
    def __init__(self):
        self.slots = {}  # code -> Slot

    def add_product(self, code, product, quantity):
        self.slots[code] = Slot(code, product, quantity)

    def dispense(self, code):
        if self.slots[code].quantity > 0:
            self.slots[code].quantity -= 1
            return self.slots[code].product
        raise OutOfStockError()
```

---

## API Design

### Parking Lot
```
POST   /parking/entry              # Vehicle entry, get ticket
POST   /parking/exit               # Vehicle exit, pay & leave
GET    /parking/spots/available    # Check availability
GET    /parking/ticket/{id}        # Get ticket details

# Entry Request
POST /parking/entry
{
    "vehicle_type": "CAR",
    "license_plate": "KA-01-AB-1234"
}

# Response
{
    "ticket_id": "T-12345",
    "spot": {"floor": 2, "number": "A-15"},
    "entry_time": "2024-01-15T10:30:00Z"
}
```

### Elevator
```
POST   /elevator/request           # Request elevator
GET    /elevator/{id}/status       # Get elevator status

# Request
POST /elevator/request
{
    "floor": 5,
    "direction": "UP"
}
```

### Vending Machine
```
POST   /vending/money              # Insert money
POST   /vending/select             # Select product
POST   /vending/cancel             # Cancel & refund
GET    /vending/products           # List products
```

---

## Interview Questions to Expect

1. "How would you handle **multiple entry/exit points**?"
   → Track entry point in ticket, calculate fee based on nearest exit

2. "How to implement **reserved parking**?"
   → Add `is_reserved` flag, `reserved_for` user reference

3. "How would you add **EV charging spots**?"
   → Create `ChargingSpot` subclass, track charging state

4. "How to optimize **elevator wait time**?"
   → Implement LOOK algorithm, consider load balancing

5. "How to handle **out of stock** in vending machine?"
   → State check before dispensing, notify admin

---

## Checklist Before Interview

- [ ] Can draw Spot/Vehicle hierarchy
- [ ] Know parking fee calculation
- [ ] Understand elevator scheduling (SCAN/LOOK)
- [ ] Can implement vending machine states
- [ ] Know how to handle capacity constraints
- [ ] Can explain nearest spot allocation
- [ ] Understand ticket lifecycle
