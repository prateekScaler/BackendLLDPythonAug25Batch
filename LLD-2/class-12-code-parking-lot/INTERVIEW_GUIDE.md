# Interview Guide - Parking Lot System

## Quick Reference for 45-Minute Interview

### Time Allocation

- **0-5 min**: Clarify requirements, draw basic diagram
- **5-20 min**: Write core models and enums
- **20-35 min**: Implement key services (TicketService, PaymentService)
- **35-40 min**: Write 2-3 basic tests
- **40-45 min**: Discuss extensions and design decisions

---

## Essential Code to Write First

### 1. Enums (2 minutes)

```python
from enum import Enum

class VehicleType(Enum):
    CAR = "CAR"
    BIKE = "BIKE"
    TRUCK = "TRUCK"

class SpotType(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

class SpotStatus(Enum):
    FREE = "FREE"
    OCCUPIED = "OCCUPIED"
```

### 2. Core Models (5 minutes)

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Vehicle:
    license_plate: str
    vehicle_type: VehicleType

@dataclass
class ParkingSpot:
    id: str
    spot_number: int
    spot_type: SpotType
    status: SpotStatus = SpotStatus.FREE

    def is_available(self) -> bool:
        return self.status == SpotStatus.FREE

@dataclass
class ParkingTicket:
    ticket_id: str
    vehicle: Vehicle
    parking_spot: ParkingSpot
    entry_time: datetime
```

### 3. Simple Repository (3 minutes)

```python
class ParkingSpotRepository:
    def __init__(self):
        self._spots = {}

    def save(self, spot):
        self._spots[spot.id] = spot
        return spot

    def find_available(self):
        return [s for s in self._spots.values() if s.is_available()]
```

### 4. Core Service (8 minutes)

```python
class TicketService:
    def __init__(self, spot_repo, vehicle_repo, ticket_repo):
        self.spot_repo = spot_repo
        self.vehicle_repo = vehicle_repo
        self.ticket_repo = ticket_repo

    def issue_ticket(self, license_plate, vehicle_type):
        # Find available spot
        spots = self.spot_repo.find_available()
        spot = self._find_matching_spot(spots, vehicle_type)

        if not spot:
            raise Exception("No spot available")

        # Mark as occupied
        spot.status = SpotStatus.OCCUPIED
        self.spot_repo.save(spot)

        # Create ticket
        ticket = ParkingTicket(
            ticket_id=f"TKT-{len(self.ticket_repo._tickets) + 1}",
            vehicle=Vehicle(license_plate, vehicle_type),
            parking_spot=spot,
            entry_time=datetime.now()
        )

        self.ticket_repo.save(ticket)
        return ticket

    def _find_matching_spot(self, spots, vehicle_type):
        # Simple mapping
        spot_map = {
            VehicleType.BIKE: SpotType.SMALL,
            VehicleType.CAR: SpotType.MEDIUM,
            VehicleType.TRUCK: SpotType.LARGE
        }
        required_type = spot_map[vehicle_type]

        for spot in spots:
            if spot.spot_type == required_type:
                return spot
        return None
```

### 5. Basic Test (3 minutes)

```python
import unittest

class TestTicketService(unittest.TestCase):
    def setUp(self):
        self.spot_repo = ParkingSpotRepository()
        self.vehicle_repo = VehicleRepository()
        self.ticket_repo = TicketRepository()
        self.service = TicketService(
            self.spot_repo, self.vehicle_repo, self.ticket_repo
        )

        # Add test spot
        spot = ParkingSpot("1", 1, SpotType.MEDIUM)
        self.spot_repo.save(spot)

    def test_issue_ticket(self):
        ticket = self.service.issue_ticket("KA01AB1234", VehicleType.CAR)

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.parking_spot.status, SpotStatus.OCCUPIED)
```

---

## Key Points to Mention

### Design Patterns Used
1. **Strategy Pattern** - For spot allocation and pricing
2. **Repository Pattern** - For data access abstraction
3. **Service Layer** - For business logic

### SOLID Principles
- **Single Responsibility**: Each class has one job
- **Open/Closed**: Can add new strategies without modifying existing code
- **Dependency Injection**: Services depend on abstractions (repositories)

### Scalability Considerations
- Replace in-memory storage with database
- Add caching layer (Redis) for available spots
- Use message queues for async operations
- Implement distributed locking for concurrency

---

## Common Interview Questions & Answers

### Q: How do you handle concurrent bookings?

**A**: "I'd implement optimistic locking with version numbers in the database. When updating a spot status, we check if the version matches. If not, the transaction fails and we retry or show 'spot no longer available'."

```python
# Pseudo-code
def occupy_spot(spot_id, current_version):
    query = """
        UPDATE parking_spot
        SET status = 'OCCUPIED', version = version + 1
        WHERE id = ? AND version = ? AND status = 'FREE'
    """
    rows_affected = execute(query, spot_id, current_version)

    if rows_affected == 0:
        raise ConcurrentModificationException()
