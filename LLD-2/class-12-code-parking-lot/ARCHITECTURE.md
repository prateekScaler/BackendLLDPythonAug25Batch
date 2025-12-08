# Architecture Guide - Parking Lot System

## Complete Layered Architecture

```
┌─────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER (Controllers + Flask App)           │
│  - TicketController                                     │
│  - PaymentController                                    │
│  - app.py (Flask REST API)                              │
│                                                          │
│  Responsibilities:                                       │
│  • HTTP request/response handling                        │
│  • Input validation                                      │
│  • Format conversions (string → enum)                   │
│  • Error formatting (exception → JSON)                  │
│  • HTTP status codes                                     │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  BUSINESS LOGIC LAYER (Services)                        │
│  - TicketService                                        │
│  - PaymentService                                       │
│                                                          │
│  Responsibilities:                                       │
│  • Core business logic                                   │
│  • Business rule validation                              │
│  • Orchestration of repositories                        │
│  • Domain exception handling                            │
│  • Strategy pattern implementation                       │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  DATA ACCESS LAYER (Repositories)                       │
│  - ParkingSpotRepository                                │
│  - VehicleRepository                                    │
│  - TicketRepository                                     │
│  - PaymentRepository                                    │
│                                                          │
│  Responsibilities:                                       │
│  • CRUD operations                                       │
│  • Query methods                                         │
│  • Data persistence abstraction                         │
│  • In-memory storage (can be replaced with DB)          │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  DOMAIN LAYER (Models + Enums)                          │
│  - Vehicle, ParkingSpot, ParkingTicket, etc.           │
│  - VehicleType, SpotType, PaymentStatus, etc.          │
│                                                          │
│  Responsibilities:                                       │
│  • Domain entities                                       │
│  • Business enumerations                                │
│  • Domain logic (e.g., spot.is_available())            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  CROSS-CUTTING CONCERNS                                  │
│  - Strategies (SpotAllocationStrategy, PricingStrategy) │
│  - Exceptions (ParkingLotException hierarchy)           │
└─────────────────────────────────────────────────────────┘
```

---

## Why Controllers Are Separate from Services

### Controllers (Presentation Layer)
**Purpose**: Handle HTTP-specific concerns

**Responsibilities**:
1. ✅ Parse HTTP requests
2. ✅ Validate input format
3. ✅ Convert strings to domain types (e.g., "CAR" → VehicleType.CAR)
4. ✅ Call service methods
5. ✅ Format responses as JSON
6. ✅ Set HTTP status codes (200, 201, 400, 404, 500)
7. ✅ Convert exceptions to error responses

**What Controllers DON'T Do**:
- ❌ Business logic
- ❌ Database operations
- ❌ Complex validations
- ❌ Calculations

### Services (Business Logic Layer)
**Purpose**: Implement business rules

**Responsibilities**:
1. ✅ Core business logic
2. ✅ Business rule validation
3. ✅ Orchestrate multiple repositories
4. ✅ Apply strategies
5. ✅ Throw domain exceptions

**What Services DON'T Do**:
- ❌ HTTP concerns (status codes, headers)
- ❌ JSON formatting
- ❌ Direct database access (use repositories)

---

## Request Flow Example

### Scenario: Issue a parking ticket

```
1. HTTP Request arrives
   POST /tickets
   {"license_plate": "KA01AB1234", "vehicle_type": "CAR"}

2. Flask app.py routes to controller
   ticket_controller.issue_ticket(request_data)

3. TicketController validates and converts
   - Check if license_plate exists
   - Convert "CAR" string → VehicleType.CAR enum
   - Create ParkingGate object

4. Controller calls service
   ticket_service.issue_ticket(license_plate, vehicle_type, entry_gate)

5. TicketService executes business logic
   - Find or create vehicle in VehicleRepository
   - Get available spots from ParkingSpotRepository
   - Use SpotAllocationStrategy to find matching spot
   - Occupy the spot
   - Create ticket
   - Save ticket in TicketRepository
   - Return ticket

6. Service returns ticket to controller

7. Controller formats response
   - Convert datetime → ISO string
   - Convert enums → strings
   - Wrap in JSON structure
   - Set status code 201

8. Flask sends HTTP response
   {
     "status": "success",
     "data": {
       "ticket_id": "TKT-12345",
       "entry_time": "2025-12-06T10:30:00",
       ...
     }
   }
```

---

## Why This Separation Matters

### 1. **Framework Independence**
Services don't know about Flask/FastAPI/Django. Tomorrow you can:
- Switch from Flask to FastAPI
- Add a CLI interface
- Add GraphQL API
- Expose via gRPC

**All without changing service layer!**

### 2. **Easier Testing**
```python
# Test service without HTTP
def test_issue_ticket():
    ticket = ticket_service.issue_ticket(...)  # No HTTP mocking needed
    assert ticket.ticket_id is not None

# Test controller with HTTP concerns
def test_issue_ticket_api():
    response, status = controller.issue_ticket({"license_plate": "..."})
    assert status == 201
    assert response['status'] == 'success'
```

