# LLD Design Decisions Quiz
### Based on Tic Tac Toe & Parking Lot Systems
- HW1 - How do you handle database Migrations?
---

## Question 1: Enum vs Boolean - Parking Spot Status

```python
# Approach A: Using Boolean
@dataclass
class ParkingSpot:
    id: str
    spot_number: int
    is_occupied: bool = False

    def is_available(self):
        return not self.is_occupied

# Approach B: Using Enum
from enum import Enum

class SpotStatus(Enum):
    FREE = "FREE"
    OCCUPIED = "OCCUPIED"

@dataclass
class ParkingSpot:
    id: str
    spot_number: int
    status: SpotStatus = SpotStatus.FREE

    def is_available(self):
        return self.status == SpotStatus.FREE
```

**Interview Question: Which approach should you choose and why?**

- A) Boolean - simpler and faster
- B) Enum - better but only if you need more than 2 states
- C) Enum - always better for domain modeling
- D) Doesn't matter, both are equivalent

---
<details>
<summary>Answer</summary>

**C) Enum - always better for domain modeling**

**Why Enum is Superior:**

1. **Future-Proof:** What if business adds `RESERVED`, `UNDER_MAINTENANCE`, `VIP_ONLY` states later?
   - Boolean: Major refactoring needed
   - Enum: Just add new enum value

2. **Self-Documenting:** `status == SpotStatus.OCCUPIED` is clearer than `is_occupied == True`

3. **Type Safety:** Can't accidentally assign `status = "free"` (lowercase) with enum validation

4. **Explicit Domain:** Boolean hides business logic; Enum makes domain states explicit

**Real Interview Scenario:**
```python
# Later requirement: Add "Reserved for VIP" spots
class SpotStatus(Enum):
    FREE = "FREE"
    OCCUPIED = "OCCUPIED"
    RESERVED = "RESERVED"      # Easy to add!
    MAINTENANCE = "MAINTENANCE"

# With boolean, you'd need:
is_occupied: bool
is_reserved: bool  # Now you have 4 states with 2 booleans - error prone!
is_maintenance: bool
```

**Key Lesson:** Use Enum for domain states, even if currently only 2 values. Booleans are for true binary flags like `is_deleted`, `is_active`.

</details>

---

## Question 2: ID Generation Strategy

```python
# Approach A: Auto-increment
class TicketRepository:
    def __init__(self):
        self._counter = 1
        self._storage = {}

    def generate_ticket_id(self):
        ticket_id = f"TKT-{self._counter}"
        self._counter += 1
        return ticket_id

# Approach B: UUID
import uuid

class TicketRepository:
    def __init__(self):
        self._storage = {}

    def generate_ticket_id(self):
        return f"TKT-{uuid.uuid4()}"

# Approach C: Timestamp-based
from datetime import datetime

class TicketRepository:
    def __init__(self):
        self._storage = {}

    def generate_ticket_id(self):
        return f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
```

**Interview Question: For a parking lot system, which approach is best?**

- A) Auto-increment - sequential and readable
- B) UUID - globally unique and no collision
- C) Timestamp - sortable and readable
- D) Depends on requirements

---
<details>
<summary>Answer</summary>

**D) Depends on requirements**

**Analysis:**

**Auto-Increment (A):**
- ✅ Human-readable (`TKT-1`, `TKT-2`)
- ✅ Sequential and sortable
- ✅ Easy to debug
- ❌ Not thread-safe without locks
- ❌ Breaks in distributed systems (multiple entry gates)
- ❌ Reveals business volume (competitor knows you issued 10,000 tickets)

**UUID (B):**
- ✅ Globally unique
- ✅ Thread-safe, no coordination needed
- ✅ Works in distributed systems
- ✅ Hides business metrics
- ❌ Not human-readable (`TKT-a1b2c3d4-e5f6...`)
- ❌ Not sortable by creation time
- ❌ Harder to debug

**Timestamp-based (C):**
- ✅ Sortable by time
- ✅ Readable
- ❌ Collision risk if two tickets issued in same second
- ❌ Needs sequence number to handle collisions
- ❌ Vulnerable to clock skew in distributed systems

**Best Solution - Hybrid:**
```python
import uuid
from datetime import datetime

def generate_ticket_id():
    # Readable prefix + timestamp + short UUID
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    short_uuid = str(uuid.uuid4())[:8]
    return f"TKT-{timestamp}-{short_uuid}"
    # Example: TKT-20250108143022-a1b2c3d4
```

**Interview Answer:**
- **LLD Interview (Single System):** Auto-increment is fine, mention thread-safety
- **Senior Interview:** Mention distributed systems, suggest UUID or hybrid
- **Always:** Ask clarifying questions about scale and distributed architecture

</details>

---

## Question 3: Where to Validate?

```python
# Parking Lot - Vehicle Entry Flow
# Controller -> Service -> Repository

# Option A: Validate in Controller
class TicketController:
    def issue_ticket(self, request_data):
        if not request_data.get('license_plate'):
            return {"error": "License plate required"}, 400

        ticket = self.service.issue_ticket(...)

# Option B: Validate in Service
class TicketService:
    def issue_ticket(self, license_plate, vehicle_type):
        if not license_plate:
            raise ValidationException("License plate required")

        # Business logic

# Option C: Validate in Model
@dataclass
class Vehicle:
    license_plate: str
    vehicle_type: VehicleType

    def __post_init__(self):
        if not self.license_plate:
            raise ValueError("License plate required")

# Option D: Validate in all layers
```

**Interview Question: Where should validation happen?**

- A) Only in Controller - it's the entry point
- B) Only in Service - single source of truth
- C) Only in Model - domain-driven design
- D) Different types of validation in different layers

---
<details>
<summary>Answer</summary>

**D) Different types of validation in different layers**

**The Right Approach:**

**1. Controller Layer - Request Format Validation**
```python
class TicketController:
    def issue_ticket(self, request_data):
        # Check required fields exist
        if 'license_plate' not in request_data:
            return {"error": "license_plate field required"}, 400

        # Check data types
        if not isinstance(request_data['license_plate'], str):
            return {"error": "license_plate must be string"}, 400
```
**Validates:** HTTP/API contract, field presence, data types

