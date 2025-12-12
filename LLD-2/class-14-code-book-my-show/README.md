# BookMyShow - Low Level Design Project

A comprehensive Django REST API implementation of a movie ticket booking system, designed for teaching LLD interview concepts with focus on concurrency control.

## 🎯 Learning Objectives

This project teaches:

1. **Django ORM & Relationships** - ForeignKey, OneToOne, ManyToMany with through models
2. **REST API Design** - ViewSets, Serializers, proper HTTP methods
3. **Concurrency Control** - Pessimistic locking, Optimistic locking, Thread locks
4. **Service Layer Architecture** - Separation of concerns, business logic organization
5. **Transaction Management** - ACID properties, atomic operations
6. **Performance Optimization** - Query optimization, indexes, select_related/prefetch_related
7. **Interview Preparation** - Common questions, gotchas, best practices

## 📋 Requirements Met

### Functional Requirements

- ✅ Support for multiple cities
- ✅ Multiple cinemas per city
- ✅ Multiple screens per cinema
- ✅ Different seat types (GOLD, DIAMOND, PLATINUM)
- ✅ Movie search and filtering (location, cinema, language, rating, category)
- ✅ Multiple show slots per movie
- ✅ Multiple payment methods (UPI, Credit Card, Netbanking)
- ✅ Coupon/promo code support
- ✅ Seat availability display
- ✅ Dynamic pricing (seat type, day, time, movie, cinema)
- ✅ Booking cancellation with cutoff time (1 hour before show)

### Technical Requirements

- ✅ Django REST Framework
- ✅ SQLite database (simple, educational)
- ✅ Three concurrency control implementations
- ✅ Controller-Service-Model architecture
- ✅ Comprehensive documentation

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT (HTTP/JSON)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   VIEW LAYER (Controller)                    │
│   • HTTP request/response handling                           │
│   • Authentication/Authorization                             │
│   • Data validation via serializers                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   SERIALIZER LAYER (DTO)                     │
│   • JSON ↔ Python object conversion                         │
│   • Input validation                                         │
│   • Response formatting                                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   SERVICE LAYER (Business Logic)             │
│   • booking_service_pessimistic.py  (DB locks)              │
│   • booking_service_optimistic.py   (version-based)         │
│   • booking_service_thread.py       (thread locks)          │
│   • movie_service.py                                         │
│   • pricing_service.py                                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   MODEL LAYER (ORM)                          │
│   • Database schema definition                               │
│   • Relationships                                            │
│   • Model-level validation                                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   DATABASE (SQLite)                          │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
bookmyshow/
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── bookmyshow/                     # Project settings
│   ├── settings.py                 # Django configuration
│   ├── urls.py                     # Root URL routing
│   └── wsgi.py                     # WSGI application
│
├── bookmyshow/booking/             # Main app
│   ├── models.py                   # Database models (11 models)
│   ├── serializers.py              # REST serializers
│   ├── views.py                    # API views/controllers
│   ├── urls.py                     # App URL routing
│   ├── admin.py                    # Django admin configuration
│   │
│   └── services/                   # Service layer
│       ├── base_service.py
│       ├── booking_service_pessimistic.py    # DB-level locks
│       ├── booking_service_optimistic.py     # Version-based
│       ├── booking_service_thread.py         # Thread locks
│       ├── movie_service.py
│       └── pricing_service.py
│
└── bookmyshow/guides/              # Educational documentation
    ├── 01_MODELS_AND_RELATIONSHIPS.md
    ├── 02_SERIALIZERS.md
    ├── 03_CONCURRENCY_CONTROL.md         # ⭐ Most important!
    ├── 04_ARCHITECTURE_AND_DATA_FLOW.md
    ├── 05_API_DOCUMENTATION.md
    └── 06_INTERVIEW_GOTCHAS.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**

```bash
cd /path/to/class-14-code-book-my-show
```

