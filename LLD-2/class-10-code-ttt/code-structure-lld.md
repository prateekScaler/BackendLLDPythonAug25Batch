# Python Project Structure for LLD/Machine Coding Interviews

## Quick Start Structure

### Minimal (Start Here)
```
project/
├── main.py              # Entry point - start here
├── models/              # Data classes & entities
└── services/            # Business logic
```

### Standard (Most Interviews)
```
project/
├── main.py              
├── models/              # Data classes & entities
├── enums/               # Enumerations & constants
├── services/            # Business logic
├── repositories/        # Data access layer
└── exceptions/          # Custom exceptions
```

### Complete (Show Advanced Design)
```
project/
├── main.py              
├── models/              # Data classes & entities
├── enums/               # Enumerations & constants
├── controllers/         # API/Input handlers
├── services/            # Business logic
├── repositories/        # Data access layer
├── exceptions/          # Custom exceptions
├── strategies/          # Strategy pattern implementations
├── factories/           # Factory pattern implementations
└── utils/               # Helper functions
```

## Core Folders (Priority Order)

### 1. **main.py** (Always First)
**Why**: Single entry point, demonstrates code organization immediately

```python
# main.py
from models.user import User
from services.booking_service import BookingService

def main():
    # Demo your system here
    service = BookingService()
    service.create_booking(...)

if __name__ == "__main__":
    main()
```

**Tips**:
- Write this first to clarify what you're building
- Add demo/test cases here
- Shows interviewer your system works

---

### 2. **models/** (Core Entities)
**Why**: Define your data structures early - everything depends on this

```python
# models/user.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: str
    name: str
    email: str
```
## Benefits of Using `@dataclass`

- **Reduces Boilerplate**: Auto-generates `__init__`, `__repr__`, `__eq__`, etc., making code cleaner.
- **Type Hints**: Enforces attribute types for better readability and tooling support.
- **Supports Default Values**: Easily set defaults for fields.
- **Immutability Option**: Use `frozen=True` for immutable instances.
- **Ordering Support**: Enable comparison methods with `order=True`.
- **Customization**: Fine-grained field control with `field()`.


**Tips**:
- Use `@dataclass` for speed (auto __init__, __repr__)
- Keep models dumb (just data, minimal logic)
- One class per file for clarity

---

### 3. **enums/** (Enumerations - Highly Recommended)
**Why**: Type safety, prevents magic strings, shows clean design

```python
# enums/vehicle_type.py
from enum import Enum

class VehicleType(Enum):
    CAR = "CAR"
    BIKE = "BIKE"
    TRUCK = "TRUCK"

# enums/booking_status.py
class BookingStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

# enums/payment_method.py
class PaymentMethod(Enum):
    CASH = "CASH"
    CARD = "CARD"
    UPI = "UPI"
```

**Tips**:
- Create early (right after models)
- One enum per file for clarity
- Use for: statuses, types, categories, modes
- Prevents typos: `BookingStatus.CONFIRMED` vs `"CONFIRMMED"`
- Interviewers love this - shows attention to design

---

### 4. **controllers/** (API/Input Layer - When Needed)
**Why**: Separates input handling from business logic - shows proper layering

```python
# controllers/booking_controller.py
class BookingController:
    def __init__(self, booking_service):
        self.service = booking_service
    
    def handle_create_booking(self, request_data):
        # Validate input
        user_id = request_data.get('user_id')
        slot_id = request_data.get('slot_id')
        
        if not user_id or not slot_id:
            return {"error": "Missing required fields"}
        
        # Delegate to service
        booking = self.service.create_booking(user_id, slot_id)
        return {"success": True, "booking_id": booking.id}
```

**When to use**:
- Systems with API endpoints (ride-sharing, food delivery)
- Multiple input sources (CLI, REST API)
- Need input validation before business logic

**Tips**:
- Controllers handle: validation, request parsing, response formatting
- Keep thin - just translate inputs/outputs
- All business logic stays in services
- Skip if direct function calls suffice

---

### 5. **services/** (Business Logic)
**Why**: Core functionality lives here - this is what interviewers evaluate