**2. Service Layer - Business Rule Validation**
```python
class TicketService:
    def issue_ticket(self, license_plate, vehicle_type):
        # Check business rules
        if self.vehicle_repo.has_active_ticket(license_plate):
            raise BusinessException("Vehicle already parked")

        if not self.has_available_spots(vehicle_type):
            raise NoSpotAvailableException()
```
**Validates:** Business logic, cross-entity rules, availability

**3. Model Layer - Domain Invariants**
```python
@dataclass
class Vehicle:
    license_plate: str
    vehicle_type: VehicleType

    def __post_init__(self):
        # Ensure object is always in valid state
        if not self.license_plate or len(self.license_plate) < 5:
            raise ValueError("Invalid license plate")

        if not isinstance(self.vehicle_type, VehicleType):
            raise ValueError("Invalid vehicle type")
```
**Validates:** Data integrity, domain constraints, object invariants

**Why This Matters:**
```python
# Example: Service can create Vehicle without going through Controller
# Model validation ensures no invalid Vehicle can ever exist
vehicle = Vehicle(license_plate="", vehicle_type=VehicleType.CAR)
# Raises ValueError! ✓
```

**Interview Answer:**
- Controller: Format & API contract
- Service: Business rules & cross-cutting concerns
- Model: Domain invariants & object consistency
- **Never skip model validation** - other services might create objects directly!

</details>

---

## Question 4: Repository Method Design

```python
# Finding available parking spots

# Approach A: Generic method
class ParkingSpotRepository:
    def find_all(self):
        return list(self._storage.values())

# Usage in Service:
available = [s for s in repo.find_all() if s.status == SpotStatus.FREE]

# Approach B: Specific method
class ParkingSpotRepository:
    def find_available(self):
        return [s for s in self._storage.values() if s.is_available()]

# Approach C: Query method with filter
class ParkingSpotRepository:
    def find_by_status(self, status: SpotStatus):
        return [s for s in self._storage.values() if s.status == status]

# Usage:
available = repo.find_by_status(SpotStatus.FREE)

# Approach D: Builder pattern query
class ParkingSpotRepository:
    def query(self):
        return SpotQuery(self._storage)

class SpotQuery:
    def available(self):
        return self.filter(lambda s: s.is_available())

    def by_type(self, spot_type):
        return self.filter(lambda s: s.spot_type == spot_type)

# Usage:
available = repo.query().available().by_type(SpotType.LARGE).execute()
```

**Interview Question: Which approach for an LLD interview?**

- A) Generic - keeps repository simple
- B) Specific - clear and direct
- C) Query method - flexible
- D) Builder pattern - most powerful

---
<details>
<summary>Answer</summary>

**B) Specific methods - clear and direct**

**Why:**

**For LLD Interviews:**
```python
class ParkingSpotRepository:
    # ✅ GOOD - Domain-specific, clear intent
    def find_available(self) -> List[ParkingSpot]:
        return [s for s in self._storage.values() if s.is_available()]

    def find_available_by_type(self, spot_type: SpotType) -> List[ParkingSpot]:
        return [s for s in self._storage.values()
                if s.is_available() and s.spot_type == spot_type]

    def find_by_floor(self, floor_id: str) -> List[ParkingSpot]:
        return [s for s in self._storage.values() if s.floor_id == floor_id]
```

**Why Not Others:**

**Approach A (Generic):**
```python
# ❌ BAD - Business logic leaks into Service
available = [s for s in repo.find_all() if s.status == SpotStatus.FREE]
# Service knows about internal status field - tight coupling!
```

**Approach C (Query with filter):**
```python
# ⚠️ OKAY but verbose
available = repo.find_by_status(SpotStatus.FREE)
large_spots = repo.find_by_type(SpotType.LARGE)
# Need many generic methods, not much better than specific
```

**Approach D (Builder pattern):**
```python
# ❌ OVERKILL for LLD interview
repo.query().available().by_type(SpotType.LARGE).on_floor(1).execute()
# Takes too much time to implement
# Interviewer thinks you're over-engineering
```

**Real Interview Conversation:**
```
Interviewer: "How do you find available spots?"
You: "I'll create a find_available() method in the repository"
Interviewer: "What if we need to filter by type?"
You: "I can add find_available_by_type(spot_type) - keeps the intent clear"
```

**Pro Tip:** Mention you could make it more generic later, but for now specific methods are:
- Clear in intent
- Easy to test
- Quick to implement
- Match domain language

**When to Use Others:**
- Generic (A): Never in interviews
- Query filter (C): If interviewer asks for "flexible querying"
- Builder (D): Only if interviewer specifically wants query builder pattern

</details>

---

## Question 5: Exception Handling Strategy

```python
# Tic Tac Toe - Making a move

# Approach A: Return boolean
class Game:
    def make_move(self, row: int, col: int, player: Player) -> bool:
        if not self._is_valid_move(row, col):
            return False
        # Make move
        return True

# Usage:
if not game.make_move(0, 0, player):
    print("Invalid move")

# Approach B: Raise specific exceptions
class InvalidMoveException(Exception):
    pass

class Game:
    def make_move(self, row: int, col: int, player: Player):
        if not self._is_valid_move(row, col):
            raise InvalidMoveException("Cell already occupied")
        # Make move

# Usage:
try:
    game.make_move(0, 0, player)
except InvalidMoveException as e:
    print(f"Error: {e}")

# Approach C: Return result object
@dataclass
class MoveResult:
    success: bool
    message: str = ""
    game_over: bool = False
    winner: Optional[Player] = None

class Game:
    def make_move(self, row: int, col: int, player: Player) -> MoveResult:
        if not self._is_valid_move(row, col):
            return MoveResult(success=False, message="Invalid move")

        # Make move
        winner = self._check_winner()
        return MoveResult(
            success=True,
            game_over=winner is not None,
            winner=winner
        )
```

**Interview Question: Which approach is best for LLD interviews?**

- A) Boolean - simple and clear
- B) Exceptions - Pythonic and clean
- C) Result object - rich information
- D) Depends on the use case

---
<details>
<summary>Answer</summary>

**D) Depends on the use case - but lean towards B (Exceptions) for invalid operations**

**Decision Matrix:**

**Use Boolean (A) when:**
- ✅ Checking conditions: `is_game_over()`, `has_winner()`, `is_valid_move()`
- ✅ Query methods: `can_place_symbol()`, `is_cell_empty()`
```python
# ✅ GOOD - checking state
if game.is_valid_move(0, 0):
    game.make_move(0, 0, player)
```

