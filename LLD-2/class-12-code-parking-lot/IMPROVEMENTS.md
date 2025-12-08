# Parking Lot System - Interview-Ready Improvements

This document outlines small, practical improvements you can discuss or implement during LLD interviews to demonstrate design maturity and best practices.

---

## 1. Base Model Pattern

### Why?
- **DRY Principle**: Common attributes (id, timestamps, audit fields) repeated across models
- **Consistency**: Standardizes how all entities track creation/modification
- **Maintainability**: Changes to common behavior only need one place
- **Interview Impact**: Shows understanding of inheritance and code reuse

### Current State
Each model has its own id and no audit tracking:
```python
@dataclass
class ParkingAttendant:
    id: str
    name: str
    email: str

@dataclass
class Vehicle:
    license_plate: str
    vehicle_type: VehicleType
```

### Improved Implementation

**Create `src/models/base_model.py`:**
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class BaseModel:
    """Base class for all entities in the system"""
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def soft_delete(self):
        """Soft delete instead of hard delete"""
        self.is_active = False
        self.updated_at = datetime.now()

    def touch(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now()
```

**Updated Models:**
```python
from .base_model import BaseModel
from dataclasses import dataclass

@dataclass
class ParkingAttendant(BaseModel):
    name: str = ""
    email: str = ""

@dataclass
class Vehicle(BaseModel):
    license_plate: str = ""
    vehicle_type: VehicleType = None
```

**Benefits in Interview:**
- Shows you think about common patterns
- Easy to extend with audit fields (created_by, updated_by)
- Demonstrates knowledge of soft deletes
- Quick to implement (2-3 minutes)

---

## 2. DTOs (Data Transfer Objects) / Serializers

### Why?
- **Separation of Concerns**: API layer separate from domain models
- **Security**: Don't expose internal model structure
- **Flexibility**: API can change without affecting domain
- **Validation**: Centralized request validation
- **Interview Impact**: Shows understanding of layered architecture

### Implementation

**Create `src/dtos/ticket_dto.py`:**
```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class IssueTicketRequest:
    """Request DTO for issuing a ticket"""
    license_plate: str
    vehicle_type: str  # String from API, will be converted to enum
    entry_gate_id: str

    def validate(self) -> list[str]:
        """Returns list of validation errors"""
        errors = []

        if not self.license_plate or len(self.license_plate) < 5:
            errors.append("license_plate must be at least 5 characters")

        if not self.vehicle_type:
            errors.append("vehicle_type is required")

        if not self.entry_gate_id:
            errors.append("entry_gate_id is required")

        return errors


@dataclass
class ParkingSpotDTO:
    """Nested DTO for parking spot in response"""
    spot_id: str
    spot_number: int
    spot_type: str
    floor_id: Optional[str] = None


@dataclass
class VehicleDTO:
    """Nested DTO for vehicle in response"""
    license_plate: str
    vehicle_type: str


@dataclass
class IssueTicketResponse:
    """Response DTO for ticket issuance"""
    ticket_id: str
    entry_time: str  # ISO format
    parking_spot: ParkingSpotDTO
    vehicle: VehicleDTO
    message: str = "Ticket issued successfully"

    @staticmethod
    def from_ticket(ticket):
        """Factory method to create DTO from domain model"""
        return IssueTicketResponse(
            ticket_id=ticket.ticket_id,
            entry_time=ticket.entry_time.isoformat(),
            parking_spot=ParkingSpotDTO(
                spot_id=ticket.parking_spot.id,
                spot_number=ticket.parking_spot.spot_number,
                spot_type=ticket.parking_spot.spot_type.value,
                floor_id=ticket.parking_spot.floor_id
            ),
            vehicle=VehicleDTO(
                license_plate=ticket.vehicle.license_plate,
                vehicle_type=ticket.vehicle.vehicle_type.value
            )
        )
```

**Create `src/dtos/payment_dto.py`:**
```python
from dataclasses import dataclass
from typing import Optional


@dataclass
class ProcessPaymentRequest:
    """Request DTO for payment processing"""
    ticket_id: str
    payment_type: str  # "UPI", "CARD", "CASH"
    amount: Optional[float] = None  # Optional, can be calculated

    def validate(self) -> list[str]:
        errors = []

        if not self.ticket_id:
            errors.append("ticket_id is required")

        if not self.payment_type:
            errors.append("payment_type is required")

        if self.amount is not None and self.amount < 0:
            errors.append("amount cannot be negative")

        return errors


@dataclass
class PaymentResponse:
    """Response DTO for payment"""
    payment_id: str
    ticket_id: str
    amount: float
    payment_type: str
    status: str
    payment_time: str
    message: str = "Payment processed successfully"

    @staticmethod
    def from_payment(payment):
        return PaymentResponse(
            payment_id=payment.payment_id,
            ticket_id=payment.ticket_id,
            amount=payment.amount,
            payment_type=payment.payment_type.value,
            status=payment.status.value,
            payment_time=payment.payment_time.isoformat()
        )
```

**Create `src/dtos/common_dto.py`:**
```python
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ApiResponse:
    """Standard API response wrapper"""
    status: str  # "success" or "error"
    data: Optional[Any] = None
    error: Optional[dict] = None
    metadata: Optional[dict] = None

    @staticmethod
    def success(data: Any, metadata: dict = None):
        return ApiResponse(status="success", data=data, metadata=metadata)

    @staticmethod
    def error(code: str, message: str):
        return ApiResponse(
            status="error",
            error={"code": code, "message": message}
        )


@dataclass
class PaginationRequest:
    """DTO for pagination parameters"""
    page: int = 1
    page_size: int = 20

    def validate(self) -> list[str]:
        errors = []
        if self.page < 1:
            errors.append("page must be >= 1")
        if self.page_size < 1 or self.page_size > 100:
            errors.append("page_size must be between 1 and 100")
        return errors

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
```

**Updated Controller Using DTOs:**
```python
from ..dtos.ticket_dto import IssueTicketRequest, IssueTicketResponse
from ..dtos.common_dto import ApiResponse

class TicketController:
    def issue_ticket(self, request_data: dict) -> tuple[dict, int]:
        # Parse request into DTO
        request = IssueTicketRequest(
            license_plate=request_data.get('license_plate'),
            vehicle_type=request_data.get('vehicle_type'),
            entry_gate_id=request_data.get('entry_gate_id')
        )

        # Validate
        errors = request.validate()
        if errors:
            response = ApiResponse.error(
                code="VALIDATION_ERROR",
                message="; ".join(errors)
            )
            return response.__dict__, 400

        try:
            # Convert to enum and call service
            vehicle_type = VehicleType[request.vehicle_type.upper()]
            ticket = self.ticket_service.issue_ticket(
                license_plate=request.license_plate,
                vehicle_type=vehicle_type,
                entry_gate=self._get_gate(request.entry_gate_id)
            )

            # Convert to response DTO
            response_dto = IssueTicketResponse.from_ticket(ticket)
            response = ApiResponse.success(data=response_dto)

            return response.__dict__, 201

        except NoSpotAvailableException as e:
            response = ApiResponse.error("NO_SPOT_AVAILABLE", str(e))
            return response.__dict__, 404
```

**Benefits:**
- Clean separation between API and domain
- Easy to add validation rules
- Consistent response format
- Type-safe data transfer
- Time to implement: 5-7 minutes

---

## 3. Builder Pattern for Complex Objects

### Why?
- **Readability**: Complex object creation is more readable
- **Flexibility**: Optional parameters handled elegantly
- **Immutability**: Can enforce immutable objects
- **Interview Impact**: Shows knowledge of creational patterns

### Implementation

**Create `src/builders/parking_lot_builder.py`:**
```python
from typing import List, Optional
from ..models import ParkingLot, ParkingFloor, ParkingSpot
from ..enums import SpotType


class ParkingLotBuilder:
    """Builder for creating ParkingLot with fluent interface"""

    def __init__(self):
        self._name: Optional[str] = None
        self._address: Optional[str] = None
        self._floors: List[ParkingFloor] = []

    def with_name(self, name: str) -> 'ParkingLotBuilder':
        self._name = name
        return self

    def with_address(self, address: str) -> 'ParkingLotBuilder':
        self._address = address
        return self

    def add_floor(self, floor: ParkingFloor) -> 'ParkingLotBuilder':
        self._floors.append(floor)
        return self

    def add_floor_with_spots(
        self,
        floor_number: int,
        small_spots: int = 0,
        medium_spots: int = 0,
        large_spots: int = 0
    ) -> 'ParkingLotBuilder':
        """Convenient method to add floor with spot configuration"""
        spots = []
        spot_counter = 1

        # Create small spots
        for i in range(small_spots):
            spots.append(ParkingSpot(
                id=f"F{floor_number}-S{spot_counter}",
                spot_number=spot_counter,
                spot_type=SpotType.SMALL,
                floor_id=f"FLOOR-{floor_number}"
            ))
            spot_counter += 1

        # Create medium spots
        for i in range(medium_spots):
            spots.append(ParkingSpot(
                id=f"F{floor_number}-M{spot_counter}",
                spot_number=spot_counter,
                spot_type=SpotType.MEDIUM,
                floor_id=f"FLOOR-{floor_number}"
            ))
            spot_counter += 1

        # Create large spots
        for i in range(large_spots):
            spots.append(ParkingSpot(
                id=f"F{floor_number}-L{spot_counter}",
                spot_number=spot_counter,
                spot_type=SpotType.LARGE,
                floor_id=f"FLOOR-{floor_number}"
            ))
            spot_counter += 1

        floor = ParkingFloor(
            floor_id=f"FLOOR-{floor_number}",
            floor_number=floor_number,
            spots=spots
        )
        self._floors.append(floor)
        return self

    def build(self) -> ParkingLot:
        if not self._name:
            raise ValueError("Parking lot name is required")

        return ParkingLot(
            name=self._name,
            address=self._address,
            floors=self._floors
        )


# Usage example:
parking_lot = (ParkingLotBuilder()
    .with_name("Central Mall Parking")
    .with_address("123 Main St")
    .add_floor_with_spots(floor_number=1, small_spots=20, medium_spots=15, large_spots=5)
    .add_floor_with_spots(floor_number=2, small_spots=25, medium_spots=20, large_spots=10)
    .build()
)
```

**Benefits:**
- Fluent, readable API
- Encapsulates complex creation logic
- Easy to extend with new options
- Time to implement: 3-4 minutes

---

## 4. Repository Interface (Dependency Inversion)

### Why?
- **SOLID Principles**: Dependency Inversion Principle
- **Testability**: Easy to mock repositories
- **Flexibility**: Swap implementations (in-memory, DB, cache)
- **Interview Impact**: Shows understanding of interfaces

### Implementation

**Create `src/repositories/base_repository.py`:**
```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional

T = TypeVar('T')


class IRepository(ABC, Generic[T]):
    """Base repository interface"""

    @abstractmethod
    def save(self, entity: T) -> T:
        """Save or update entity"""
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[T]:
        """Find entity by ID"""
        pass

    @abstractmethod
    def find_all(self) -> List[T]:
        """Get all entities"""
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        """Delete entity by ID"""
        pass

    @abstractmethod
    def exists(self, id: str) -> bool:
        """Check if entity exists"""
        pass
```

**Updated Repository:**
```python
from .base_repository import IRepository
from ..models import ParkingSpot

class ParkingSpotRepository(IRepository[ParkingSpot]):
    """Concrete implementation of parking spot repository"""

    def __init__(self):
        self._storage: dict[str, ParkingSpot] = {}

    def save(self, entity: ParkingSpot) -> ParkingSpot:
        self._storage[entity.id] = entity
        return entity

    def find_by_id(self, id: str) -> Optional[ParkingSpot]:
        return self._storage.get(id)

    def find_all(self) -> List[ParkingSpot]:
        return list(self._storage.values())

    def delete(self, id: str) -> bool:
        if id in self._storage:
            del self._storage[id]
            return True
        return False

    def exists(self, id: str) -> bool:
        return id in self._storage

    # Domain-specific methods
    def find_available(self) -> List[ParkingSpot]:
        return [spot for spot in self._storage.values() if spot.is_available()]
```

---

## 6. Request Validators

### Why?
- **Single Responsibility**: Validation logic separate from controllers
- **Reusability**: Same validators across different endpoints
- **Clarity**: Clear validation rules
- **Interview Impact**: Shows understanding of validation patterns

### Implementation

**Create `src/validators/ticket_validator.py`:**
```python
from typing import List
import re


class TicketValidator:
    """Validator for ticket-related operations"""

    @staticmethod
    def validate_license_plate(license_plate: str) -> List[str]:
        """Validate license plate format"""
        errors = []

        if not license_plate:
            errors.append("License plate is required")
            return errors

        if len(license_plate) < 5:
            errors.append("License plate must be at least 5 characters")

        if len(license_plate) > 15:
            errors.append("License plate must not exceed 15 characters")

        # Only alphanumeric and spaces
        if not re.match(r'^[A-Z0-9\s]+$', license_plate.upper()):
            errors.append("License plate can only contain letters, numbers, and spaces")

        return errors

    @staticmethod
    def validate_vehicle_type(vehicle_type: str) -> List[str]:
        """Validate vehicle type"""
        errors = []
        valid_types = ["BIKE", "CAR", "TRUCK", "BUS"]

        if not vehicle_type:
            errors.append("Vehicle type is required")
        elif vehicle_type.upper() not in valid_types:
            errors.append(f"Vehicle type must be one of: {', '.join(valid_types)}")

        return errors


class PaymentValidator:
    """Validator for payment operations"""

    @staticmethod
    def validate_amount(amount: float) -> List[str]:
        errors = []

        if amount is None:
            errors.append("Amount is required")
            return errors

        if amount < 0:
            errors.append("Amount cannot be negative")

        if amount == 0:
            errors.append("Amount must be greater than zero")

        if amount > 100000:  # Max amount check
            errors.append("Amount exceeds maximum limit of ₹100,000")

        return errors
```

---

## 6. Exception Hierarchy

### Why?
- **Clarity**: Specific exceptions for specific errors
- **Error Handling**: Easier to catch and handle specific cases
- **Debugging**: Better error messages
- **Interview Impact**: Shows understanding of exception design

### Implementation

**Create `src/exceptions/base_exception.py`:**
```python
class ParkingLotException(Exception):
    """Base exception for all parking lot errors"""

    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        super().__init__(self.message)


class ValidationException(ParkingLotException):
    """Raised when validation fails"""
    pass


class ResourceNotFoundException(ParkingLotException):
    """Raised when a resource is not found"""
    pass


class BusinessRuleViolationException(ParkingLotException):
    """Raised when a business rule is violated"""
    pass


# Specific exceptions
class NoSpotAvailableException(BusinessRuleViolationException):
    def __init__(self, vehicle_type: str = None):
        msg = f"No parking spot available for {vehicle_type}" if vehicle_type else "No parking spot available"
        super().__init__(msg, "NO_SPOT_AVAILABLE")


class TicketNotFoundException(ResourceNotFoundException):
    def __init__(self, ticket_id: str):
        super().__init__(f"Ticket not found: {ticket_id}", "TICKET_NOT_FOUND")


class InvalidPaymentException(BusinessRuleViolationException):
    def __init__(self, reason: str):
        super().__init__(f"Invalid payment: {reason}", "INVALID_PAYMENT")


class DuplicatePaymentException(BusinessRuleViolationException):
    def __init__(self, ticket_id: str):
        super().__init__(f"Payment already exists for ticket: {ticket_id}", "DUPLICATE_PAYMENT")
```

---


## Quick Win Checklist for Interviews

When time is limited, implement these in order:

### High Impact, Quick (< 3 minutes each)
1. ✅ **Base Model** - Shows inheritance understanding
2. ✅ **Response DTOs** - Shows API design knowledge

### Medium Impact (3-5 minutes each)
5. ✅ **Request DTOs with validation**
6. ✅ **Exception hierarchy**
7. ✅ **Builder pattern for complex objects**

### Nice to Have (5+ minutes)
8. ✅ **Service response objects**
9. ✅ **Separate validators**
10. ✅ **Complete value object library**

---

## Interview Tips

1. **Mention First, Implement Later**: "I would add DTOs here to separate API from domain, but let me implement the core logic first"

2. **Show Trade-offs**: "We could use a Builder pattern here for complex object creation, but for time constraints, constructor is fine"

3. **Talk While Coding**: "I'm creating a base model to avoid repeating id and timestamp fields"

4. **Ask Clarifying Questions**: "Should we support soft deletes? I can add that to the base model"

5. **Prioritize**: Focus on patterns that demonstrate:
   - SOLID principles
   - Clean architecture
   - Type safety
   - Error handling

---

## Summary

These improvements transform a basic parking lot system into an interview-winning design by demonstrating:
- **Design Patterns**: Builder, Repository, DTO
- **SOLID Principles**: SRP, DIP, OCP
- **Domain-Driven Design**: Value Objects, Entities
- **Clean Architecture**: Layered separation
- **Best Practices**: Validation, error handling, type safety

Each improvement is small (2-7 minutes) but shows deep understanding of software design principles.