```python
# services/booking_service.py
class BookingService:
    def __init__(self):
        self.bookings = {}  # Simple in-memory storage
    
    def create_booking(self, user_id, slot_id):
        # Your business logic here
        pass
```

**Tips**:
- One service per major feature
- Keep methods focused (single responsibility)
- Start with in-memory storage (dict/list)

---

### 6. **repositories/** (Data Access Layer - Important!)
**Why**: Separates data access from business logic, shows SOLID principles

```python
# repositories/booking_repository.py
from typing import Optional, List
from models.booking import Booking

class BookingRepository:
    def __init__(self):
        self.bookings = {}  # In-memory: id -> Booking
        self.user_bookings = {}  # user_id -> [booking_ids]
    
    def save(self, booking: Booking) -> Booking:
        self.bookings[booking.id] = booking
        
        if booking.user_id not in self.user_bookings:
            self.user_bookings[booking.user_id] = []
        self.user_bookings[booking.user_id].append(booking.id)
        
        return booking
    
    def find_by_id(self, booking_id: str) -> Optional[Booking]:
        return self.bookings.get(booking_id)
    
    def find_by_user(self, user_id: str) -> List[Booking]:
        booking_ids = self.user_bookings.get(user_id, [])
        return [self.bookings[bid] for bid in booking_ids]
    
    def delete(self, booking_id: str) -> bool:
        if booking_id in self.bookings:
            del self.bookings[booking_id]
            return True
        return False
```

**Tips**:
- Use for standard CRUD operations (Create, Read, Update, Delete)
- Keeps services clean - they don't worry about data storage
- Easy to mock for testing
- Shows separation of concerns (bonus points!)
- Start simple with dict/list, mention "easily swappable with DB"

---

### 7. **exceptions/** (Custom Exceptions - Very Important!)
**Why**: Better error handling, cleaner code, shows professional design

```python
# exceptions/booking_exceptions.py
class BookingException(Exception):
    """Base exception for booking-related errors"""
    pass

class BookingNotFoundException(BookingException):
    def __init__(self, booking_id: str):
        self.booking_id = booking_id
        super().__init__(f"Booking {booking_id} not found")

class SlotNotAvailableException(BookingException):
    def __init__(self, slot_id: str):
        self.slot_id = slot_id
        super().__init__(f"Slot {slot_id} is not available")

class InvalidBookingStateException(BookingException):
    def __init__(self, message: str):
        super().__init__(message)

# exceptions/payment_exceptions.py
class PaymentException(Exception):
    """Base exception for payment-related errors"""
    pass

class InsufficientBalanceException(PaymentException):
    pass

class PaymentFailedException(PaymentException):
    pass
```

**Usage in service**:
```python
# services/booking_service.py
from exceptions.booking_exceptions import SlotNotAvailableException

class BookingService:
    def create_booking(self, user_id, slot_id):
        if not self.is_slot_available(slot_id):
            raise SlotNotAvailableException(slot_id)
        # ... rest of logic
```

**Tips**:
- Create hierarchy: Base exception → Specific exceptions
- Makes error handling explicit and type-safe
- Better than returning None or error codes
- Shows understanding of exception design
- Group related exceptions in same file

---

### 8. **strategies/** (Optional - Strategy Pattern)
**Why**: For algorithms that vary by context (pricing, sorting, matching)

```python
# strategies/pricing_strategy.py
from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, base_price: float, distance: float) -> float:
        pass

class SurgePricingStrategy(PricingStrategy):
    def __init__(self, surge_multiplier: float):
        self.surge_multiplier = surge_multiplier
    
    def calculate_price(self, base_price: float, distance: float) -> float:
        return base_price * distance * self.surge_multiplier

class FlatPricingStrategy(PricingStrategy):
    def calculate_price(self, base_price: float, distance: float) -> float:
        return base_price * distance

# Usage in service
class RideService:
    def __init__(self, pricing_strategy: PricingStrategy):
        self.pricing_strategy = pricing_strategy
    
    def calculate_fare(self, distance: float):
        return self.pricing_strategy.calculate_price(10, distance)
```

**When to use**:
- Multiple algorithms for same task (pricing, notifications, matching)
- Behavior needs to change at runtime
- Want to show design pattern knowledge