**Use Exceptions (B) when:**
- ✅ Enforcing business rules
- ✅ Invalid operations that shouldn't happen
- ✅ Exceptional scenarios
```python
# ✅ GOOD - operation that can fail
class Game:
    def make_move(self, row: int, col: int, player: Player):
        if not self.is_valid_move(row, col):
            raise InvalidMoveException("Cell occupied")

        if not self.is_correct_turn(player):
            raise WrongPlayerTurnException(f"Not {player.name}'s turn")

        # Make move
```

**Use Result Object (C) when:**
- ✅ Method returns multiple pieces of information
- ✅ Success + additional context needed
- ✅ Want to avoid exceptions for control flow
```python
# ✅ GOOD - rich result needed
@dataclass
class MoveResult:
    success: bool
    game_over: bool = False
    winner: Optional[Player] = None
    winning_combination: Optional[List] = None

# Caller gets everything in one call
result = game.make_move(0, 0, player)
if result.game_over:
    print(f"{result.winner.name} wins!")
```

**Best Hybrid Approach:**
```python
class Game:
    # Query methods - return boolean
    def is_valid_move(self, row: int, col: int) -> bool:
        return self.board.is_empty(row, col)

    def is_game_over(self) -> bool:
        return self.winner is not None or self.board.is_full()

    # Command methods - raise exceptions
    def make_move(self, row: int, col: int, player: Player) -> None:
        if not self.is_correct_turn(player):
            raise WrongPlayerTurnException()

        if not self.is_valid_move(row, col):
            raise InvalidMoveException()

        self.board.place_symbol(row, col, player.symbol)
        self._update_game_state()

    # Query with rich result
    def get_game_state(self) -> GameState:
        return GameState(
            is_over=self.is_game_over(),
            winner=self.winner,
            current_player=self.current_player
        )
```

**Interview Answer:**
- **Queries → Boolean:** `is_valid()`, `can_do()`, `has_something()`
- **Commands → Exceptions:** `make_move()`, `place_bet()`, `process_payment()`
- **Rich results → Result Objects:** When you need to return multiple related pieces of info

**Red Flag in Interviews:**
```python
# ❌ BAD - Using boolean for commands loses error context
if not game.make_move(0, 0, player):
    # WHY did it fail? Cell occupied? Wrong turn? Game over?
    print("Move failed")  # Unhelpful!
```

</details>

---

## Question 6: Null Object vs Optional vs Exception

```python
# Parking Lot - Finding a ticket

# Approach A: Return None
class TicketRepository:
    def find_by_id(self, ticket_id: str) -> Optional[Ticket]:
        return self._storage.get(ticket_id)

# Usage:
ticket = repo.find_by_id("TKT-123")
if ticket is None:
    print("Not found")

# Approach B: Raise exception
class TicketRepository:
    def find_by_id(self, ticket_id: str) -> Ticket:
        ticket = self._storage.get(ticket_id)
        if ticket is None:
            raise TicketNotFoundException(ticket_id)
        return ticket

# Usage:
try:
    ticket = repo.find_by_id("TKT-123")
except TicketNotFoundException:
    print("Not found")

# Approach C: Null object pattern
class NullTicket(Ticket):
    def is_null(self):
        return True

class TicketRepository:
    def find_by_id(self, ticket_id: str) -> Ticket:
        ticket = self._storage.get(ticket_id)
        return ticket if ticket else NullTicket()

# Usage:
ticket = repo.find_by_id("TKT-123")
if not ticket.is_null():
    # use ticket
```

**Interview Question: Which approach for repository find methods?**

- A) Return None/Optional - explicit and safe
- B) Raise exception - forces error handling
- C) Null object - no null checks needed
- D) Different approaches for different methods

---
<details>
<summary>Answer</summary>

**D) Different approaches for different methods**

**The Right Strategy:**

**Return Optional (None) when:**
- ✅ "Not found" is a **valid outcome**
- ✅ Caller will check and handle gracefully
- ✅ Find/query operations

```python
class TicketRepository:
    def find_by_id(self, ticket_id: str) -> Optional[Ticket]:
        """Query method - not found is valid"""
        return self._storage.get(ticket_id)

# Service Layer
def get_ticket_if_exists(self, ticket_id: str) -> Optional[Ticket]:
    return self.repo.find_by_id(ticket_id)
```

**Raise Exception when:**
- ✅ "Not found" is an **error condition**
- ✅ Caller expects resource to exist
- ✅ Get operations (assuming existence)

```python
class TicketRepository:
    def get_by_id(self, ticket_id: str) -> Ticket:
        """Get method - must exist"""
        ticket = self._storage.get(ticket_id)
        if ticket is None:
            raise TicketNotFoundException(f"Ticket {ticket_id} not found")
        return ticket

# Service Layer
def process_payment(self, ticket_id: str):
    # Should fail loudly if ticket doesn't exist
    ticket = self.repo.get_by_id(ticket_id)  # Raises exception
    # Process payment
```

**Use Null Object when:**
- ⚠️ Rarely in LLD interviews - only if specifically needed
- ✅ Default behavior is well-defined
- ✅ Want to avoid null checks

**Best Practice - Have Both:**
```python
class TicketRepository:
    def find_by_id(self, ticket_id: str) -> Optional[Ticket]:
        """
        Find ticket by ID.
        Returns None if not found (valid scenario).
        """
        return self._storage.get(ticket_id)

    def get_by_id(self, ticket_id: str) -> Ticket:
        """
        Get ticket by ID.
        Raises TicketNotFoundException if not found (error scenario).
        """
        ticket = self.find_by_id(ticket_id)
        if ticket is None:
            raise TicketNotFoundException(ticket_id)
        return ticket
```

**Usage Examples:**
```python
# Scenario 1: Checking if vehicle is parked
ticket = ticket_repo.find_by_license_plate("KA01AB1234")
if ticket:
    print("Vehicle already parked")
else:
    print("Vehicle not in parking lot")  # Valid outcome

# Scenario 2: Processing payment (ticket MUST exist)
ticket = ticket_repo.get_by_id("TKT-123")  # Raises if not found
payment = payment_service.process(ticket)  # Proceed with confidence
```

