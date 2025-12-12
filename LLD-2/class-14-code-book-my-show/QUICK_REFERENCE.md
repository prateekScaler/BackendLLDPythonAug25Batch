# BookMyShow - Quick Reference Card

## 🚀 Setup Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate

# 3. Create admin user
python manage.py createsuperuser

# 4. Seed sample data
python manage.py seed_data

# 5. Start server
python manage.py runserver
```

## 📚 Learning Path

1. **Start Here**: `README.md` - Project overview
2. **Setup**: `SETUP_GUIDE.md` - Detailed setup instructions
3. **Study Order**:
   - `guides/01_MODELS_AND_RELATIONSHIPS.md` - Database design
   - `guides/02_SERIALIZERS.md` - API data handling
   - `guides/03_CONCURRENCY_CONTROL.md` - ⭐ **MOST IMPORTANT**
   - `guides/04_ARCHITECTURE_AND_DATA_FLOW.md` - System design
   - `guides/05_API_DOCUMENTATION.md` - API reference
   - `guides/06_INTERVIEW_GOTCHAS.md` - Interview prep

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `models.py` | Database schema (11 models) |
| `serializers.py` | JSON ↔ Python conversion |
| `views.py` | API endpoints (controllers) |
| `services/booking_service_*.py` | 3 concurrency implementations |
| `urls.py` | API routing |

## 🎯 Concurrency Implementations

### Switch Between Implementations

Edit `views.py` line 48:

```python
# Pessimistic Locking (default)
from .services.booking_service_pessimistic import BookingServicePessimistic
BookingService = BookingServicePessimistic

# OR Optimistic Locking
from .services.booking_service_optimistic import BookingServiceOptimistic
BookingService = BookingServiceOptimistic

# OR Thread Locking (educational only)
from .services.booking_service_thread import BookingServiceThread
BookingService = BookingServiceThread
```

### Comparison

| Feature | Pessimistic | Optimistic | Thread |
|---------|------------|------------|--------|
| **Lock Type** | Database | Version-based | Application |
| **Concurrency** | Low (blocking) | High | Low |
| **Distributed** | ✅ Yes | ✅ Yes | ❌ No |
| **Retry Needed** | ❌ No | ✅ Yes | ❌ No |
| **Production Ready** | ✅ Yes | ✅ Yes | ❌ No |

## 🔌 API Quick Test

```bash
# Health check
curl http://localhost:8000/api/health/

# List cities
curl http://localhost:8000/api/cities/

# List movies
curl http://localhost:8000/api/movies/

# Search movies in Mumbai
curl http://localhost:8000/api/movies/search/?city=mumbai

# Get show details
curl http://localhost:8000/api/shows/show-1/

# Book tickets (requires auth)
curl -X POST http://localhost:8000/api/book/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "show_id": "show-1",
    "seat_ids": ["showseat-1", "showseat-2"],
    "payment_mode": "UPI"
  }'
```

## 📊 Database Relationships

```
City → Theater → Screen → Seat (1:N at each level)
                  ↓        ↓
                Show ← ────┘
                  ↓
             ShowSeat (instance with price/status)
                  ↓
             TicketSeat
                  ↓
              Ticket → Payment (1:1)
                  ↓
                User