### 3. **Single Responsibility Principle**
- Controller: HTTP translation
- Service: Business logic
- Repository: Data access

Each layer has ONE reason to change.

### 4. **Reusability**
Same services can be used by:
- REST API (Flask/FastAPI)
- Background jobs (Celery)
- Admin CLI tools
- Message queue consumers
- WebSocket handlers

---

## Code Comparison

### ❌ Without Controllers (Bad)

```python
@app.route('/tickets', methods=['POST'])
def issue_ticket():
    # Business logic mixed with HTTP handling!
    license_plate = request.json.get('license_plate')

    # Find vehicle in database
    vehicle = db.session.query(Vehicle).filter_by(license_plate=license_plate).first()

    # Allocate spot
    spots = db.session.query(Spot).filter_by(status='FREE').all()
    spot = find_matching_spot(spots, vehicle_type)

    # Create ticket
    ticket = Ticket(...)
    db.session.add(ticket)
    db.session.commit()

    return jsonify({...}), 201
```

**Problems**:
1. Can't test business logic without Flask
2. Can't reuse logic in CLI or background jobs
3. Hard to switch databases
4. Violates SRP

### ✅ With Controllers (Good)

```python
# Controller (HTTP layer)
@app.route('/tickets', methods=['POST'])
def issue_ticket():
    response, status = ticket_controller.issue_ticket(request.get_json())
    return jsonify(response), status

# Service (Business logic)
class TicketService:
    def issue_ticket(self, license_plate, vehicle_type, gate):
        # Pure business logic, no HTTP concerns
        vehicle = self.vehicle_repo.find_or_create(license_plate)
        spot = self.allocation_strategy.find_spot(...)
        ticket = ParkingTicket(...)
        return self.ticket_repo.save(ticket)
```

**Benefits**:
1. ✅ Test business logic independently
2. ✅ Reuse in any context
3. ✅ Easy to switch storage
4. ✅ Clean separation

---

## When to Skip Controllers (Interview Context)

### Skip Controllers If:
1. ⏰ **Time constrained** (< 30 minutes)
2. 🎯 **Interviewer focuses on algorithms** (not architecture)
3. 📝 **Interviewer says** "don't worry about API layer"
4. 🔍 **Problem is about data structures** (e.g., LRU cache)

### Include Controllers If:
1. 🏗️ **System design question** ("Design a parking lot API")
2. 🌐 **REST API mentioned** explicitly
3. ⏳ **Sufficient time** (> 40 minutes)
4. 💼 **Senior role** (expected to know layering)
5. 🗣️ **Interviewer asks** "How would you expose this as API?"

---

## Interview Communication Tips

### If You Skip Controllers
Say this explicitly:
> "I'm focusing on the business logic layer - the services and domain models. In production, I'd add a controller layer on top to handle HTTP requests, but for this interview, I'll focus on the core parking lot logic. Does that work?"

### If You Include Controllers
Explain the separation:
> "I'm separating concerns into layers. Controllers will handle HTTP requests and validation, then delegate to services for business logic. This keeps the code testable and framework-agnostic. I'll start with services first, then add controllers if we have time."

---

## Production Considerations

### What's Missing (But Should Be Added)

1. **Authentication/Authorization**
   ```python
   @require_role('ATTENDANT')
   def issue_ticket():
       ...
   ```

2. **Request Logging**
   ```python
   @log_request
   def issue_ticket():
       ...
   ```

3. **Rate Limiting**
   ```python
   @rate_limit(requests=100, per='minute')
   def issue_ticket():
       ...
   ```

4. **Input Validation (Pydantic/Marshmallow)**
   ```python
   class IssueTicketRequest(BaseModel):
       license_plate: str = Field(..., pattern=r'^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$')
       vehicle_type: VehicleType
   ```

5. **API Documentation (OpenAPI/Swagger)**
   ```python
   @api.doc(responses={201: 'Success', 400: 'Bad Request'})
   def issue_ticket():
       ...
   ```

---

## Complete Architecture Benefits

| Without Controllers | With Controllers |
|---------------------|------------------|
| Services know about HTTP | Services are framework-agnostic |
| Can't test without web framework | Easy unit testing |
| Hard to add new interfaces | Easy to add CLI/GraphQL/gRPC |
| Violates SRP | Clean separation of concerns |
| Tight coupling | Loose coupling |

---

## Summary

**Controllers = HTTP Translation Layer**
- Input validation
- Format conversion
- Error formatting
- Status codes

**Services = Business Logic**
- Core domain rules
- Orchestration
- Exception handling

**Repositories = Data Access**
- CRUD operations
- Queries

**Models = Domain Entities**
- Business objects
- Domain logic

This is the **industry-standard layered architecture** used in production systems! 🚀