**Interview Conversation:**
```
Interviewer: "What if the ticket is not found?"
You: "I have two methods:"
     "- find_by_id() returns Optional for queries"
     "- get_by_id() raises exception for operations that require the ticket"
Interviewer: "Why both?"
You: "Different semantics - find is exploratory, get assumes existence"
```

**Red Flags:**
```python
# ❌ BAD - Inconsistent naming
def find_by_id(self, id: str) -> Ticket:  # Says "find" but raises exception
    ticket = self._storage.get(id)
    if not ticket:
        raise NotFoundException()  # Confusing!

# ❌ BAD - Using exceptions for control flow
try:
    ticket = repo.get_by_id("TKT-123")
except TicketNotFoundException:
    # Expected scenario treated as exception
    create_new_ticket()
```

**Key Takeaway:**
- **find_*** → Optional (not found is valid)
- **get_*** → Raises exception (not found is error)
- **Null Object** → Skip unless specifically needed

</details>

---

## Question 7: Strategy Pattern - Where to Put Logic?

```python
# Parking Lot - Different pricing strategies

# Approach A: Strategy in Service
class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, hours: float) -> float:
        pass

class HourlyPricing(PricingStrategy):
    def calculate(self, hours: float) -> float:
        return hours * 50

class PaymentService:
    def __init__(self, pricing_strategy: PricingStrategy):
        self.pricing_strategy = pricing_strategy

    def calculate_amount(self, ticket):
        hours = self._calculate_hours(ticket)
        return self.pricing_strategy.calculate(hours)

# Approach B: Strategy with full context
class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, ticket: Ticket, entry_time: datetime, exit_time: datetime) -> float:
        pass

class HourlyPricing(PricingStrategy):
    def calculate(self, ticket: Ticket, entry_time: datetime, exit_time: datetime) -> float:
        hours = (exit_time - entry_time).total_seconds() / 3600
        rate = self._get_rate(ticket.vehicle.vehicle_type)
        return hours * rate

    def _get_rate(self, vehicle_type: VehicleType) -> float:
        return {
            VehicleType.BIKE: 20,
            VehicleType.CAR: 50,
            VehicleType.TRUCK: 100
        }[vehicle_type]

# Approach C: Strategy just for rate, service handles time
class PricingStrategy(ABC):
    @abstractmethod
    def get_rate(self, vehicle_type: VehicleType) -> float:
        pass

class PaymentService:
    def __init__(self, pricing_strategy: PricingStrategy):
        self.pricing_strategy = pricing_strategy

    def calculate_amount(self, ticket):
        hours = self._calculate_hours(ticket)
        rate = self.pricing_strategy.get_rate(ticket.vehicle.vehicle_type)
        return hours * rate
```

**Interview Question: Which design is best?**

- A) Strategy gets only what it needs (hours)
- B) Strategy gets full context (ticket, times)
- C) Strategy only decides rates, service handles calculation
- D) Mix of B and C depending on complexity

---
<details>
<summary>Answer</summary>

**B) Strategy gets full context - most flexible**

**Why:**

**Approach B (Full Context) is Best:**
```python
class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, ticket: Ticket, entry_time: datetime, exit_time: datetime) -> float:
        pass

class WeekdayWeekendPricing(PricingStrategy):
    def calculate(self, ticket: Ticket, entry_time: datetime, exit_time: datetime) -> float:
        # Strategy can make its own decisions!
        is_weekend = entry_time.weekday() >= 5
        hours = (exit_time - entry_time).total_seconds() / 3600

        if ticket.vehicle.vehicle_type == VehicleType.CAR:
            rate = 100 if is_weekend else 50
        else:
            rate = 50 if is_weekend else 20

        return hours * rate

class DynamicPricing(PricingStrategy):
    def calculate(self, ticket: Ticket, entry_time: datetime, exit_time: datetime) -> float:
        # Can check spot type, time of day, duration, vehicle type
        base_rate = self._get_base_rate(ticket.vehicle.vehicle_type)

        # Peak hours surcharge
        if 8 <= entry_time.hour <= 10 or 17 <= entry_time.hour <= 19:
            base_rate *= 1.5

        # Large spot premium
        if ticket.parking_spot.spot_type == SpotType.LARGE:
            base_rate *= 1.2

        hours = (exit_time - entry_time).total_seconds() / 3600
        return hours * base_rate
```

**Why Not Others:**

**Approach A (Hours Only) - Too Restrictive:**
```python
# ❌ BAD - Strategy can't make smart decisions
class PricingStrategy(ABC):
    def calculate(self, hours: float) -> float:
        pass

# Can't implement weekend pricing, peak hour pricing, vehicle-based pricing!
# Service must know about ALL pricing rules and pass calculated values
```

**Approach C (Rate Only) - Rigid:**
```python
# ❌ BAD - Service has to know pricing logic
class PaymentService:
    def calculate_amount(self, ticket):
        hours = self._calculate_hours(ticket)

        # Service shouldn't know this!
        if is_weekend():
            rate = self.pricing_strategy.get_weekend_rate(...)
        else:
            rate = self.pricing_strategy.get_weekday_rate(...)

        # What if pricing is not hours * rate?
        # What if first hour free, then charges apply?
        return hours * rate
```

**The Right Way:**
```python
class PricingStrategy(ABC):
    """Strategy has full control over pricing logic"""

    @abstractmethod
    def calculate(
        self,
        ticket: Ticket,
        entry_time: datetime,
        exit_time: datetime
    ) -> Money:  # Return Money object, not float!
        pass


class FirstHourFreePricing(PricingStrategy):
    def calculate(self, ticket: Ticket, entry_time: datetime, exit_time: datetime) -> Money:
        total_hours = (exit_time - entry_time).total_seconds() / 3600

        # First hour free
        billable_hours = max(0, total_hours - 1)

        rate = 50  # ₹50 per hour
        amount = billable_hours * rate

        return Money(Decimal(amount))


class SlabBasedPricing(PricingStrategy):
    def calculate(self, ticket: Ticket, entry_time: datetime, exit_time: datetime) -> Money:
        hours = (exit_time - entry_time).total_seconds() / 3600

        # Complex slab logic - strategy handles it!
        if hours <= 2:
            amount = 50
        elif hours <= 4:
            amount = 50 + (hours - 2) * 40
        else:
            amount = 50 + (2 * 40) + (hours - 4) * 30

        return Money(Decimal(amount))
```

