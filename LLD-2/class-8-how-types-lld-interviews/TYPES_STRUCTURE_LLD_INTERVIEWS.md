# Low-Level Design (LLD) Interview Preparation Guide

## Understanding the LLD Interview Landscape in India

### Three Distinct Interview Styles

```
Indian Tech Industry LLD Interviews
│
├── Traditional IT Companies (TCS, Infosys, Wipro, Accenture)
│   ├── Focus: OOP theory, design patterns theory
│   ├── Format: Verbal Q&A, theoretical explanations
│   └── Duration: 30-45 mins
│
├── Product MNCs (Google, Microsoft, Amazon, Flipkart, PhonePe)
│   ├── Focus: Complete design process + code structure
│   ├── Format: Whiteboard/doc design + pseudo/working code
│   └── Duration: 45-60 mins
│
└── Modern Startups (Swiggy, Zomato, CRED, Razorpay, Zepto)
    ├── Focus: Working machine coding + practical design
    ├── Format: Full implementation with tests
    └── Duration: 90-120 mins
```

---

## Type 1: Traditional IT Companies - Theory-Heavy Interviews

**Companies:** TCS, Infosys, Wipro, Cognizant, Accenture, Capgemini, HCL

**What They Ask:**

```
Typical Question Flow:
├── "Explain SOLID principles with examples"
├── "What's the difference between abstract class and interface?"
├── "When would you use Factory vs Builder pattern?"
├── "Explain polymorphism in Python"
├── "What are access modifiers? Why use private attributes?"
└── "Explain singleton pattern. Is it thread-safe?"
```

**Example Questions:**

1. **OOP Trivia:**
   - "Can you override a private method in Python?"
   - "What's the difference between `@staticmethod` and `@classmethod`?"
   - "Explain duck typing vs strong typing"

2. **Design Pattern Theory:**
   - "Explain Observer pattern with real-world example"
   - "When to use Strategy vs State pattern?"
   - "What problem does Facade pattern solve?"

3. **Python-Specific:**
   - "What are magic methods (`__init__`, `__str__`)?"
   - "Explain decorators and their use cases"
   - "What are `*args` and `**kwargs`?"
   - "Difference between list and tuple?"

**How to Prepare:**
```
✅ Memorize all 23 GoF patterns (at least know names)
✅ Practice explaining SOLID with 2-3 examples each
✅ Know Python internals (GIL, memory management, decorators)
✅ Practice UML diagrams on paper
✅ Prepare real-world examples for each pattern
```

**Interview Structure:**
- No coding usually, just verbal/written explanations
- May ask to draw class diagrams on paper
- Expect tricky corner case questions about language features

---

## Type 2: Product MNCs - Design-Focused Interviews

**Companies:** Google, Microsoft, Amazon, Flipkart, PhonePe, Uber, Ola, Paytm

**What They Expect:**

### The Complete Design Process (45-60 mins)

```
Interview Timeline:
00-05 min: Problem statement + Overview alignment
05-12 min: Requirements gathering (5-6 max)
12-20 min: Core entities + Class diagram
20-35 min: API design + Pseudocode/Code structure
35-45 min: Deep dive (schema/concurrency/extensibility)
45-60 min: Q&A, trade-offs discussion
```

### Phase 1: Overview Alignment (Critical!)

**Interviewer Says:** "Design a car rental system like Zoomcar"

**❌ Wrong Response:**
```
"Sure, let me start designing..."
[Starts without checking if they know what Zoomcar is]
```

**✅ Right Response:**
```
YOU: "Let me confirm my understanding - Zoomcar is a self-drive 
     car rental platform where users can book cars by the hour/day. 
     Is this the system we're designing?"

INTERVIEWER: "Yes, exactly."

YOU: "Got it. Should I design from the consumer's perspective 
     (booking cars) or admin perspective (managing inventory), 
     or both?"

INTERVIEWER: "Start with consumer, we can touch admin later."
```

**Key Point:** If you don't know the system (e.g., Swiggy, BookMyShow, Splitwise), **ask the interviewer to explain it**. Don't guess!

```
Example - Unknown System:

YOU: "I'm not familiar with Dunzo. Could you briefly explain 
     what it does?"

INTERVIEWER: "It's a hyperlocal delivery service. Users can 
             send packages or order groceries within the city."

YOU: "Understood. Like a courier + grocery delivery hybrid. 
     Should I focus on the delivery flow or order management?"
```

### Phase 2: Requirements Gathering (5-6 Requirements ONLY!)

**🎯 Golden Rule: Small number of requirements + Working code >>> Many requirements + Nothing works**

**Template:**

```
Functional Requirements (4-5 max):
1. [Core Feature 1]
2. [Core Feature 2]  
3. [Core Feature 3]
4. [Edge case handling]
5. [One complex feature]

Non-Functional (1-2 max):
1. [Concurrency/Thread-safety if needed]
2. [Extensibility point]

Future Scope (mention but don't implement):
- [Feature that makes design extensible]
- [Nice-to-have enhancement]
```

**Example - Parking Lot:**

```
YOU: "Let me gather requirements. I'll keep it focused so we 
     can build something working."

Functional Requirements:
1. Park a vehicle - assign available spot
2. Unpark a vehicle - calculate and collect payment  
3. Check available spots by vehicle type
4. Support multiple vehicle types (bike, car, truck)
5. Multiple floors (if time permits)

Non-Functional:
1. Thread-safe spot allocation (multiple entries)

Future Scope (not implementing now):
- Monthly pass holders
- Valet parking
- Online pre-booking

YOU: "Does this scope sound good? Should I add/remove anything?"
```

