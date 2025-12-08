# Parking Lot System - Python Implementation

A complete, interview-ready implementation of a parking lot management system following SOLID principles and design patterns. **No external frameworks required** - pure Python with proper layered architecture.

## 🎯 Features

- Multi-floor parking lot support
- Multiple vehicle types (Car, Bike, Truck, Bus, Scooter)
- Multiple spot types (Small, Medium, Large)
- Automatic spot allocation using Strategy pattern
- Flexible pricing strategy
- Payment processing
- Invoice generation
- In-memory data storage (easily extendable to database)
- **Controllers for request handling** (framework-agnostic)

## 📁 Project Structure

```
code-parking-lot/
├── src/
│   ├── controllers/        # Request/Response handling
│   │   ├── ticket_controller.py
│   │   └── payment_controller.py
│   ├── services/           # Business logic layer
│   │   ├── ticket_service.py
│   │   └── payment_service.py
│   ├── repositories/       # Data access layer
│   │   ├── parking_spot_repository.py
│   │   ├── vehicle_repository.py
│   │   ├── ticket_repository.py
│   │   └── payment_repository.py
│   ├── strategies/         # Strategy pattern implementations
│   │   ├── spot_allocation_strategy.py
│   │   ├── nearest_spot_strategy.py
│   │   └── pricing_strategy.py
│   ├── models/             # Domain models
│   │   ├── vehicle.py
│   │   ├── parking_spot.py
│   │   ├── parking_ticket.py
│   │   ├── payment.py
│   │   └── ...
│   ├── enums/              # Enum definitions
│   │   ├── vehicle_type.py
│   │   ├── spot_type.py
│   │   └── ...
│   └── exceptions/         # Custom exceptions
│       └── parking_exceptions.py
├── tests/                  # Unit tests
│   ├── test_controllers.py      # 10 tests
│   ├── test_ticket_service.py   # 5 tests
│   ├── test_payment_service.py  # 5 tests
│   └── test_spot_allocation.py  # 5 tests
├── main.py                 # Demo application
├── DIAGRAMS.md            # Complete system diagrams
├── INTERVIEW_GUIDE.md     # 45-minute interview strategy
├── ARCHITECTURE.md        # Architecture explanation
└── README.md              # This file
```

## 🏗️ Architecture - Layered Design

```
┌─────────────────────────────────┐
│  CONTROLLERS                    │  ← Validate input, format output
│  (Presentation Layer)           │     Return (response_dict, status_code)
├─────────────────────────────────┤
│  SERVICES                       │  ← Business logic, orchestration
│  (Business Logic Layer)         │     Use repositories & strategies
├─────────────────────────────────┤
│  REPOSITORIES                   │  ← CRUD operations, data access
│  (Data Access Layer)            │     In-memory storage
├─────────────────────────────────┤
│  MODELS + ENUMS                 │  ← Domain entities, types
│  (Domain Layer)                 │     Business objects
└─────────────────────────────────┘
│  STRATEGIES                     │  ← Pluggable algorithms
│  (Cross-cutting)                │     Spot allocation, pricing
└─────────────────────────────────┘
```

### Why Controllers?

Controllers handle **request validation** and **response formatting**, keeping services clean and framework-agnostic:

```python
# Controller (handles HTTP-like requests)
class TicketController:
    def issue_ticket(self, request_data: dict) -> tuple[dict, int]:
        # 1. Validate input
        if not request_data.get('license_plate'):
            return {'error': 'license_plate required'}, 400

        # 2. Convert types (string → enum)
        vehicle_type = VehicleType[request_data['vehicle_type']]

        # 3. Call service
        ticket = self.service.issue_ticket(...)

        # 4. Format response
        return {'status': 'success', 'data': {...}}, 201

# Service (pure business logic)
class TicketService:
    def issue_ticket(self, license_plate, vehicle_type, gate):
        # No HTTP concerns, just business logic
        vehicle = self.vehicle_repo.find_or_create(license_plate)
        spot = self.allocation_strategy.find_spot(...)
        ticket = ParkingTicket(...)
        return self.ticket_repo.save(ticket)
```

**Benefits**:
- Services can be tested without mocking HTTP
- Same services work with Flask, FastAPI, CLI, or message queues
- Clear separation: Controller = I/O, Service = Logic
- Framework-independent core logic

## 🚀 Quick Start

### Installation

```bash
cd class-12-code-parking-lot

# No dependencies needed! Pure Python 3.8+
# (pytest optional for running tests)
```

### Run Demo

```bash
python3 main.py
```