**Service Layer (Clean):**
```python
class PaymentService:
    def __init__(self, pricing_strategy: PricingStrategy):
        self.pricing_strategy = pricing_strategy

    def calculate_amount(self, ticket: Ticket, exit_time: datetime) -> Money:
        # Service doesn't know pricing logic at all!
        return self.pricing_strategy.calculate(
            ticket=ticket,
            entry_time=ticket.entry_time,
            exit_time=exit_time
        )
```

**Interview Answer:**
"I pass full context to the strategy because:"
1. **Strategy has full control** - can implement any pricing logic
2. **Service stays clean** - doesn't need to know pricing rules
3. **Easy to add complex strategies** - weekend, peak hour, slab-based, dynamic
4. **True Strategy Pattern** - behavior fully encapsulated

**Mention this bonus:**
"If performance is a concern and strategies are complex, I might pass a PricingContext object to avoid coupling strategy to domain models."

```python
@dataclass
class PricingContext:
    vehicle_type: VehicleType
    spot_type: SpotType
    entry_time: datetime
    exit_time: datetime
    is_vip: bool = False

# Strategy depends on context, not domain models
class PricingStrategy(ABC):
    def calculate(self, context: PricingContext) -> Money:
        pass
```

</details>

---

## Question 8: Model Relationships - Composition vs Reference

```python
# Parking Lot - Ticket design

# Approach A: Store full objects (Composition)
@dataclass
class ParkingTicket:
    ticket_id: str
    vehicle: Vehicle  # Full object
    parking_spot: ParkingSpot  # Full object
    entry_gate: ParkingGate  # Full object
    entry_time: datetime

# Approach B: Store IDs (Reference)
@dataclass
class ParkingTicket:
    ticket_id: str
    vehicle_id: str
    parking_spot_id: str
    entry_gate_id: str
    entry_time: datetime

# Approach C: Hybrid
@dataclass
class ParkingTicket:
    ticket_id: str
    vehicle: Vehicle  # Full object - core entity
    parking_spot_id: str  # Reference - mutable state
    entry_gate_id: str  # Reference - static data
    entry_time: datetime
```

**Interview Question: Which approach for an LLD interview?**

- A) Store full objects - easy to use
- B) Store IDs - simulates database relations
- C) Hybrid - best of both worlds
- D) Full objects for in-memory, IDs for database

---
<details>
<summary>Answer</summary>

**A) Store full objects - this is in-memory LLD, not database design**

**Why Full Objects:**

```python
@dataclass
class ParkingTicket:
    ticket_id: str
    vehicle: Vehicle  # ✅ Full object
    parking_spot: ParkingSpot  # ✅ Full object
    entry_gate: ParkingGate  # ✅ Full object
    entry_operator: Optional[ParkingAttendant] = None  # ✅ Full object
    entry_time: datetime = field(default_factory=datetime.now)
```

**Benefits:**

1. **No Lazy Loading Complexity:**
```python
# ✅ GOOD - Direct access
def generate_invoice(self, ticket: ParkingTicket):
    print(f"Vehicle: {ticket.vehicle.license_plate}")
    print(f"Spot: {ticket.parking_spot.spot_number}")
    print(f"Operator: {ticket.entry_operator.name}")

# ❌ BAD - If using IDs, need to fetch
def generate_invoice(self, ticket: ParkingTicket):
    vehicle = self.vehicle_repo.get_by_id(ticket.vehicle_id)  # Extra lookup!
    spot = self.spot_repo.get_by_id(ticket.spot_id)  # Extra lookup!
    operator = self.operator_repo.get_by_id(ticket.operator_id)  # Extra lookup!
```

2. **Simpler Method Signatures:**
```python
# ✅ GOOD
def issue_ticket(
    self,
    vehicle: Vehicle,
    spot: ParkingSpot,
    gate: ParkingGate
) -> ParkingTicket:
    return ParkingTicket(
        ticket_id=self._generate_id(),
        vehicle=vehicle,
        parking_spot=spot,
        entry_gate=gate
    )

# ❌ BAD - Have to pass repos everywhere
def issue_ticket(
    self,
    vehicle_id: str,
    spot_id: str,
    gate_id: str,
    vehicle_repo: VehicleRepository,  # Ugly!
    spot_repo: SpotRepository,
    gate_repo: GateRepository
) -> ParkingTicket:
    # More code, more complexity
```

3. **Cleaner Service Layer:**
```python
# ✅ GOOD - Business logic is clear
def process_payment(self, ticket: ParkingTicket) -> Payment:
    hours = self._calculate_hours(ticket.entry_time, datetime.now())

    # Direct access to vehicle type
    amount = self.pricing_strategy.calculate(
        vehicle_type=ticket.vehicle.vehicle_type,
        hours=hours
    )

    return Payment(...)

# ❌ BAD - Service becomes a repository orchestrator
def process_payment(self, ticket: ParkingTicket) -> Payment:
    vehicle = self.vehicle_repo.get_by_id(ticket.vehicle_id)
    hours = self._calculate_hours(ticket.entry_time, datetime.now())
    amount = self.pricing_strategy.calculate(
        vehicle_type=vehicle.vehicle_type,  # Extra step
        hours=hours
    )
```

**When to Use IDs (Rare Cases):**

```python
# Only if there's a circular dependency issue
@dataclass
class ParkingFloor:
    floor_id: str
    spots: List[ParkingSpot]  # Floor has spots

@dataclass
class ParkingSpot:
    spot_id: str
    floor_id: str  # ✅ Use ID to avoid circular reference
    # floor: ParkingFloor  # ❌ Would create circular reference
```

**Interview Response:**
```
Interviewer: "Should Ticket store Vehicle object or vehicle_id?"

You: "Full Vehicle object. Since this is an in-memory LLD design,
      storing full objects makes the code simpler and more readable.

      The Ticket needs vehicle information to calculate pricing,
      generate invoices, and check vehicle type. Storing the full
      object avoids constant repository lookups.

      In a real database implementation, we'd use foreign keys, but
      for LLD we optimize for code clarity, not database normalization."

Interviewer: "What about memory?"

You: "In an in-memory system, references are cheap. Multiple tickets
      pointing to the same Vehicle object is fine - Python uses
      references anyway. If memory was a concern, we'd need to
      discuss caching strategies, but that's beyond typical LLD scope."
```