**Example - Library Management:**

```
Functional Requirements:
1. Issue book to member
2. Return book 
3. Search books by title/author/ISBN
4. Handle overdue fines
5. Reserve books that are currently issued

Non-Functional:
1. Data persistence needed? 
   [Clarify: In-memory vs DB]

Future Scope:
- Multiple copies of same book
- Digital e-books
- Recommendation system
```

**🚨 Common Mistake:**
```
❌ Student lists 15 requirements
❌ Interview ends with nothing coded
❌ Too complex to implement in time

✅ Student lists 5 requirements  
✅ Working code for all 5
✅ Time to discuss extensibility
```

### Phase 3: Clarifying Questions & Data Persistence

**On Each Requirement, Ask 1-2 Clarifying Questions:**

```
Requirement: "Park a vehicle"

Clarifications:
├── "What if no spots available? Raise exception or return None?"
├── "Should we assign nearest spot or any available spot?"
└── "Do we need to track entry time for billing?"
```

**Persistence Discussion:**

```
YOU: "For this interview, should I persist data to a database 
     or keep everything in-memory?"

[90% of time, they'll say in-memory]

INTERVIEWER: "In-memory is fine."

YOU: "Perfect. I'll use a dict to store spots and tickets. 
     This keeps things simple and fast for the interview."
```

**If they say DB needed:**
```
YOU: "Understood. I'll design the schema after class diagram. 
     For now, I'll assume a repository layer abstracts DB calls."
```

**📝 Critical: Write Requirements Down**

```
On whiteboard/doc, maintain:

┌─────────────────────────────────────┐
│ REQUIREMENTS (Finalized)            │
├─────────────────────────────────────┤
│ ✓ Park vehicle (assign spot)        │
│ ✓ Unpark vehicle (calculate fee)    │
│ ✓ Check availability by type        │
│ ✓ Support Bike/Car/Truck            │
│ ✓ Thread-safe allocation            │
│                                      │
│ Future: Monthly pass, Valet         │
└─────────────────────────────────────┘
```

This shows organization and keeps you on track.

---

### Phase 4: Identifying Entities (The Right Way)

**Two Approaches - Pick Based on Problem:**

#### Approach 1: Noun Identification (Works for most problems)

**When to use:** Clear business domain problems (library, parking, e-commerce)

```
Problem: "Design a movie ticket booking system"

Read requirements, underline nouns:
├── "USER books a SHOW at a THEATER"
├── "SHOW has multiple SEATS"  
├── "Generate BOOKING confirmation"
├── "Process PAYMENT"

Entities identified:
1. User
2. Movie  
3. Show (movie + time + theater)
4. Theater
5. Seat
6. Booking
7. Payment
```

**Example - Food Delivery (Swiggy/Zomato):**

```
Requirement: "Customer orders food from restaurant, 
              delivery partner delivers it"

Nouns → Entities:
├── Customer
├── Restaurant  
├── MenuItem
├── Order
├── Cart
├── DeliveryPartner
└── Payment
```

#### Approach 2: Visualization (Works for game/simulation problems)

**When to use:** Games, simulations, real-time systems

```
Problem: "Design Snake and Ladder game"

Visualize the game:
├── I see a BOARD with numbers
├── PLAYERS move with DICE roll
├── SNAKE connects two positions  
├── LADDER connects two positions
├── GAME manages turns

Entities identified:
1. Board
2. Player
3. Dice
4. Snake
5. Ladder  
6. Game (orchestrator)
```

**Example - Chess:**

```
Visualize gameplay:
├── 8x8 BOARD
├── Different PIECES (King, Queen, etc.)
├── Each piece has POSITION
├── Two PLAYERS take turns
├── MOVE represents action
├── GAME tracks state

Entities:
1. Board
2. Piece (abstract)
   ├── King, Queen, Rook (concrete)
3. Position
4. Player
5. Move
6. Game
```

**Example - Parking Lot (Hybrid approach):**

```
Nouns from requirements:
├── Vehicle, Spot, Floor, Ticket

Visualization:
├── "I see a multi-level structure"
├── "Cars enter, get spot, exit"
├── "Payment happens at exit"

Combined Entities:
1. Vehicle (noun)
2. ParkingSpot (noun + visualized)
3. Floor (visualized structure)
4. Ticket (noun)
5. ParkingLot (orchestrator)
6. Payment (noun)
```

---

### Phase 5: Class Diagram (On Whiteboard/Doc)

**Draw relationships immediately after identifying entities:**

```
Library System Example:

┌──────────────┐         ┌──────────────┐
│    Member    │         │     Book     │
├──────────────┤         ├──────────────┤
│ - id         │         │ - isbn       │
│ - name       │         │ - title      │
│ - email      │         │ - author     │
└──────────────┘         │ - is_available│
       │                 └──────────────┘
       │ issues/returns         ▲
       ▼                        │
┌──────────────┐                │
│  BookLoan    │                │
├──────────────┤                │
│ - loan_id    │◆──────────────┘
│ - issue_date │         
│ - return_date│         ┌──────────────┐
│ - fine       │         │   Library    │
└──────────────┘         ├──────────────┤
                         │ - books      │
                         │ - members    │
                         │ - loans      │
                         └──────────────┘
```

**Relationships to show:**
- **◆ Composition:** Strong ownership (BookLoan ◆→ Book)
- **◇ Aggregation:** Weak ownership (Library ◇→ Books)  
- **→ Association:** Simple link (Member → BookLoan)
- **Multiplicity:** 1..*, 0..1, etc.