**Output:**
```
============================================================
PARKING LOT SYSTEM DEMO
============================================================

[SETUP] Initializing parking lot...
✓ Parking lot initialized with 5 spots
✓ Attendant: Rajesh Kumar

[SCENARIO 1] Car arrives at parking lot
✓ Ticket issued: TKT-B0A9C602
  - Vehicle: KA01AB1234
  - Spot: B-1 (MEDIUM)
  - Entry time: 2025-12-06 00:03:55

[SCENARIO 4] Car owner makes payment
✓ Payment processed: PAY-1F1C91F4
  - Amount: ₹80
  - Method: UPI
  - Status: DONE

...
✓ Demo completed successfully!
```

### Run Tests

```bash
# Run all tests
python3 -m unittest discover tests -v

# Result: 25 tests passing ✓
```

## 💻 Usage Example

```python
from src.controllers import TicketController, PaymentController
from src.services import TicketService, PaymentService
from src.repositories import *
from src.strategies import NearestSpotStrategy, HourlyPricingStrategy
from src.models import ParkingSpot
from src.enums import SpotType, VehicleType, PaymentType

# Initialize system
spot_repo = ParkingSpotRepository()
vehicle_repo = VehicleRepository()
ticket_repo = TicketRepository()
payment_repo = PaymentRepository()

allocation_strategy = NearestSpotStrategy()
pricing_strategy = HourlyPricingStrategy()

ticket_service = TicketService(
    spot_repo, vehicle_repo, ticket_repo, allocation_strategy
)
payment_service = PaymentService(
    payment_repo, ticket_repo, pricing_strategy
)

ticket_controller = TicketController(ticket_service)
payment_controller = PaymentController(payment_service)

# Create parking spot
spot = ParkingSpot(id="B-1", spot_number=1, spot_type=SpotType.MEDIUM)
spot_repo.save(spot)

# Issue ticket
request = {
    'license_plate': 'KA01AB1234',
    'vehicle_type': 'CAR',
    'entry_gate_id': 'GATE-1'
}
response, status = ticket_controller.issue_ticket(request)

if status == 201:
    ticket_id = response['data']['ticket_id']
    print(f"✓ Ticket issued: {ticket_id}")

    # Process payment
    payment_request = {
        'ticket_id': ticket_id,
        'payment_type': 'UPI'
    }
    payment_response, payment_status = payment_controller.process_payment(payment_request)

    if payment_status == 200:
        amount = payment_response['data']['amount']
        print(f"✓ Payment processed: ₹{amount}")
```

## 📊 Complete Request Flow

### Example: Issue Ticket

```
1. Client calls controller
   ticket_controller.issue_ticket({
       'license_plate': 'KA01AB1234',
       'vehicle_type': 'CAR'
   })

2. Controller validates
   - Check license_plate exists ✓
   - Convert "CAR" → VehicleType.CAR ✓

3. Controller calls service
   ticket_service.issue_ticket(license_plate, vehicle_type, gate)

4. Service executes business logic
   - Find/create vehicle
   - Get available spots
   - Use strategy to allocate spot
   - Occupy spot
   - Create and save ticket

5. Service returns ticket to controller

6. Controller formats response
   - Convert datetime → ISO string
   - Convert enums → strings
   - Wrap in JSON structure
   - Set status code (201)

7. Controller returns
   ({'status': 'success', 'data': {...}}, 201)
```

See **DIAGRAMS.md** for complete sequence diagrams and flow charts!

## 🎨 Design Patterns

### 1. Strategy Pattern
**Where**: Spot allocation and pricing
```python
class SpotAllocationStrategy(ABC):
    @abstractmethod
    def find_spot(self, spots, vehicle_type):
        pass

class NearestSpotStrategy(SpotAllocationStrategy):
    def find_spot(self, spots, vehicle_type):
        # Implementation
```

**Benefit**: Easy to add new strategies without modifying existing code

### 2. Repository Pattern
**Where**: Data access layer
```python
class ParkingSpotRepository:
    def find_available(self):
        return [spot for spot in self._spots.values() if spot.is_available()]
```

**Benefit**: Abstract storage mechanism (can swap in-memory → database)

### 3. Service Layer Pattern
**Where**: Business logic
```python
class TicketService:
    def issue_ticket(self, ...):
        # Business logic here
```

**Benefit**: Centralized business logic, easy to test

### 4. Dependency Injection
**Where**: Services depend on interfaces
```python
class TicketService:
    def __init__(self, spot_repo, vehicle_repo, ticket_repo, strategy):
        self.spot_repository = spot_repo
        self.allocation_strategy = strategy  # Can inject any strategy!
```

**Benefit**: Loose coupling, easy testing with mocks

## 🧪 Testing Strategy

### Layer-by-Layer Testing

**1. Strategy Tests** (5 tests)
- Test spot allocation logic
- Test pricing calculations

**2. Service Tests** (10 tests)
- Test business logic
- Test error scenarios
- Mock repositories

**3. Controller Tests** (10 tests)
- Test input validation
- Test response formatting
- Test status codes