---

### 9. **factories/** (Optional - Factory Pattern)
**Why**: Centralize object creation logic

```python
# factories/vehicle_factory.py
from models.vehicle import Vehicle, Car, Bike, Truck
from enums.vehicle_type import VehicleType

class VehicleFactory:
    @staticmethod
    def create_vehicle(vehicle_type: VehicleType, number: str) -> Vehicle:
        if vehicle_type == VehicleType.CAR:
            return Car(number, capacity=4)
        elif vehicle_type == VehicleType.BIKE:
            return Bike(number, capacity=2)
        elif vehicle_type == VehicleType.TRUCK:
            return Truck(number, capacity=2)
        else:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")

# Usage
vehicle = VehicleFactory.create_vehicle(VehicleType.CAR, "KA-01-1234")
```

**When to use**:
- Complex object creation with many variations
- Creation logic shouldn't be in service/controller
- Want to demonstrate design patterns

---

### 10. **utils/** (Optional - Helpers)
**Why**: Common utilities, validators, constants, helpers

```python
# utils/validators.py
import re

def validate_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    return len(phone) == 10 and phone.isdigit()

# utils/constants.py
MAX_BOOKINGS_PER_USER = 5
DEFAULT_TIMEOUT_SECONDS = 300
SUPPORTED_PAYMENT_METHODS = ["CARD", "UPI", "CASH"]

# utils/id_generator.py
import uuid

def generate_id(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:8]}"

# utils/date_utils.py
from datetime import datetime, timedelta

def is_past_time(timestamp: datetime) -> bool:
    return timestamp < datetime.now()

def add_hours(timestamp: datetime, hours: int) -> datetime:
    return timestamp + timedelta(hours=hours)
```

**Tips**:
- Add only when functions are reused across multiple files
- Don't over-engineer this
- Good for: validators, ID generators, date helpers, formatters

---

## When to Use What

| Interview Type | Folders to Include | Priority |
|---------------|-------------------|----------|
| **Simple Machine Coding** | `main.py` + `models/` + inline logic | Just get it working |
| **Standard LLD (30-45 min)** | `main.py` + `models/` + `enums/` + `services/` + `exceptions/` | **Most common** |
| **API-Based LLD** | Add `controllers/` + `repositories/` | Show layering |
| **Complex LLD (60+ min)** | Full structure + `strategies/` or `factories/` | Show design patterns |

### Folder Priority for Time-Constrained Interviews

**Must Have (First 20 minutes)**:
1. `main.py` - Entry point with demo
2. `models/` - Your data structures
3. `services/` - Core business logic

**Should Have (Next 15 minutes)**:
4. `enums/` - Replace magic strings
5. `exceptions/` - Better error handling

**Nice to Have (If time permits)**:
6. `repositories/` - Separate data access
7. `controllers/` - For API-like systems
8. `utils/` - Common helpers

**Advanced (Only if finished early)**:
9. `strategies/` - Strategy pattern
10. `factories/` - Factory pattern

---

## Fast MVP Strategy

### Step 1: Start with main.py (5 mins)
```python
# Write what you want to achieve
def main():
    # TODO: Create user
    # TODO: Book slot
    # TODO: Cancel booking
    pass
```

### Step 2: Create models (10 mins)
- Identify 3-4 core entities
- Use dataclasses
- Add only required fields

### Step 3: Build one service (15 mins)
- Implement one complete flow end-to-end
- Use dict/list for storage initially
- Make it work, then refactor

### Step 4: Expand & refactor (remaining time)
- Add remaining features
- Extract common logic
- Handle edge cases

---

## Interview Coding Tips

### ⚡ Speed Hacks
1. **Use type hints** - Catches bugs early, shows professionalism
2. **Dataclasses** - Saves 10+ lines per model
3. **In-memory storage first** - `self.users = {}` beats designing a database
4. **Print debugging** - Faster than perfect error handling initially

### 🎯 Must-Haves
- [ ] Code runs without errors
- [ ] Main flow works (happy path)
- [ ] Models with dataclasses
- [ ] Enums instead of magic strings
- [ ] Custom exceptions for errors
- [ ] Clear class/method names