---

### Phase 6: Code Structure & Hygiene

**What MNCs Evaluate:**

```
Code Quality Checklist:
├── ✅ Meaningful names (not x, temp, data)
├── ✅ SOLID principles applied
├── ✅ Design patterns explicitly mentioned
├── ✅ Proper encapsulation (private attributes with _)
├── ✅ Exception handling
├── ✅ None checks where needed
├── ✅ Docstrings for complex logic
└── ✅ Extensible design (ABC, Protocol, not concrete everywhere)
```

**Example - Good vs Bad Code:**

```python
# ❌ BAD CODE
class PL:
    def __init__(self):
        self.m = {}
    
    def park(self, v):
        s = None
        for ps in self.m.values():
            if ps.st == 0:
                s = ps
                break
        return T(s, v)

# ✅ GOOD CODE  
from abc import ABC, abstractmethod
from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum

class VehicleType(Enum):
    BIKE = "BIKE"
    CAR = "CAR"
    TRUCK = "TRUCK"

class SpotStatus(Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"

@dataclass
class Vehicle:
    license_plate: str
    vehicle_type: VehicleType

class SpotAllocationStrategy(ABC):
    @abstractmethod
    def find_available_spot(self, vehicle: Vehicle, 
                           spots: Dict[int, 'ParkingSpot']) -> Optional['ParkingSpot']:
        pass

class NearestSpotStrategy(SpotAllocationStrategy):
    def find_available_spot(self, vehicle: Vehicle, 
                           spots: Dict[int, 'ParkingSpot']) -> Optional['ParkingSpot']:
        """Finds nearest available spot matching vehicle type"""
        for spot in sorted(spots.values(), key=lambda s: s.distance_from_entrance):
            if spot.can_accommodate(vehicle):
                return spot
        return None

class ParkingSpot:
    def __init__(self, spot_id: int, spot_type: VehicleType, floor: int):
        self._spot_id = spot_id
        self._spot_type = spot_type
        self._floor = floor
        self._status = SpotStatus.AVAILABLE
    
    def can_accommodate(self, vehicle: Vehicle) -> bool:
        """Check if spot can fit the vehicle"""
        return (self._spot_type == vehicle.vehicle_type and 
                self._status == SpotStatus.AVAILABLE)
    
    def occupy(self) -> None:
        self._status = SpotStatus.OCCUPIED
    
    def vacate(self) -> None:
        self._status = SpotStatus.AVAILABLE

class NoSpotAvailableException(Exception):
    """Raised when no parking spot is available"""
    pass

class ParkingLot:
    def __init__(self, allocation_strategy: SpotAllocationStrategy):
        self._spots: Dict[int, ParkingSpot] = {}
        self._active_tickets: Dict[str, Ticket] = {}
        self._allocation_strategy = allocation_strategy
    
    def park_vehicle(self, vehicle: Vehicle) -> 'Ticket':
        """
        Parks vehicle using configured allocation strategy
        
        Args:
            vehicle: Vehicle to park
            
        Returns:
            Ticket with parking details
            
        Raises:
            NoSpotAvailableException: If parking is full
        """
        spot = self._allocation_strategy.find_available_spot(vehicle, self._spots)
        
        if spot is None:
            raise NoSpotAvailableException(
                f"No spots available for {vehicle.vehicle_type.value}"
            )
        
        spot.occupy()
        ticket = self._generate_ticket(vehicle, spot)
        self._active_tickets[ticket.ticket_id] = ticket
        return ticket
    
    def set_allocation_strategy(self, strategy: SpotAllocationStrategy) -> None:
        """Change spot allocation strategy at runtime (Strategy pattern)"""
        self._allocation_strategy = strategy
```

**Extensibility Example:**

```python
# Instead of hardcoded logic
class ParkingLot:
    def calculate_fee(self, ticket: Ticket) -> float:
        hours = ticket.get_duration_hours()
        return hours * 10.0  # ❌ Hardcoded

# Show extensibility via Strategy
from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, duration_hours: int, vehicle_type: VehicleType) -> float:
        pass

class HourlyPricing(PricingStrategy):
    def __init__(self):
        self._rates = {
            VehicleType.BIKE: 5.0,
            VehicleType.CAR: 10.0,
            VehicleType.TRUCK: 20.0
        }
    
    def calculate_fee(self, duration_hours: int, vehicle_type: VehicleType) -> float:
        return duration_hours * self._rates[vehicle_type]

class FlatRatePricing(PricingStrategy):
    def calculate_fee(self, duration_hours: int, vehicle_type: VehicleType) -> float:
        return 100.0  # Flat rate regardless

class WeekendPricing(PricingStrategy):
    def calculate_fee(self, duration_hours: int, vehicle_type: VehicleType) -> float:
        # 20% discount on weekends
        base_rate = 10.0 if vehicle_type == VehicleType.CAR else 5.0
        return duration_hours * base_rate * 0.8

class ParkingLot:
    def __init__(self, pricing_strategy: PricingStrategy):
        self._pricing_strategy = pricing_strategy
    
    # ✅ Extensible - can swap pricing at runtime
    def calculate_fee(self, ticket: Ticket) -> float:
        return self._pricing_strategy.calculate_fee(
            ticket.get_duration_hours(),
            ticket.vehicle.vehicle_type
        )
    
    def set_pricing_strategy(self, strategy: PricingStrategy) -> None:
        """Change pricing strategy (e.g., weekend vs weekday)"""
        self._pricing_strategy = strategy
```