**Common Mistake:**
```python
# ❌ WRONG - Trying to simulate database in memory
@dataclass
class ParkingTicket:
    ticket_id: str
    vehicle_id: str  # Don't do this!
    parking_spot_id: str  # This is LLD, not database design!

# Leads to anti-pattern:
class TicketService:
    def __init__(
        self,
        ticket_repo,
        vehicle_repo,  # Too many repos!
        spot_repo,
        gate_repo,
        operator_repo
    ):
        # Service becomes repo manager, not business logic
```

**Rule of Thumb:**
- **Core entities that Ticket operates on** → Full objects
- **Static lookup data** → Can use IDs or Enums
- **Large collections** → Might use IDs, but discuss trade-offs

**Example:**
```python
@dataclass
class ParkingTicket:
    ticket_id: str
    vehicle: Vehicle  # ✅ Core entity - full object
    parking_spot: ParkingSpot  # ✅ Core entity - full object
    entry_gate: ParkingGate  # ✅ Needed for business logic - full object
    entry_time: datetime

    # If you had parking_lot reference:
    parking_lot_id: str  # ✅ OK - just for grouping, not used in logic
```

</details>

---

## Question 9: Service Method Granularity

```python
# Parking Lot - Vehicle exit flow

# Approach A: One method does everything
class PaymentService:
    def checkout_vehicle(self, ticket_id: str, payment_type: PaymentType) -> Invoice:
        # Get ticket
        ticket = self.ticket_repo.get_by_id(ticket_id)

        # Calculate amount
        hours = self._calculate_hours(ticket)
        amount = self.pricing_strategy.calculate(hours)

        # Process payment
        payment = Payment(...)
        self.payment_repo.save(payment)

        # Generate invoice
        invoice = Invoice(...)

        # Free spot
        ticket.parking_spot.free()
        self.spot_repo.save(ticket.parking_spot)

        return invoice

# Approach B: Separate methods
class PaymentService:
    def calculate_amount(self, ticket_id: str) -> float:
        ticket = self.ticket_repo.get_by_id(ticket_id)
        hours = self._calculate_hours(ticket)
        return self.pricing_strategy.calculate(hours)

    def process_payment(self, ticket_id: str, payment_type: PaymentType) -> Payment:
        amount = self.calculate_amount(ticket_id)
        payment = Payment(...)
        self.payment_repo.save(payment)
        return payment

    def generate_invoice(self, ticket_id: str) -> Invoice:
        payment = self.payment_repo.find_by_ticket(ticket_id)
        invoice = Invoice(...)
        return invoice

class TicketService:
    def free_spot(self, ticket_id: str):
        ticket = self.ticket_repo.get_by_id(ticket_id)
        ticket.parking_spot.free()
        self.spot_repo.save(ticket.parking_spot)

# Usage:
payment = payment_service.process_payment(ticket_id, PaymentType.UPI)
invoice = payment_service.generate_invoice(ticket_id)
ticket_service.free_spot(ticket_id)
```

**Interview Question: Which granularity is better?**

- A) One big method - simpler to use
- B) Separate methods - more flexible
- C) Both - facade pattern for common flow
- D) Depends on requirements

---
<details>
<summary>Answer</summary>

**C) Both - provide atomic operations AND convenient facade**

**The Right Approach:**

```python
class PaymentService:
    """
    Service provides both:
    1. Atomic operations (calculate, process, generate)
    2. Convenience facade (checkout)
    """

    # ✅ Atomic operations - single responsibility
    def calculate_amount(self, ticket_id: str) -> Money:
        """Calculate parking fee"""
        ticket = self.ticket_repo.get_by_id(ticket_id)
        return self.pricing_strategy.calculate(
            ticket,
            ticket.entry_time,
            datetime.now()
        )

    def process_payment(
        self,
        ticket_id: str,
        payment_type: PaymentType,
        amount: Optional[Money] = None
    ) -> Payment:
        """Process payment for a ticket"""
        # Check if already paid
        existing = self.payment_repo.find_by_ticket(ticket_id)
        if existing:
            raise DuplicatePaymentException(ticket_id)

        # Calculate if not provided
        if amount is None:
            amount = self.calculate_amount(ticket_id)

        payment = Payment(
            payment_id=self._generate_id(),
            ticket_id=ticket_id,
            amount=amount,
            payment_type=payment_type,
            status=PaymentStatus.COMPLETED,
            payment_time=datetime.now()
        )

        self.payment_repo.save(payment)
        return payment

    def generate_invoice(self, ticket_id: str) -> Invoice:
        """Generate invoice for paid ticket"""
        ticket = self.ticket_repo.get_by_id(ticket_id)
        payment = self.payment_repo.get_by_ticket(ticket_id)

        invoice = Invoice(
            invoice_id=self._generate_id(),
            ticket=ticket,
            payment=payment,
            exit_time=datetime.now(),
            amount=payment.amount
        )

        return invoice

    # ✅ Facade method - convenient workflow
    def checkout_and_pay(
        self,
        ticket_id: str,
        payment_type: PaymentType
    ) -> tuple[Payment, Invoice]:
        """
        Convenience method for complete checkout flow.

        For custom flows, use individual methods:
        - calculate_amount() - to show amount before payment
        - process_payment() - when ready to pay
        - generate_invoice() - after payment
        """
        # This orchestrates the workflow
        payment = self.process_payment(ticket_id, payment_type)
        invoice = self.generate_invoice(ticket_id)

        return payment, invoice
```

**Why This is Best:**

1. **Flexibility for Different Flows:**
```python
# Flow 1: Show amount first, pay later
amount = payment_service.calculate_amount(ticket_id)
print(f"Amount to pay: {amount}")

user_confirms = input("Proceed? (y/n)")
if user_confirms == 'y':
    payment = payment_service.process_payment(ticket_id, PaymentType.UPI)
    invoice = payment_service.generate_invoice(ticket_id)

# Flow 2: Quick checkout
payment, invoice = payment_service.checkout_and_pay(ticket_id, PaymentType.CASH)

# Flow 3: Pre-calculated amount (e.g., from discount code)
discounted_amount = calculate_discount(ticket_id)
payment = payment_service.process_payment(
    ticket_id,
    PaymentType.CARD,
    amount=discounted_amount
)
```