```

### Q: How would you add support for reserved parking?

**A**: "I'd add a ReservationService with a reservation_start_time and reservation_end_time. When allocating spots, the strategy would first check if any reserved spots are available for the current time window."

### Q: How do you prevent payment fraud?

**A**: "I'd implement:
1. Idempotency keys for payment requests
2. Payment gateway integration with 3D secure
3. Audit logs for all payment attempts
4. Rate limiting on payment endpoints
5. Token-based authentication"

### Q: How would you handle pricing for weekends/peak hours?

**A**: "I'd create a DynamicPricingStrategy that checks the current time and applies multipliers:

```python
class DynamicPricingStrategy(PricingStrategy):
    def calculate_fee(self, entry_time, exit_time, spot_type):
        base_fee = self.base_strategy.calculate_fee(...)

        if self.is_weekend(exit_time):
            base_fee *= 1.5
        if self.is_peak_hour(exit_time):
            base_fee *= 1.2

        return base_fee
```

---

## Code Structure Shortcuts

### If time is running out, focus on:
1. ✅ Core models (Vehicle, Spot, Ticket)
2. ✅ One service (TicketService)
3. ✅ One test (happy path)
4. ✅ Discuss the rest verbally

### What you can skip:
- ❌ Multiple strategies (just implement one)
- ❌ Invoice generation (focus on payment)
- ❌ Multiple test files (1 file with 3 tests is enough)
- ❌ Complex error handling (basic exceptions are fine)

---

## Interview Communication Tips

### While Coding
- **Think aloud**: "I'm creating a repository pattern here for data access abstraction"
- **Ask questions**: "Should we support hourly or daily pricing?"
- **State assumptions**: "I'm assuming we only need in-memory storage for now"

### When Stuck
- **Break it down**: "Let me start with the simplest case - a single spot and vehicle"
- **Draw it out**: "Can I quickly sketch the flow?"
- **Propose alternatives**: "We could do this with a simple list or use a priority queue"

### Finishing Strong
- **Summarize**: "So we have models, services, and tests covering the main flows"
- **Acknowledge gaps**: "In production, I'd add database transactions and proper error handling"
- **Show extensibility**: "We can easily add new pricing strategies by implementing the interface"

---

## Red Flags to Avoid

❌ **Don't:**
- Write everything in one class
- Use global variables
- Ignore error handling completely
- Write code without explaining
- Try to make it perfect (working code > perfect code)

✅ **Do:**
- Use meaningful variable names
- Keep methods short and focused
- Write at least one test
- Explain your design choices
- Ask clarifying questions

---

## Sample Interview Timeline

**Minute 0-5: Requirements**
- "Can spots accommodate multiple vehicle types?"
- "Is pricing fixed or dynamic?"
- "Do we need to support reservations?"
- "Should we track who issued the ticket?"

**Minute 5-10: Design**
- Draw class diagram on whiteboard
- Explain relationships
- Mention design patterns

**Minute 10-25: Core Implementation**
- Models and enums
- Main service logic
- Repository for storage

**Minute 25-35: Payment Logic**
- Payment service
- Simple pricing strategy

**Minute 35-40: Tests**
- Happy path test
- Error case test

**Minute 40-45: Discussion**
- Scalability
- Database design
- Edge cases
- Improvements

---

## Quick Copy-Paste Snippets

### Exception Classes
```python
class ParkingLotException(Exception):
    pass

class NoSpotAvailableException(ParkingLotException):
    def __init__(self, vehicle_type):
        super().__init__(f"No spot available for {vehicle_type}")
```

### UUID Generation
```python
import uuid

ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
```

### Date Handling
```python
from datetime import datetime, timedelta
import math

duration = exit_time - entry_time
hours = math.ceil(duration.total_seconds() / 3600)
```

---

## Remember

- **Working code > Perfect code**
- **Tests show you care about quality**
- **Communication > Silent coding**
- **Simple solutions first, optimize later**

Good luck! 🚀