**Naming Conventions:**

```python
# ✅ DO
class BookLoan:
    pass

def issue_book(member: Member, book: Book) -> BookLoan:
    pass

def find_available_books() -> List[Book]:
    pass

def is_overdue(self) -> bool:
    pass

# ❌ DON'T  
class BL:
    pass

def process(o1, o2):
    pass

def get() -> List[Book]:
    pass

def check() -> bool:
    pass
```

**Python-Specific Best Practices:**

```python
# ✅ Use dataclasses for simple data holders
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Ticket:
    ticket_id: str
    vehicle: Vehicle
    spot: ParkingSpot
    entry_time: datetime
    exit_time: Optional[datetime] = None

# ✅ Use Enums for fixed choices
from enum import Enum

class OrderStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

# ✅ Use type hints
from typing import List, Dict, Optional

def get_available_spots(self, vehicle_type: VehicleType) -> List[ParkingSpot]:
    return [spot for spot in self._spots.values() 
            if spot.spot_type == vehicle_type and spot.is_available()]

# ✅ Use properties for encapsulation
class ParkingSpot:
    def __init__(self, spot_id: int):
        self._spot_id = spot_id
        self._is_occupied = False
    
    @property
    def is_available(self) -> bool:
        return not self._is_occupied
    
    @property
    def spot_id(self) -> int:
        return self._spot_id

# ✅ Use context managers for resource management
class DatabaseConnection:
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# Usage
with DatabaseConnection() as db:
    db.execute_query()
```

---

### Phase 7: Schema Design (If Persistence Required)

**When to show:** Interviewer explicitly asks "How would you persist this?"

```sql
-- Show normalized design with proper indexes

-- Parking Lot Example
CREATE TABLE vehicles (
    id BIGSERIAL PRIMARY KEY,
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    vehicle_type VARCHAR(10) NOT NULL CHECK (vehicle_type IN ('BIKE', 'CAR', 'TRUCK')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_vehicles_license ON vehicles(license_plate);

CREATE TABLE parking_spots (
    id INTEGER PRIMARY KEY,
    floor_number INTEGER NOT NULL,
    spot_number INTEGER NOT NULL,
    spot_type VARCHAR(10) NOT NULL CHECK (spot_type IN ('BIKE', 'CAR', 'TRUCK')),
    is_occupied BOOLEAN DEFAULT FALSE,
    UNIQUE (floor_number, spot_number)
);

-- Composite index for fast lookup by type and availability
CREATE INDEX idx_spots_type_occupied ON parking_spots(spot_type, is_occupied);

CREATE TABLE tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehicle_id BIGINT NOT NULL REFERENCES vehicles(id),
    spot_id INTEGER NOT NULL REFERENCES parking_spots(id),
    entry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    exit_time TIMESTAMP NULL,
    fee_paid DECIMAL(10, 2),
    CONSTRAINT fk_vehicle FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
    CONSTRAINT fk_spot FOREIGN KEY (spot_id) REFERENCES parking_spots(id)
);

CREATE INDEX idx_tickets_entry ON tickets(entry_time);
CREATE INDEX idx_tickets_active ON tickets(exit_time) WHERE exit_time IS NULL;
```

**Explain your indexes:**
```
YOU: "I've added a composite index on (spot_type, is_occupied) 
     because we frequently query 'available spots of type X', 
     and this allows the DB to use index-only scans.
     
     The partial index on exit_time for NULL values helps us 
     quickly find all active tickets without scanning the entire table."
```
---

## Type 3: Modern Startups - Machine Coding Focus

**Companies:** Swiggy, Zomato, CRED, Razorpay, Zepto, Meesho, ShareChat, Dream11

**What They Want:**

```
Machine Coding Evaluation:
├── Working code (can execute)
├── All requirements implemented
├── Test cases passing
├── Clean code structure
├── Follows best practices
└── Bonus: Unit tests, design patterns
```

### Interview Structure (90-120 mins)

```
Timeline:
00-10 min: Requirements (they give, you clarify)
10-20 min: Quick design discussion (optional)
20-95 min: CODING (non-stop)
95-120 min: Demo + code review
```

### What Startups Focus On:

**1. Speed + Working Code:**
```
✅ Submit 70% working solution in time
   > 100% perfect solution late

✅ Core features working perfectly
   > All features half-broken

✅ Simple, readable code
   > Over-engineered complex code
```

**2. Practical Problems:**

```
Common Machine Coding Problems:
├── Splitwise (expense sharing)
├── Snake and Ladder game
├── Parking Lot with CLI
├── Movie ticket booking
├── Online shopping cart
├── Ride-sharing (basic matching)
├── Food delivery assignment
└── Cricket scoring system
```

**3. Execution Environment:**

```
Typical Setup:
├── IDE: PyCharm/VSCode/Online editor
├── Language: Python 3.8+ (usually)
├── Can run with `python main.py`
├── May need to show test cases passing
└── Sometimes given test harness
```

**4. What Makes You Stand Out:**