2. **Testability:**
```python
# Easy to test individual pieces
def test_calculate_amount():
    amount = payment_service.calculate_amount("TKT-1")
    assert amount == Money(100)

def test_duplicate_payment():
    payment_service.process_payment("TKT-1", PaymentType.UPI)

    with pytest.raises(DuplicatePaymentException):
        payment_service.process_payment("TKT-1", PaymentType.CASH)
```

3. **Transaction Boundaries:**
```python
# Each atomic method is a transaction
def process_payment(self, ticket_id: str, payment_type: PaymentType) -> Payment:
    # Single responsibility - single transaction
    payment = Payment(...)
    self.payment_repo.save(payment)
    return payment

# Facade orchestrates transactions
def checkout_and_pay(self, ticket_id: str, payment_type: PaymentType):
    # Multiple transactions, coordinated
    payment = self.process_payment(ticket_id, payment_type)
    invoice = self.generate_invoice(ticket_id)

    # If we need to free spot, separate service handles it
    # (Different aggregate root)
    return payment, invoice
```

**Interview Conversation:**
```
Interviewer: "Should checkout be one method or multiple?"

You: "I'd provide both. Individual methods (calculate_amount, process_payment,
     generate_invoice) for flexibility, and a facade method (checkout_and_pay)
     for the common happy path.

     This gives callers options:
     - Display amount before payment? Use calculate_amount first
     - Bulk operations? Call methods individually
     - Simple checkout? Use the facade

     Each method has a single responsibility and clear transaction boundary."

Interviewer: "What about freeing the parking spot?"

You: "That's a different aggregate root (ParkingSpot vs Payment), so I'd put
     it in TicketService.free_spot(). The controller orchestrates:

     payment, invoice = payment_service.checkout_and_pay(...)
     ticket_service.free_spot(ticket_id)

     This maintains service boundaries."
```

**Controller Layer:**
```python
class PaymentController:
    def checkout(self, request_data: dict) -> tuple[dict, int]:
        """POST /checkout"""
        ticket_id = request_data['ticket_id']
        payment_type = PaymentType[request_data['payment_type']]

        try:
            # Use facade for simple flow
            payment, invoice = self.payment_service.checkout_and_pay(
                ticket_id,
                payment_type
            )

            # Free spot (different service)
            self.ticket_service.free_spot(ticket_id)

            return {
                'status': 'success',
                'data': {
                    'payment': PaymentDTO.from_payment(payment),
                    'invoice': InvoiceDTO.from_invoice(invoice)
                }
            }, 200

        except DuplicatePaymentException as e:
            return {'status': 'error', 'message': str(e)}, 400

    def get_amount(self, ticket_id: str) -> tuple[dict, int]:
        """GET /tickets/{ticket_id}/amount"""
        # Use atomic method for specific query
        amount = self.payment_service.calculate_amount(ticket_id)

        return {
            'status': 'success',
            'data': {'amount': float(amount.amount)}
        }, 200
```

**Key Takeaway:**
- **Atomic methods** - Each does ONE thing (SRP)
- **Facade method** - Orchestrates common workflow
- **Don't cross aggregate boundaries** - Freeing spot is TicketService's job
- **Controller coordinates** - Calls multiple services if needed

</details>

---

## Question 10: State Management - Who Owns Status Updates?

```python
# Tic Tac Toe - Game state

# Approach A: Model updates its own state
@dataclass
class Game:
    board: Board
    current_player: Player
    status: GameStatus = GameStatus.IN_PROGRESS
    winner: Optional[Player] = None

    def make_move(self, row: int, col: int):
        self.board.place_symbol(row, col, self.current_player.symbol)
        self._check_and_update_game_state()  # Model updates itself
        self._switch_player()

    def _check_and_update_game_state(self):
        if self.board.has_winner():
            self.status = GameStatus.FINISHED
            self.winner = self.current_player
        elif self.board.is_full():
            self.status = GameStatus.DRAW

# Approach B: Service updates model state
@dataclass
class Game:
    board: Board
    current_player: Player
    status: GameStatus = GameStatus.IN_PROGRESS
    winner: Optional[Player] = None

class GameService:
    def make_move(self, game: Game, row: int, col: int):
        game.board.place_symbol(row, col, game.current_player.symbol)

        # Service controls state transitions
        if game.board.has_winner():
            game.status = GameStatus.FINISHED
            game.winner = game.current_player
        elif game.board.is_full():
            game.status = GameStatus.DRAW

        self._switch_player(game)

# Approach C: Separate state manager
class GameStateManager:
    def update_state(self, game: Game):
        if game.board.has_winner():
            game.status = GameStatus.FINISHED
            game.winner = game.current_player
        elif game.board.is_full():
            game.status = GameStatus.DRAW

class GameService:
    def __init__(self):
        self.state_manager = GameStateManager()

    def make_move(self, game: Game, row: int, col: int):
        game.board.place_symbol(row, col, game.current_player.symbol)
        self.state_manager.update_state(game)
        self._switch_player(game)
```

**Interview Question: Where should state management logic live?**

- A) Model - encapsulation and domain logic
- B) Service - separation of concerns
- C) Separate state manager - single responsibility
- D) Mix - model for simple, service for complex

---
<details>
<summary>Answer</summary>

**A) Model - encapsulation and domain logic**

**Why:**

**Domain models should protect their invariants:**
```python
@dataclass
class Game:
    """Game model - owns its state and ensures consistency"""
    board: Board
    current_player: Player
    status: GameStatus = GameStatus.IN_PROGRESS
    winner: Optional[Player] = None

    def make_move(self, row: int, col: int, player: Player):
        """Public API - enforces rules and maintains consistency"""
        # Validation
        self._validate_move(row, col, player)

        # State change
        self.board.place_symbol(row, col, player.symbol)

        # Update game state automatically
        self._update_game_state()

        # Switch turns
        self._switch_player()

    def _validate_move(self, row: int, col: int, player: Player):
        """Enforce game rules"""
        if self.status != GameStatus.IN_PROGRESS:
            raise GameOverException("Game is already finished")

        if player != self.current_player:
            raise WrongPlayerException(f"Not {player.name}'s turn")

        if not self.board.is_valid_position(row, col):
            raise InvalidMoveException("Invalid position")

        if not self.board.is_empty(row, col):
            raise CellOccupiedException("Cell already occupied")

    def _update_game_state(self):
        """Update game status based on board state"""
        # Model knows how to check its own state
        if self.board.has_winner():
            self.status = GameStatus.FINISHED
            self.winner = self.current_player
        elif self.board.is_full():
            self.status = GameStatus.DRAW
            self.winner = None

    def _switch_player(self):
        """Switch to next player"""
        if self.status == GameStatus.IN_PROGRESS:
            # Get next player logic
            self.current_player = self._get_next_player()

    # ✅ Model exposes high-level behavior, not state setters
    # ❌ NO: set_status(), set_winner(), set_current_player()
```