```python
# Example: Controller test
def test_issue_ticket_missing_license_plate(self):
    request_data = {'vehicle_type': 'CAR'}  # Missing license_plate

    response, status_code = self.controller.issue_ticket(request_data)

    self.assertEqual(status_code, 400)
    self.assertEqual(response['error']['code'], 'VALIDATION_ERROR')
```

## 🎓 SOLID Principles

✅ **Single Responsibility**: Each class has one job
- Controller: I/O handling
- Service: Business logic
- Repository: Data access

✅ **Open/Closed**: Extensible without modification
- Add new strategies without changing services

✅ **Liskov Substitution**: Strategies are interchangeable
- Any `SpotAllocationStrategy` works in `TicketService`

✅ **Interface Segregation**: Focused interfaces
- Each repository has specific methods

✅ **Dependency Inversion**: Depend on abstractions
- Services depend on strategy interfaces, not implementations

## 💡 Interview Tips

### Time Allocation (45 minutes)

**0-5 min**: Clarify requirements, draw basic diagram
**5-20 min**: Write models, enums, services
**20-35 min**: Write controllers, repositories
**35-40 min**: Write 2-3 tests
**40-45 min**: Discuss extensions

### What to Focus On

✅ **Must Have**:
- Models (Vehicle, Spot, Ticket)
- Services (TicketService)
- Basic repository
- 1-2 tests

✅ **Good to Have**:
- Controllers
- Strategies
- Complete tests

✅ **Nice to Have**:
- Multiple strategies
- Exception handling
- Documentation

### What to Say

When explaining controllers:
> "Controllers handle request validation and response formatting. Services contain pure business logic. This keeps the code testable and framework-independent. In production, we'd wrap these controllers in Flask or FastAPI endpoints."

## 🔮 Future Improvements

### Framework Integration
- **Flask REST API**: Wrap controllers in Flask routes
- **FastAPI**: Use Pydantic models for validation
- **Django**: Integrate with Django ORM

### Database
- Replace in-memory repositories with SQLAlchemy
- Add migrations (Alembic)
- Connection pooling

### Advanced Features
- Real-time availability via WebSockets
- Reservation system
- Dynamic pricing (peak hours, events)
- Multi-tenant support
- Analytics dashboard

### Production Concerns
- Authentication & Authorization (JWT)
- Rate limiting
- Logging & monitoring
- Caching (Redis) for spot availability
- Message queues (Celery) for async operations
- Docker containerization
- Kubernetes deployment

### API Layer (Future)
```python
# Example: Flask integration (future improvement)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/tickets', methods=['POST'])
def issue_ticket_endpoint():
    response, status = ticket_controller.issue_ticket(request.get_json())
    return jsonify(response), status

# Similarly for FastAPI:
from fastapi import FastAPI

app = FastAPI()

@app.post('/tickets')
def issue_ticket_endpoint(request: TicketRequest):
    response, status = ticket_controller.issue_ticket(request.dict())
    return response
```

## 📚 Documentation

- **README.md** (this file): Overview and usage
- **DIAGRAMS.md**: Complete class, sequence, and package diagrams
- **ARCHITECTURE.md**: Detailed architecture explanation
- **INTERVIEW_GUIDE.md**: 45-minute interview strategy
- **sequence-diagrams.puml**: PlantUML sequence diagrams

## 🏆 Key Highlights

### Why This Implementation Stands Out

1. **Complete Layered Architecture**
   - Clear separation of concerns
   - Framework-independent core

2. **Production-Ready Patterns**
   - Strategy, Repository, Service patterns
   - SOLID principles throughout

3. **Comprehensive Testing**
   - 25 tests covering all layers
   - Happy path + error scenarios

4. **Interview-Friendly**
   - Can be coded in 45 minutes
   - Progressive implementation strategy
   - Clear extension points

5. **Well-Documented**
   - Detailed diagrams
   - Code comments
   - Usage examples

## 📈 Complexity

- **Time Complexity**:
  - Issue ticket: O(n) where n = available spots
  - Process payment: O(1)
  - Find spot: O(n) (can optimize with indexing)

- **Space Complexity**: O(t + v + s) where:
  - t = number of tickets
  - v = number of vehicles
  - s = number of spots

## 🤝 Contributing

This is a reference implementation for learning. Feel free to:
- Add new strategies
- Implement database layer
- Add more test cases
- Improve documentation

## 📝 License

MIT License - Free to use for learning and interviews!

## 🎯 Summary

This parking lot system demonstrates:
- ✅ Clean architecture with clear layers
- ✅ SOLID principles and design patterns
- ✅ Framework-agnostic design
- ✅ Comprehensive testing
- ✅ Interview-ready structure
- ✅ Production-quality code

**Perfect for**: LLD interviews, learning design patterns, understanding layered architecture

---

**Author**: Generated with Claude Code
**Python Version**: 3.8+
**Tests**: 25/25 passing ✓
**Lines of Code**: ~1000 (excluding tests)

Happy Coding! 🚀