```python
# ✅ GOOD - Startup-friendly code

# 1. Start with working main method
from typing import Dict, List
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

# Clear, runnable entry point
def main():
    """Demo of parking lot functionality"""
    # Initialize parking lot
    lot = ParkingLot(capacity=100)
    
    # Park a car
    car = Vehicle("KA-01-1234", VehicleType.CAR)
    ticket = lot.park_vehicle(car)
    print(f"✓ Parked at spot: {ticket.spot_id}")
    
    # Unpark and pay
    fee = lot.unpark_vehicle(ticket)
    print(f"✓ Fee collected: ₹{fee}")
    
    # Check availability
    available = lot.get_available_count(VehicleType.CAR)
    print(f"✓ Available car spots: {available}")

if __name__ == "__main__":
    main()

# 2. Modular code with clear separation
class ParkingLot:
    """Main orchestrator for parking lot operations"""
    
    def __init__(self, capacity: int):
        self._spot_manager = SpotManager(capacity)
        self._ticket_manager = TicketManager()
        self._fee_calculator = FeeCalculator()
    
    def park_vehicle(self, vehicle: Vehicle) -> Ticket:
        """Park vehicle and return ticket"""
        spot = self._spot_manager.allocate_spot(vehicle)
        if not spot:
            raise NoSpotAvailableException(f"No spot for {vehicle.vehicle_type}")
        
        ticket = self._ticket_manager.generate_ticket(vehicle, spot)
        return ticket
    
    def unpark_vehicle(self, ticket: Ticket) -> float:
        """Unpark vehicle and return fee"""
        fee = self._fee_calculator.calculate(ticket)
        self._spot_manager.free_spot(ticket.spot_id)
        self._ticket_manager.close_ticket(ticket.ticket_id)
        return fee

# 3. Add basic tests if time permits
import unittest

class TestParkingLot(unittest.TestCase):
    def setUp(self):
        self.lot = ParkingLot(capacity=10)
    
    def test_park_and_unpark(self):
        """Test basic parking and unparking"""
        vehicle = Vehicle("TEST123", VehicleType.CAR)
        
        # Park vehicle
        ticket = self.lot.park_vehicle(vehicle)
        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.vehicle.license_plate, "TEST123")
        
        # Unpark vehicle
        fee = self.lot.unpark_vehicle(ticket)
        self.assertGreater(fee, 0)
    
    def test_no_spot_available(self):
        """Test exception when parking is full"""
        # Fill all spots
        tickets = []
        for i in range(10):
            vehicle = Vehicle(f"KA{i}", VehicleType.CAR)
            tickets.append(self.lot.park_vehicle(vehicle))
        
        # Try to park one more
        with self.assertRaises(NoSpotAvailableException):
            extra_vehicle = Vehicle("EXTRA", VehicleType.CAR)
            self.lot.park_vehicle(extra_vehicle)

if __name__ == "__main__":
    unittest.main()
```

**5. Common Pitfalls:**

```
❌ Spending 30 mins on perfect class diagram
   ✅ Spend 5 mins, start coding

❌ Implementing every design pattern
   ✅ Use 1-2 patterns where natural

❌ Over-abstracting with ABC everywhere  
   ✅ Concrete classes first, refactor if time

❌ No working main() method
   ✅ Runnable demo code

❌ No error handling
   ✅ Basic try-except, validation

❌ Not using Python idioms
   ✅ List comprehensions, generators, dataclasses
```

**Python-Specific Machine Coding Tips:**

```python
# ✅ Use Python's built-in data structures effectively
from collections import defaultdict, deque, Counter
from heapq import heappush, heappop

# For frequency counting
spot_usage = Counter()
spot_usage[spot_id] += 1

# For grouping
spots_by_floor = defaultdict(list)
spots_by_floor[floor].append(spot)

# For queue (FIFO)
waiting_queue = deque()
waiting_queue.append(vehicle)
next_vehicle = waiting_queue.popleft()

# For priority queue (min-heap)
available_spots = []
heappush(available_spots, (distance, spot))
nearest_spot = heappop(available_spots)[1]

# ✅ Use list/dict comprehensions for clean code
# Get all available car spots
available = [spot for spot in spots.values() 
             if spot.type == VehicleType.CAR and spot.is_available]

# Build spot map
spot_map = {spot.id: spot for spot in all_spots}

# ✅ Use generators for memory efficiency
def get_tickets_on_date(self, date):
    """Generator for tickets on specific date"""
    for ticket in self._tickets.values():
        if ticket.entry_time.date() == date:
            yield ticket

# ✅ Use decorators for common functionality
from functools import wraps
import threading

def thread_safe(func):
    """Decorator to make method thread-safe"""
    lock = threading.Lock()
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        with lock:
            return func(*args, **kwargs)
    return wrapper

class ParkingLot:
    @thread_safe
    def park_vehicle(self, vehicle):
        # Thread-safe implementation
        pass

# ✅ Use context managers
class Transaction:
    def __enter__(self):
        self.begin()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

# Usage
with Transaction() as txn:
    txn.park_vehicle(vehicle)
```

---

## Quick Comparison Table

```
┌──────────────────┬────────────────┬─────────────────┬──────────────────┐
│   Aspect         │  Traditional   │   MNC Product   │  Modern Startup  │
├──────────────────┼────────────────┼─────────────────┼──────────────────┤
│ Focus            │ Theory         │ Design Process  │ Working Code     │
│ Coding Required  │ Minimal/None   │ Pseudo/Partial  │ Full working     │
│ Time for Design  │ N/A            │ 50% of time     │ 20% of time      │
│ Time for Code    │ N/A            │ 30% of time     │ 70% of time      │
│ Design Patterns  │ Must explain   │ Use 2-3         │ Use if natural   │
│ Schema Design    │ Sometimes      │ If asked        │ Rarely           │
│ Unit Tests       │ No             │ Discuss approach│ Write if time    │
│ Extensibility    │ Theory only    │ Must show       │ Nice to have     │
│ Thread Safety    │ Explain        │ Show in code    │ If required      │
│ Python Idioms    │ Not critical   │ Good to show    │ Expected         │
└──────────────────┴────────────────┴─────────────────┴──────────────────┘
```