2. **Create virtual environment** (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser** (for admin access)

```bash
python manage.py createsuperuser
```

6. **Populate database with sample data** (optional but recommended)

```bash
python manage.py seed_data
```

This creates sample cities, theaters, screens, seats, movies, and shows.

7. **Run development server**

```bash
python manage.py runserver
```

8. **Access the application**

- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- Health Check: http://localhost:8000/api/health/

## 📊 Database Models

### Core Entities

1. **City** - Cities where service is available
2. **Theater** - Cinema halls in a city
3. **Screen** - Screens within a theater
4. **Seat** - Seat configuration (template)
5. **Movie** - Movies available for booking
6. **Show** - Movie screening at specific time/screen
7. **ShowSeat** - Seat instance for a specific show (with price, status)
8. **User** - Extended Django user model
9. **Ticket** - Booking record
10. **TicketSeat** - Through model for ticket-seat relationship
11. **Payment** - Payment transaction
12. **PricingRule** - Dynamic pricing configuration
13. **Coupon** - Discount coupons

### Key Relationships

```
City (1) → (N) Theater (1) → (N) Screen (1) → (N) Seat
                │                      │
                └─────(N) Show (N)─────┘
                          │
                     (1) ShowSeat (N)
                          │
                    (N) TicketSeat (N)
                          │
                      (1) Ticket (1) → (1) Payment
                          │
                        (N) User
```

## 🔐 Concurrency Control (The Heart of This Project!)

This project implements **THREE** different concurrency control mechanisms:

### 1. Pessimistic Locking (Recommended for Production)

**File**: `services/booking_service_pessimistic.py`

```python
# Acquires database row-level lock
@transaction.atomic
def book_tickets(...):
    seats = ShowSeat.objects.select_for_update().filter(...)
    # Other transactions wait here
    # Guaranteed consistency
```

**When to use**: High contention, critical operations

### 2. Optimistic Locking (Better Concurrency)

**File**: `services/booking_service_optimistic.py`

```python
# Version-based conflict detection
def book_tickets(...):
    seat = ShowSeat.objects.get(id=seat_id)
    old_version = seat.version

    updated = ShowSeat.objects.filter(
        id=seat_id,
        version=old_version  # Check version
    ).update(
        status='BOOKED',
        version=F('version') + 1  # Increment
    )

    if updated == 0:
        # Conflict! Retry
```

**When to use**: Low contention, high throughput needed

### 3. Thread-based Locking (Educational Only)

**File**: `services/booking_service_thread.py`

```python
# Application-level lock
lock = threading.Lock()
with lock:
    # Only one thread at a time
```

**When to use**: Single server, educational purposes, **NOT for production**

### Switching Between Implementations

In `views.py`:

```python
# Choose implementation here:
from .services.booking_service_pessimistic import BookingServicePessimistic
BookingService = BookingServicePessimistic

# Or use:
# from .services.booking_service_optimistic import BookingServiceOptimistic
# BookingService = BookingServiceOptimistic
```

## 🎓 Educational Guides

Each guide is designed for interview preparation:

| Guide | Purpose | Interview Focus |
|-------|---------|----------------|
| **01_MODELS_AND_RELATIONSHIPS.md** | Django ORM, relationships | Database design, N+1 queries |
| **02_SERIALIZERS.md** | DRF serializers, validation | Data transformation, validation |
| **03_CONCURRENCY_CONTROL.md** | ⭐ Locking mechanisms | Race conditions, transactions |
| **04_ARCHITECTURE_AND_DATA_FLOW.md** | System architecture | MVC, layer separation |
| **05_API_DOCUMENTATION.md** | API endpoints | RESTful design |
| **06_INTERVIEW_GOTCHAS.md** | Common mistakes, best practices | Interview preparation |

## 🔑 Key API Endpoints

### User Flow

```
1. Register      → POST   /api/register/
2. Login         → POST   /api/auth/login/
3. Search Movies → GET    /api/movies/search/?city=mumbai&query=avengers
4. View Shows    → GET    /api/movies/{id}/shows/?city=mumbai
5. View Seats    → GET    /api/shows/{id}/
6. Book Tickets  → POST   /api/book/
7. Confirm Pay   → POST   /api/tickets/{id}/confirm-payment/
8. View Tickets  → GET    /api/tickets/
9. Cancel        → POST   /api/tickets/{id}/cancel/
```

### Admin Operations (via Django Admin)

- Add cities, theaters, screens, seats
- Add movies and shows
- Create pricing rules
- Manage coupons

## 🎯 Interview Practice Scenarios

### Scenario 1: Explain the double booking problem

**Question**: How do you prevent two users from booking the same seat?

**Answer**: See `guides/03_CONCURRENCY_CONTROL.md`
- Explain race condition
- Demonstrate with timing diagram
- Show pessimistic vs optimistic solutions
- Discuss trade-offs

### Scenario 2: Design seat pricing

**Question**: Seat prices vary by multiple factors. How do you design this?

**Answer**: See `PricingRule` model and `pricing_service.py`
- Base price + multipliers
- Configurable rules
- Applied during ShowSeat creation

### Scenario 3: Scale to millions of users

**Question**: How would you scale this system?

**Answer**: See `guides/06_INTERVIEW_GOTCHAS.md`
- Database partitioning
- Caching strategy
- Distributed locks
- Microservices

## 🧪 Testing Concurrency

```python
import threading

def test_concurrent_booking():
    """Test that only one user can book a seat"""
    def book():
        try:
            booking_service.book_tickets(
                user=user,
                show_id='show-1',
                seat_ids=['seat-a1'],
                payment_mode='UPI'
            )
        except:
            pass  # Expected for all but one

    # 10 threads trying to book same seat
    threads = [threading.Thread(target=book) for _ in range(10)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    # Verify: Only 1 booking succeeded
    seat = ShowSeat.objects.get(id='seat-a1')
    assert seat.status == 'BOOKED'
    assert Ticket.objects.filter(ticket_seats__show_seat=seat).count() == 1
```

## 🤔 Common Interview Questions Covered

1. ✅ How to prevent double booking? (Concurrency)
2. ✅ Database schema for BookMyShow (Models)
3. ✅ Dynamic pricing design (PricingRule)
4. ✅ API design for booking flow (REST APIs)
5. ✅ How to scale the system? (Scalability)
6. ✅ N+1 query problem (Performance)
7. ✅ Transaction management (ACID)
8. ✅ Pessimistic vs Optimistic locking (Concurrency)

## 🎓 Interview Tips

### DO:
- ✅ Explain your thought process
- ✅ Ask clarifying questions
- ✅ Discuss trade-offs
- ✅ Start simple, then optimize
- ✅ Draw diagrams
- ✅ Write clean code

### DON'T:
- ❌ Jump to code immediately
- ❌ Ignore edge cases
- ❌ Say "I'll use a flag" for concurrency
- ❌ Forget about scalability
- ❌ Write code without explaining

## 🔗 Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- DRF Documentation: https://www.django-rest-framework.org/
- Database Transactions: https://docs.djangoproject.com/en/stable/topics/db/transactions/
- Optimistic Locking: https://en.wikipedia.org/wiki/Optimistic_concurrency_control
- Pessimistic Locking: https://en.wikipedia.org/wiki/Lock_(database)

## 🤝 Contributing

This is an educational project. Feel free to:
- Add more test cases
- Improve documentation
- Add new features
- Fix bugs


## 👨‍🏫 Author

Created for LLD interview preparation - Backend LLD Python Aug 25 Batch

---

## 🎯 Next Steps

1. **Setup the project** (see Quick Start)
2. **Read the guides** (start with guides/01_...)
3. **Explore the code** (models → serializers → services → views)
4. **Test the APIs** (use Postman or curl)
5. **Understand concurrency** (⭐ Most important for interviews!)
6. **Practice explaining** (as if in an interview)

**Remember**: The goal is not to memorize code, but to understand **concepts** and **trade-offs**!

Good luck with your LLD interviews! 🚀