### 💎 Nice-to-Haves (if time permits)
- [ ] Separate repositories layer
- [ ] Controllers for API-like interaction
- [ ] Strategy or Factory patterns
- [ ] Comprehensive exception hierarchy
- [ ] Utils for common operations

### ❌ Avoid
- Complex inheritance hierarchies
- Over-abstraction early
- Premature optimization
- Too many design patterns

---

## Complete Example: Parking Lot System

### Structure
```
parking_lot/
├── main.py
├── models/
│   ├── vehicle.py
│   ├── parking_spot.py
│   ├── ticket.py
│   └── parking_lot.py
├── enums/
│   ├── vehicle_type.py
│   └── spot_status.py
├── exceptions/
│   └── parking_exceptions.py
├── controllers/
│   └── parking_controller.py
├── services/
│   └── parking_service.py
├── repositories/
│   ├── spot_repository.py
│   └── ticket_repository.py
└── strategies/
    └── pricing_strategy.py
```

### Key Files

```python
# enums/vehicle_type.py
from enum import Enum

class VehicleType(Enum):
    CAR = "CAR"
    BIKE = "BIKE"
    TRUCK = "TRUCK"

# exceptions/parking_exceptions.py
class ParkingLotFullException(Exception):
    def __init__(self):
        super().__init__("No available parking spots")

class InvalidTicketException(Exception):
    def __init__(self, ticket_id: str):
        super().__init__(f"Invalid ticket: {ticket_id}")

# main.py
from controllers.parking_controller import ParkingController
from enums.vehicle_type import VehicleType

def main():
    controller = ParkingController(total_spots=100)
    
    # Test case 1: Park a vehicle
    try:
        response = controller.park_vehicle({
            "vehicle_number": "KA-01-1234",
            "vehicle_type": "CAR"
        })
        print(f"✓ Parked: {response}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test case 2: Unpark vehicle
    try:
        unpark_response = controller.unpark_vehicle({
            "ticket_id": response['ticket_id']
        })
        print(f"✓ Unparked: {unpark_response}")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    main()

# controllers/parking_controller.py
from services.parking_service import ParkingService
from models.vehicle import Vehicle
from enums.vehicle_type import VehicleType
from exceptions.parking_exceptions import ParkingLotFullException

class ParkingController:
    def __init__(self, total_spots: int):
        self.service = ParkingService(total_spots)
    
    def park_vehicle(self, request_data: dict) -> dict:
        vehicle_num = request_data.get("vehicle_number")
        vehicle_type_str = request_data.get("vehicle_type")
        
        if not vehicle_num or not vehicle_type_str:
            return {"error": "Missing required fields"}
        
        try:
            vehicle_type = VehicleType[vehicle_type_str]
            vehicle = Vehicle(vehicle_num, vehicle_type)
            ticket = self.service.park_vehicle(vehicle)
            
            return {
                "success": True,
                "ticket_id": ticket.id,
                "spot_id": ticket.spot_id,
                "entry_time": ticket.entry_time.isoformat()
            }
        except ParkingLotFullException as e:
            return {"error": str(e)}
    
    def unpark_vehicle(self, request_data: dict) -> dict:
        ticket_id = request_data.get("ticket_id")
        
        try:
            fee = self.service.unpark_vehicle(ticket_id)
            return {"success": True, "fee": fee}
        except Exception as e:
            return {"error": str(e)}

# repositories/spot_repository.py
from typing import Optional, List
from models.parking_spot import ParkingSpot
from enums.vehicle_type import VehicleType

class SpotRepository:
    def __init__(self):
        self.spots = {}
    
    def save(self, spot: ParkingSpot):
        self.spots[spot.id] = spot
    
    def find_available_spot(self, vehicle_type: VehicleType) -> Optional[ParkingSpot]:
        for spot in self.spots.values():
            if spot.is_available and spot.vehicle_type == vehicle_type:
                return spot
        return None
```

**Time to build**: 15 mins for basic structure, 30-45 mins for complete implementation

---

## Key Takeaway

**Start simple, make it work, then improve.** Interviewers value working code over perfect architecture. Build the MVP in the first 20 minutes, then polish.