---

## Patterns to Show Off (Python Edition)

| Pattern | Python Implementation | When to Use | Example |
|---------|----------------------|-------------|---------|
| **Strategy** | ABC + implementations | Multiple algorithms | Pricing, Spot allocation |
| **Factory** | Factory method/class | Object creation logic | `VehicleFactory.create(type)` |
| **Singleton** | Module-level or metaclass | Single instance needed | `DatabaseConnection` |
| **Observer** | Callbacks or events | Event notification | Notify when spots available |
| **Builder** | Fluent interface | Complex object construction | `VehicleBuilder().set_type().build()` |
| **Decorator** | Python decorators | Add behavior dynamically | `@thread_safe`, `@cache` |

**Python-Specific Pattern Examples:**

```python
# Singleton using module (Pythonic way)
# parking_lot.py
class _ParkingLot:
    def __init__(self):
        self._spots = {}

parking_lot = _ParkingLot()  # Single instance

# Import anywhere: from parking_lot import parking_lot

# Singleton using metaclass (if they want to see advanced)
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=SingletonMeta):
    pass

# Factory pattern
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def get_parking_fee_multiplier(self) -> float:
        pass

class Bike(Vehicle):
    def get_parking_fee_multiplier(self) -> float:
        return 0.5

class Car(Vehicle):
    def get_parking_fee_multiplier(self) -> float:
        return 1.0

class VehicleFactory:
    @staticmethod
    def create_vehicle(vehicle_type: str, license_plate: str) -> Vehicle:
        vehicles = {
            "BIKE": Bike,
            "CAR": Car,
            "TRUCK": Truck
        }
        
        vehicle_class = vehicles.get(vehicle_type.upper())
        if not vehicle_class:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        
        return vehicle_class(license_plate)

# Observer pattern
from typing import List, Protocol

class ParkingObserver(Protocol):
    def on_vehicle_parked(self, ticket: Ticket) -> None: ...
    def on_vehicle_unparked(self, ticket: Ticket, fee: float) -> None: ...

class NotificationService:
    def on_vehicle_parked(self, ticket: Ticket) -> None:
        print(f"SMS: Vehicle {ticket.vehicle.license_plate} parked")
    
    def on_vehicle_unparked(self, ticket: Ticket, fee: float) -> None:
        print(f"SMS: Fee ₹{fee} collected")

class ParkingLot:
    def __init__(self):
        self._observers: List[ParkingObserver] = []
    
    def register_observer(self, observer: ParkingObserver) -> None:
        self._observers.append(observer)
    
    def park_vehicle(self, vehicle: Vehicle) -> Ticket:
        # ... parking logic
        ticket = self._generate_ticket(vehicle, spot)
        
        # Notify observers
        for observer in self._observers:
            observer.on_vehicle_parked(ticket)
        
        return ticket

# Decorator pattern (Python style)
from functools import wraps
import time

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f}s")
        return result
    return wrapper

def validate_vehicle(func):
    @wraps(func)
    def wrapper(self, vehicle, *args, **kwargs):
        if not vehicle or not vehicle.license_plate:
            raise ValueError("Invalid vehicle")
        return func(self, vehicle, *args, **kwargs)
    return wrapper

class ParkingLot:
    @log_execution_time
    @validate_vehicle
    def park_vehicle(self, vehicle: Vehicle) -> Ticket:
        # Implementation
        pass
```

---

## DSA Application Points in LLD

```python
# 1. Min Heap for spot allocation (nearest to entrance)
import heapq

class SpotManager:
    def __init__(self):
        self._available_spots = []  # Min heap of (distance, spot)
    
    def add_spot(self, spot: ParkingSpot):
        heapq.heappush(self._available_spots, 
                      (spot.distance_from_entrance, spot))
    
    def get_nearest_spot(self) -> ParkingSpot:
        if self._available_spots:
            _, spot = heapq.heappop(self._available_spots)
            return spot
        return None

# 2. Dict for O(1) lookups
class TicketManager:
    def __init__(self):
        self._active_tickets: Dict[str, Ticket] = {}
    
    def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        return self._active_tickets.get(ticket_id)  # O(1)

# 3. Deque for FIFO queue
from collections import deque

class WaitingList:
    def __init__(self):
        self._queue = deque()
    
    def add_to_waitlist(self, vehicle: Vehicle):
        self._queue.append(vehicle)
    
    def get_next(self) -> Optional[Vehicle]:
        return self._queue.popleft() if self._queue else None

# 4. Trie for prefix search (vehicle number search)
class TrieNode:
    def __init__(self):
        self.children = {}
        self.vehicles = []

class VehicleSearchIndex:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, license_plate: str, vehicle: Vehicle):
        node = self.root
        for char in license_plate:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.vehicles.append(vehicle)
    
    def search_by_prefix(self, prefix: str) -> List[Vehicle]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return node.vehicles

# 5. Sliding window for rate limiting
from collections import deque
from time import time

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        self._max_requests = max_requests
        self._window = time_window
        self._requests = deque()  # (timestamp, request)
    
    def is_allowed(self, user_id: str) -> bool:
        now = time()
        
        # Remove old requests outside window
        while self._requests and self._requests[0] < now - self._window:
            self._requests.popleft()
        
        # Check if under limit
        if len(self._requests) < self._max_requests:
            self._requests.append(now)
            return True
        return False

# 6. Graph for dependencies (e.g., Splitwise)
class ExpenseGraph:
    def __init__(self):
        self._graph: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    
    def add_debt(self, from_user: str, to_user: str, amount: float):
        """Add edge: from_user owes to_user"""
        self._graph[from_user][to_user] += amount
    
    def simplify_debts(self) -> List[Tuple[str, str, float]]:
        """Minimize number of transactions using graph algorithm"""
        # Calculate net balance for each user
        balances = defaultdict(float)
        for user, debts in self._graph.items():
            for creditor, amount in debts.items():
                balances[user] -= amount
                balances[creditor] += amount
        
        # Separate debtors and creditors
        debtors = [(user, -bal) for user, bal in balances.items() if bal < 0]
        creditors = [(user, bal) for user, bal in balances.items() if bal > 0]
        
        # Greedy matching
        transactions = []
        i, j = 0, 0
        while i < len(debtors) and j < len(creditors):
            debtor, debt = debtors[i]
            creditor, credit = creditors[j]
            
            amount = min(debt, credit)
            transactions.append((debtor, creditor, amount))
            
            debtors[i] = (debtor, debt - amount)
            creditors[j] = (creditor, credit - amount)
            
            if debtors[i][1] == 0:
                i += 1
            if creditors[j][1] == 0:
                j += 1
        
        return transactions
```