```

## 🎓 Interview Topics Covered

### Must Know:
- ✅ Race conditions and concurrency
- ✅ Pessimistic vs Optimistic locking
- ✅ Database transactions (ACID)
- ✅ Django ORM relationships
- ✅ Service layer architecture
- ✅ REST API design

### Deep Dive:
- ✅ N+1 query problem
- ✅ SELECT FOR UPDATE
- ✅ Version-based conflict detection
- ✅ Dynamic pricing system
- ✅ Scalability considerations

## 🔍 Code Walkthrough Order

1. **Models** (`models.py`)
   - Start with `City` → `Theater` → `Screen` → `Seat`
   - Then `Movie` → `Show` → `ShowSeat`
   - Finally `Ticket` → `Payment`

2. **Serializers** (`serializers.py`)
   - Simple: `CitySerializer`
   - Nested: `TheaterSerializer`
   - Validation: `BookingRequestSerializer`

3. **Services** (`services/`)
   - `booking_service_pessimistic.py` - Read line by line
   - Compare with `booking_service_optimistic.py`
   - Understand difference

4. **Views** (`views.py`)
   - `book_tickets()` function - Most important!
   - Follow data flow: Request → Serializer → Service → Response

## 💡 Quick Tips

### Performance Optimization
```python
# Bad: N+1 queries
theaters = Theater.objects.all()
for t in theaters:
    print(t.city.name)  # Query per theater!

# Good: Join
theaters = Theater.objects.select_related('city').all()
for t in theaters:
    print(t.city.name)  # No extra queries
```

### Concurrency Testing
```python
import threading

def book_same_seat():
    # 10 threads booking same seat
    threads = [threading.Thread(target=book_seat) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    # Only 1 should succeed
```

### Transaction Management
```python
from django.db import transaction

@transaction.atomic
def book_tickets():
    # All or nothing
    create_ticket()
    create_payment()
    # If payment fails, ticket is rolled back
```

## 📖 Sample Data Created by seed_data

- **3 Cities**: Mumbai, Delhi, Bangalore
- **3 Theaters**: PVR Juhu, INOX R-City, PVR Saket
- **9 Screens**: 3 per theater (Audi 1, 2, 3)
- **225 Seats**: 25 per screen (10 Gold, 10 Platinum, 5 Diamond)
- **4 Movies**: Avengers, Inception, Dark Knight, Interstellar
- **18 Shows**: 2 shows per screen, tomorrow at 2 PM and 6:30 PM
- **4,500 ShowSeats**: 225 seats × 18 shows

## 🎯 Interview Scenarios

### Scenario 1: Race Condition
**Q**: Two users book same seat simultaneously. What happens?

**A**: Depends on implementation:
- **Pessimistic**: Second waits, then fails
- **Optimistic**: Both read, one succeeds, one retries
- **Thread**: Works only on single server

### Scenario 2: Scalability
**Q**: System has 1M concurrent users. How to scale?

**A**:
- Database: Read replicas, partitioning by city
- Cache: Redis for listings (not for booking!)
- App: Horizontal scaling with load balancer
- Locks: Redis Redlock for distributed locking

### Scenario 3: Pricing
**Q**: Seat prices vary. How to design?

**A**:
- Seat: Template (permanent)
- ShowSeat: Instance (dynamic price)
- PricingRule: Configuration (multipliers)
- Calculate when show is created

## ⚠️ Common Mistakes

1. ❌ Price in Seat table (should be in ShowSeat)
2. ❌ No transaction for booking (use @transaction.atomic)
3. ❌ Thread locks for production (use DB locks)
4. ❌ No validation of cutoff time
5. ❌ N+1 queries (use select_related/prefetch_related)

## 🎓 Study Checklist

- [ ] Understand all model relationships
- [ ] Explain pessimistic vs optimistic locking
- [ ] Can write a booking service from scratch
- [ ] Know when to use each locking strategy
- [ ] Understand transaction management
- [ ] Can optimize database queries
- [ ] Explain the full booking flow
- [ ] Ready to discuss scalability
- [ ] Practiced explaining design decisions
- [ ] Completed coding the project end-to-end

## 📝 Final Exam Questions

Try to answer without looking:

1. What's the difference between Seat and ShowSeat?
2. How to prevent double booking?
3. When to use pessimistic vs optimistic locking?
4. Explain the booking flow from API to database.
5. How would you scale to 1M users?

**Answers in**: `guides/06_INTERVIEW_GOTCHAS.md`

---

**Remember**: Understanding > Memorization!

Good luck with your interviews! 🚀