**Service Layer - Thin Orchestration:**
```python
class GameService:
    """Service orchestrates, model enforces rules"""

    def __init__(self, game_repo: GameRepository):
        self.game_repo = game_repo

    def make_move(
        self,
        game_id: str,
        row: int,
        col: int,
        player_id: str
    ) -> Game:
        """Service handles persistence and lookup, model handles logic"""
        # Get entities
        game = self.game_repo.get_by_id(game_id)
        player = game.get_player_by_id(player_id)

        # Model does the work
        game.make_move(row, col, player)

        # Persist
        self.game_repo.save(game)

        return game
```

**Why Not Service-Managed State:**

```python
# ❌ BAD - Anemic domain model
@dataclass
class Game:
    board: Board
    current_player: Player
    status: GameStatus = GameStatus.IN_PROGRESS
    winner: Optional[Player] = None

    # Just getters/setters - no behavior!

class GameService:
    def make_move(self, game: Game, row: int, col: int, player: Player):
        # Service has all the logic - model is just data
        if game.status != GameStatus.IN_PROGRESS:
            raise GameOverException()

        if player != game.current_player:
            raise WrongPlayerException()

        game.board.place_symbol(row, col, player.symbol)

        # Service manipulating model state
        if game.board.has_winner():
            game.status = GameStatus.FINISHED
            game.winner = game.current_player
        elif game.board.is_full():
            game.status = GameStatus.DRAW

        # Problem: What if someone else creates Game and forgets to check state?
        # Model can't protect itself!
```

**Real Problem with Service-Managed State:**
```python
# With anemic model:
game = Game(...)
game.status = GameStatus.FINISHED  # Oops! No validation
game.winner = None  # Inconsistent state!

# With rich domain model:
game = Game(...)
game.make_move(0, 0, player)  # Only way to change state
# game.status = GameStatus.FINISHED  # Doesn't compile! No setter!
```

**When Service CAN Manage State:**

Only when coordinating multiple aggregates:
```python
class ParkingService:
    def checkout_vehicle(self, ticket_id: str):
        """Service coordinates multiple aggregates"""
        ticket = self.ticket_repo.get_by_id(ticket_id)

        # Each model manages its own state
        ticket.complete()  # Ticket updates itself
        ticket.parking_spot.free()  # Spot updates itself

        # Service just coordinates, doesn't manipulate internals
        self.ticket_repo.save(ticket)
        self.spot_repo.save(ticket.parking_spot)
```

**Interview Answer:**

"State management should live in the domain model because:

1. **Encapsulation**: Model protects its invariants - can't have inconsistent state
2. **Domain Logic**: State transitions are business rules, belong in domain
3. **Testability**: Test model in isolation without service dependencies
4. **Reusability**: Other services can use model without duplicating logic

The service layer should:
- Load entities from repositories
- Call domain methods (not manipulate state directly)
- Persist changes
- Coordinate multiple aggregates

**Red flag**: If your model is all getters/setters and service has all the logic,
you have an anemic domain model - common anti-pattern in LLD interviews."

**Show You Know Advanced Concepts:**
```
Interviewer: "But doesn't that make the model too fat?"

You: "That's a sign of proper domain-driven design. The model contains domain
     logic, the service coordinates workflows. If the model gets truly complex,
     I can extract strategy patterns (like we did with pricing) or create
     domain services for operations spanning multiple entities.

     But simple state management like checking win conditions? That's core
     domain logic - belongs in the model."
```

**Perfect Answer in Code:**
```python
# ✅ PERFECT - Rich domain model
class Game:
    # Private state, public behavior
    def make_move(self, row, col, player):
        """Exposes WHAT you can do, not HOW it's done"""
        self._validate_move(row, col, player)
        self._apply_move(row, col, player)
        self._update_state()
        self._advance_turn()

    def is_game_over(self) -> bool:
        """Query method - safe to call anytime"""
        return self.status != GameStatus.IN_PROGRESS

    def get_winner(self) -> Optional[Player]:
        """Query method"""
        return self.winner if self.is_game_over() else None

    # ❌ NO PUBLIC SETTERS
    # def set_status(self, status): ...
    # def set_winner(self, player): ...
```

**Key Takeaway:**
- **Models**: Own state, expose behavior, protect invariants
- **Services**: Orchestrate, don't manipulate
- **Tell, don't ask**: `game.make_move()` not `game.get_board().set_cell()`

</details>

---

## Summary

These 10 questions cover critical design decisions you'll face in LLD interviews:

1. **Enum vs Boolean** - Domain modeling choices
2. **ID Generation** - Auto-increment vs UUID vs hybrid
3. **Validation Layers** - Controller vs Service vs Model
4. **Repository Methods** - Specific vs generic methods
5. **Exception Handling** - Boolean vs Exception vs Result objects
6. **Null Handling** - Optional vs Exceptions vs Null objects
7. **Strategy Pattern** - Context passing decisions
8. **Model Relationships** - Composition vs references
9. **Service Granularity** - Atomic vs facade methods
10. **State Management** - Where domain logic belongs

**Interview Pro Tips:**

✅ **Think about:** Extensibility, clarity, interview time
✅ **Ask about:** Scale, distribution, future requirements
✅ **Mention trade-offs:** Show you understand different approaches
✅ **Stay practical:** Don't over-engineer for 45-minute interviews

**Common Mistakes to Avoid:**

❌ Boolean when Enum is better (not future-proof)
❌ Anemic domain models (logic in service, not model)
❌ Generic repository methods (leaks abstraction)
❌ Storing IDs instead of objects in LLD (over-complicating)
❌ One giant method (violates SRP)
❌ Service managing model state (breaks encapsulation)

Good luck with your LLD interviews! 🚀