---

## Sample Company-Specific Examples

### Swiggy Interview (Startup Machine Coding)

```
Problem: "Build a food delivery order management system"

Given Requirements:
1. Add restaurants with menu items
2. Customer places order  
3. Assign delivery partner
4. Track order status
5. Calculate bill with taxes

Expected:
├── Working Python code
├── Can run `python main.py` and see output
├── All 5 features working
├── Clean class structure
└── Basic error handling

NOT Expected:
├── Perfect design patterns
├── Database integration
├── Complex algorithms  
└── Over-optimization

Time: 90 minutes to submit working code

Sample Structure:
```

```python
# main.py
from typing import List, Dict
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime

class OrderStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"

@dataclass
class MenuItem:
    id: str
    name: str
    price: float

@dataclass
class Restaurant:
    id: str
    name: str
    menu: List[MenuItem] = field(default_factory=list)
    
    def add_menu_item(self, item: MenuItem):
        self.menu.append(item)

@dataclass
class Order:
    order_id: str
    restaurant: Restaurant
    items: List[MenuItem]
    customer_id: str
    status: OrderStatus = OrderStatus.PENDING
    delivery_partner_id: str = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def calculate_total(self) -> float:
        subtotal = sum(item.price for item in self.items)
        tax = subtotal * 0.05  # 5% GST
        return subtotal + tax

class DeliveryPartner:
    def __init__(self, partner_id: str, name: str):
        self.partner_id = partner_id
        self.name = name
        self.is_available = True

class FoodDeliverySystem:
    def __init__(self):
        self._restaurants: Dict[str, Restaurant] = {}
        self._orders: Dict[str, Order] = {}
        self._partners: Dict[str, DeliveryPartner] = {}
        self._order_counter = 0
    
    def add_restaurant(self, restaurant: Restaurant):
        self._restaurants[restaurant.id] = restaurant
        print(f"✓ Added restaurant: {restaurant.name}")
    
    def place_order(self, customer_id: str, restaurant_id: str, 
                   item_ids: List[str]) -> Order:
        restaurant = self._restaurants.get(restaurant_id)
        if not restaurant:
            raise ValueError("Restaurant not found")
        
        # Get menu items
        items = [item for item in restaurant.menu if item.id in item_ids]
        if len(items) != len(item_ids):
            raise ValueError("Some items not found in menu")
        
        # Create order
        self._order_counter += 1
        order = Order(
            order_id=f"ORD{self._order_counter:04d}",
            restaurant=restaurant,
            items=items,
            customer_id=customer_id
        )
        
        self._orders[order.order_id] = order
        print(f"✓ Order placed: {order.order_id}, Total: ₹{order.calculate_total():.2f}")
        return order
    
    def assign_delivery_partner(self, order_id: str):
        order = self._orders.get(order_id)
        if not order:
            raise ValueError("Order not found")
        
        # Find available partner
        partner = next((p for p in self._partners.values() if p.is_available), None)
        if not partner:
            raise ValueError("No delivery partners available")
        
        order.delivery_partner_id = partner.partner_id
        order.status = OrderStatus.OUT_FOR_DELIVERY
        partner.is_available = False
        print(f"✓ Assigned {partner.name} to order {order_id}")
    
    def update_order_status(self, order_id: str, status: OrderStatus):
        order = self._orders.get(order_id)
        if not order:
            raise ValueError("Order not found")
        
        order.status = status
        print(f"✓ Order {order_id} status: {status.value}")
        
        if status == OrderStatus.DELIVERED and order.delivery_partner_id:
            partner = self._partners[order.delivery_partner_id]
            partner.is_available = True
    
    def add_delivery_partner(self, partner: DeliveryPartner):
        self._partners[partner.partner_id] = partner
        print(f"✓ Added delivery partner: {partner.name}")

def main():
    """Demo the food delivery system"""
    system = FoodDeliverySystem()
    
    # 1. Add restaurant
    restaurant = Restaurant(id="R1", name="Burger King")
    restaurant.add_menu_item(MenuItem("M1", "Whopper", 150.0))
    restaurant.add_menu_item(MenuItem("M2", "Fries", 80.0))
    system.add_restaurant(restaurant)
    
    # 2. Add delivery partner
    partner = DeliveryPartner("P1", "Ravi Kumar")
    system.add_delivery_partner(partner)
    
    # 3. Place order
    order = system.place_order("C1", "R1", ["M1", "M2"])
    
    # 4. Confirm and assign
    system.update_order_status(order.order_id, OrderStatus.CONFIRMED)
    system.assign_delivery_partner(order.order_id)
    
    # 5. Track delivery
    system.update_order_status(order.order_id, OrderStatus.DELIVERED)
    
    print("\n✅ All features working successfully!")

if __name__ == "__main__":
    main()
```

**Output:**
```
✓ Added restaurant: Burger King
✓ Added delivery partner: Ravi Kumar
✓ Order placed: ORD0001, Total: ₹241.50
✓ Order ORD0001 status: CONFIRMED
✓ Assigned Ravi Kumar to order ORD0001
✓ Order ORD0001 status: DELIVERED

✅ All features working successfully!
```

---

## Quick Reference: Common LLD Problems

```
Problem              Key Classes           Patterns             DSA
─────────────────────────────────────────────────────────────────────
Parking Lot          ParkingSpot,          Strategy, Factory    dict (HashMap)
                     Vehicle, Ticket,                           heapq (PriorityQueue)
                     ParkingLot

Chess Game           Board, Piece,         Command, Strategy    2D list
                     Player, Move                               

Library System       Book, Member,         Observer, Facade     dict
                     BookLoan, Library                          defaultdict

Splitwise            User, Expense,        Strategy, Observer   Graph (dict of dicts)
                     Group, Settlement                          heapq (Min Heap)

Cache (LRU)          LRUCache, Node        Singleton            dict +
                                                                OrderedDict/deque

Rate Limiter         RateLimiter,          Strategy             Sliding Window
                     RequestCounter                             deque

Logger               Logger, Handler,      Singleton, Chain     queue.Queue
                     LogLevel              of Responsibility

Snake & Ladder       Board, Player,        Strategy             list, dict
                     Snake, Ladder, Game                        

Food Delivery        Restaurant, Order,    Strategy, Observer   dict, heapq
                     DeliveryPartner                            (for matching)

Movie Booking        Theater, Show,        Builder, Strategy    dict, set
                     Seat, Booking                              (for seat locking)
```

---

## Final Strategic Advice

### For Traditional IT Interviews:
```
Prepare:
├── Memorize GoF patterns with examples
├── SOLID principles with 3 examples each
├── Python specifics (decorators, generators, GIL)
└── Practice explaining on whiteboard

During interview:
├── Give textbook definitions first
├── Then real-world examples
├── Draw UML if asked
└── Be confident even if theoretical
```

### For Product MNCs:
```
Prepare:
├── Practice 10+ design problems end-to-end
├── Focus on requirements gathering
├── Draw clean class diagrams
└── Code structure (pseudo-code acceptable)

During interview:
├── Spend time on requirements (don't rush)
├── Draw before coding
├── Explicitly mention patterns and principles
├── Ask for feedback: "Is this the right direction?"
├── Show extensibility with ABC/Protocol
└── Use type hints throughout
```

### For Startups:
```
Prepare:
├── Practice machine coding with 90-min timer
├── Focus on speed + correctness
├── Keep code simple and readable
└── Practice with PyCharm/VSCode

During interview:
├── Start coding quickly after brief design
├── Make it work first, optimize later
├── Have a running main() method
├── Use Python idioms (comprehensions, dataclasses)
├── Comment your code as you write
├── Test manually with print statements
└── Use @dataclass and Enums for clean code
```

### Python-Specific Interview Wins:

```python
# ✅ Show you know modern Python
from typing import List, Dict, Optional, Protocol
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

# ✅ Use context managers
with open('data.txt') as f:
    data = f.read()

# ✅ Use comprehensions
available = [s for s in spots if s.is_available]

# ✅ Use proper exceptions
class ParkingFullException(Exception):
    """Raised when parking lot is full"""
    pass

# ✅ Use property decorators
@property
def is_available(self) -> bool:
    return self._status == Status.AVAILABLE

# ✅ Use __str__ and __repr__
def __repr__(self) -> str:
    return f"Vehicle(plate={self.plate}, type={self.type})"
```

---

## The Showoff Checklist

**During Requirements:**
- [ ] Ask about scale → shows you think big
- [ ] Clarify concurrency → shows production mindset
- [ ] Question persistence → shows you understand trade-offs

**During Design:**
- [ ] Use proper UML notation → shows formality
- [ ] Name 2-3 design patterns → shows knowledge
- [ ] Mention SOLID principles → shows fundamentals
- [ ] Use type hints everywhere → shows modern Python

**During Coding:**
- [ ] Use meaningful names → readability
- [ ] Add docstrings for complex methods → documentation
- [ ] Handle edge cases → thoroughness
- [ ] Write at least 1 test → quality mindset
- [ ] Use dataclasses/Enums → clean code
- [ ] Use list/dict comprehensions → Pythonic

**During Discussion:**
- [ ] Discuss time/space complexity → shows DSA foundation
- [ ] Mention logging/monitoring → shows production experience
- [ ] Talk about future extensions → shows vision
- [ ] Explain why dict over list → shows data structure knowledge

---

Good luck! Remember: **LLD is about communication, not just code.** Explain your thought process, show trade-offs, and demonstrate you can work with others. 🚀