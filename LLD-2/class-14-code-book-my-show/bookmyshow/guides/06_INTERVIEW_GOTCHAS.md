# LLD Interview Gotchas and Best Practices

## Table of Contents
1. [Common Interview Questions](#common-interview-questions)
2. [Design Discussion Points](#design-discussion-points)
3. [Common Mistakes](#common-mistakes)
4. [Performance Optimization](#performance-optimization)
5. [Scalability Considerations](#scalability-considerations)
6. [Code Quality](#code-quality)

---

## Common Interview Questions

### Q1: How do you handle concurrent bookings for the same seat?

**Bad Answer**: "I'll check if seat is available, then book it."

**Good Answer**:
```
I would use database-level concurrency control:

For HIGH contention (popular movies):
- Pessimistic locking with SELECT FOR UPDATE
- Guarantees consistency
- One transaction at a time

For LOW contention (regular shows):
- Optimistic locking with version field
- Higher throughput
- Retry on conflict

Code example:
@transaction.atomic
def book_seat():
    seat = ShowSeat.objects.select_for_update().get(id=5)
    if seat.status == 'AVAILABLE':
        seat.status = 'BOOKED'
        seat.save()
```

**Why Good**: Shows understanding of concurrency, trade-offs, and provides implementation.

---

### Q2: How do you design the seat pricing system?

**Bad Answer**: "Store price in Seat table."

**Good Answer**:
```
Seat pricing depends on multiple factors:
1. Seat type (Gold/Diamond/Platinum)
2. Day of week (weekend surge)
3. Time of day (prime time)
4. Movie (blockbusters cost more)
5. Theater location

Design:
- Seat: Master data (permanent seat info)
- ShowSeat: Instance data (price for specific show)
- PricingRule: Configuration (multipliers & rules)

When show is created:
for each seat in screen:
    base_price = get_base_price(seat.type)
    price = apply_pricing_rules(
        base_price,
        show.time,
        show.movie,
        show.theater
    )
    create ShowSeat with calculated price
```

**Why Good**: Demonstrates flexible design, business understanding, and extensibility.

---

### Q3: Database schema for BookMyShow - explain key relationships.

**Bad Answer**: Lists all tables without explaining relationships.

**Good Answer**:
```
Key relationships:

1. City → Theater → Screen → Seat
   (Hierarchical: 1:N at each level)
   Why: Geographical and physical organization

2. Movie → Show ← Screen
   (Show links movie to screen at specific time)
   Why: Same movie can play in multiple screens

3. Show ↔ Seat (M:N via ShowSeat)
   Why: Need per-show seat price and status
   ShowSeat = Instance, Seat = Template

4. Ticket ↔ ShowSeat (M:N via TicketSeat)
   Why: One ticket can have multiple seats

5. Ticket → Payment (1:1)
   Why: One payment per booking

Critical decision: Separate Seat and ShowSeat
- Seat: Permanent (A1, Gold type)
- ShowSeat: Per-show (price, availability)
- Allows dynamic pricing & concurrent booking control
```

**Why Good**: Explains rationale, not just structure.

---

### Q4: How to prevent double booking?

**Bad Answer**: "Check if available before booking."

**Good Answer**:
```
Double booking is a race condition:
Time | User A         | User B
-----|----------------|----------------
T1   | Check: OK      |
T2   |                | Check: OK
T3   | Book           | Book (ERROR!)

Solutions:

1. Pessimistic Locking:
   seat = ShowSeat.objects.select_for_update().get(id=5)
   // Row is locked, User B waits
   if seat.status == 'AVAILABLE':
       seat.status = 'BOOKED'

2. Optimistic Locking:
   updated = ShowSeat.objects.filter(
       id=5,
       version=old_version,
       status='AVAILABLE'
   ).update(
       status='BOOKED',
       version=F('version') + 1
   )
   if updated == 0:
       raise ConflictError()

3. Unique Constraint:
   unique_together = ['show', 'seat']
   Database ensures no duplicates

Preferred: #1 for final booking (guaranteed),
           #2 for seat selection (better UX)
```

**Why Good**: Identifies the problem, provides multiple solutions with trade-offs.

---

### Q5: How would you scale this system to millions of users?

**Bad Answer**: "Use more servers."

**Good Answer**:
```
Scaling strategy:

1. Database Layer:
   - Read replicas for searches/listings
   - Write master for bookings
   - Partition by city (Mumbai DB, Delhi DB)
   - Index on frequently queried fields

2. Application Layer:
   - Horizontal scaling (multiple servers)
   - Load balancer (distribute requests)
   - Stateless services (no session on server)

3. Caching:
   - Redis for:
     * Movie listings (TTL: 1 hour)
     * Show schedules (TTL: 15 min)
     * Available seat count (TTL: 30 sec)
   - Never cache seat availability (must be real-time)

4. Async Processing:
   - Email notifications: Message queue (Celery)
   - Payment processing: Async with webhooks
   - Seat lock cleanup: Background job

5. CDN:
   - Movie posters, static assets

6. Distributed Locking:
   - Redis Redlock for seat booking
   - Replace SELECT FOR UPDATE in distributed setup

Architecture:
[Load Balancer] → [App Servers] → [Redis Cache]
                                 ↘ [Read DB Replicas]
                                 ↘ [Write DB Master]
```

**Why Good**: Comprehensive, specific technologies, considers different aspects.

---

## Design Discussion Points

### 1. Why separate Seat and ShowSeat?

**Interviewer probes**: "Can't we just use Seat table?"

**Answer**:
```
Separation is crucial for:

1. Dynamic Pricing:
   - Same seat, different prices for different shows
   - Friday night > Monday afternoon
   - Blockbuster > Regular movie

2. Concurrency Control:
   - Lock ShowSeat for specific show, not seat
   - Different shows on same screen can book simultaneously

3. Historical Data:
   - ShowSeat tracks which shows had seat booked
   - Seat is just configuration

Example:
Seat: A1, Gold (permanent)
ShowSeat1: A1, $300, Show: Avengers, Status: Booked
ShowSeat2: A1, $200, Show: Regular Movie, Status: Available

Without separation, how do you:
- Have different prices for same seat?
- Track booking status per show?
- Lock for concurrent bookings?
```

---

### 2. Why service layer? Can't models/views handle it?

**Answer**:
```
Service layer provides:

1. Separation of Concerns:
   - Views: HTTP concerns (request/response)
   - Models: Data structure (schema, relationships)
   - Services: Business logic (what, not how)

2. Reusability:
   - REST API uses service
   - GraphQL API uses same service
   - CLI tool uses same service
   - Background jobs use same service

3. Testability:
   - Test services without HTTP layer
   - Mock dependencies easily
   - Unit tests independent of Django

4. Transaction Management:
   - Complex multi-model operations
   - Atomic transactions
   - Rollback on failure

Example:
# Bad: Business logic in view
def book_tickets(request):
    seat = ShowSeat.objects.get(...)
    if seat.status == 'AVAILABLE':
        seat.status = 'BOOKED'
        seat.save()
        ticket = Ticket.objects.create(...)
        payment = Payment.objects.create(...)
    return Response(...)

# Good: Business logic in service
def book_tickets(request):
    result = BookingService().book_tickets(...)
    return Response(result)
```

---

## Common Mistakes

### Mistake 1: Storing price in Seat table

```python
# Bad
class Seat(models.Model):
    number = models.CharField(max_length=10)
    price = models.DecimalField(...)  # ❌ Static price

# Problem: How to have different prices for different shows?
```

**Fix**: Price in ShowSeat (per show instance).

---

### Mistake 2: Not using transactions

```python
# Bad
def book_tickets():
    ticket = Ticket.objects.create(...)
    payment = Payment.objects.create(...)
    # What if payment creation fails? Orphaned ticket!

# Good
@transaction.atomic
def book_tickets():
    ticket = Ticket.objects.create(...)
    payment = Payment.objects.create(...)
    # If payment fails, ticket creation is rolled back
```

---

### Mistake 3: N+1 Query Problem

```python
# Bad
theaters = Theater.objects.all()
for theater in theaters:
    print(theater.city.name)  # Query for each theater!

# Good
theaters = Theater.objects.select_related('city').all()
for theater in theaters:
    print(theater.city.name)  # No extra queries
```

---

### Mistake 4: Using thread locks for distributed system

```python
# Bad (only works on single server)
lock = threading.Lock()
with lock:
    book_seat()

# Good (works across servers)
seat = ShowSeat.objects.select_for_update().get(id=5)
```

---

### Mistake 5: Not validating business rules

```python
# Bad
def cancel_ticket(ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.status = 'CANCELLED'
    ticket.save()
    # No check for cutoff time!

# Good
def cancel_ticket(ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if not ticket.can_cancel():
        raise ValueError("Cannot cancel after cutoff time")
    ticket.status = 'CANCELLED'
    ticket.save()
```

---

## Performance Optimization

### 1. Database Indexes

```python
class ShowSeat(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, db_index=True)  # ✓

    class Meta:
        indexes = [
            models.Index(fields=['show', 'status']),  # Composite index
        ]

# Query that benefits:
ShowSeat.objects.filter(show=show, status='AVAILABLE')
# Uses composite index: fast!
```

### 2. Query Optimization

```python
# Bad: Separate queries
movies = Movie.objects.all()
for movie in movies:
    print(movie.show_set.count())  # N queries

# Good: Annotation
movies = Movie.objects.annotate(
    show_count=Count('shows')
)
for movie in movies:
    print(movie.show_count)  # No extra queries
```

### 3. Pagination

```python
# Bad: Return all results
movies = Movie.objects.all()  # Could be 10,000 movies!

# Good: Paginate
from rest_framework.pagination import PageNumberPagination

class MovieViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    # Returns 10-20 at a time
```

### 4. Caching

```python
from django.core.cache import cache

def get_available_seats(show_id):
    cache_key = f'seats:{show_id}'

    seats = cache.get(cache_key)
    if seats is None:
        seats = ShowSeat.objects.filter(
            show_id=show_id,
            status='AVAILABLE'
        )
        cache.set(cache_key, seats, timeout=30)  # 30 seconds

    return seats
```

---

## Scalability Considerations

### 1. Database Partitioning

```
# Partition by city
Mumbai users → Mumbai database
Delhi users → Delhi database

# Partition by date
Recent shows → Fast SSD database
Old shows → Archival database
```

### 2. Microservices

```
User Service: Authentication, profiles
Movie Service: Movie data, search
Booking Service: Seat booking, payments
Notification Service: Emails, SMS

Each service has its own database
Communicate via REST/gRPC/Message Queue
```

### 3. Eventual Consistency

```
# Seat availability count can be eventually consistent
# (cached with 30-second TTL)

# But booking must be strongly consistent
# (real-time check with locks)

Trade-off: Better performance for reads,
          Strict consistency for writes
```

---

## Code Quality

### 1. Follow PEP 8

```python
# Bad
def BookTickets(ShowId,SeatId):
    pass

# Good
def book_tickets(show_id, seat_id):
    pass
```

### 2. Meaningful Names

```python
# Bad
s = ShowSeat.objects.get(id=i)

# Good
show_seat = ShowSeat.objects.get(id=seat_id)
```

### 3. DRY (Don't Repeat Yourself)

```python
# Bad
seat1 = ShowSeat.objects.get(id=1)
if seat1.status != 'AVAILABLE':
    raise ValueError("Not available")

seat2 = ShowSeat.objects.get(id=2)
if seat2.status != 'AVAILABLE':
    raise ValueError("Not available")

# Good
def validate_seat_availability(seat_id):
    seat = ShowSeat.objects.get(id=seat_id)
    if seat.status != 'AVAILABLE':
        raise ValueError("Not available")
    return seat

seat1 = validate_seat_availability(1)
seat2 = validate_seat_availability(2)
```

### 4. Error Handling

```python
# Bad
def book_tickets(show_id, seat_ids):
    seats = ShowSeat.objects.filter(id__in=seat_ids)
    # What if seats don't exist?

# Good
def book_tickets(show_id, seat_ids):
    seats = ShowSeat.objects.filter(id__in=seat_ids)

    if seats.count() != len(seat_ids):
        raise ValueError("Some seats not found")

    # Continue with booking
```

---

## Interview Red Flags (Don't Do This!)

### ❌ 1. "I'll just add a flag"

```python
# Bad solution for concurrency
class ShowSeat(models.Model):
    is_being_booked = models.BooleanField(default=False)

# Problem: Still has race condition between check and set!
```

**Better**: Use proper locking mechanisms.

---

### ❌ 2. "I'll use sleep() to avoid conflicts"

```python
# Bad
if seat.status == 'AVAILABLE':
    time.sleep(0.1)  # Hope no one else books?
    seat.status = 'BOOKED'
```

**Better**: Use database locks.

---

### ❌ 3. "I don't need indexes, database is fast"

Shows lack of understanding of performance at scale.

---

### ❌ 4. "I'll handle concurrency in frontend"

Backend must ALWAYS validate. Never trust client.

---

## Summary: Interview Checklist

### System Design
- [ ] Understand requirements
- [ ] Identify entities and relationships
- [ ] Explain design decisions
- [ ] Discuss trade-offs

### Concurrency
- [ ] Identify race conditions
- [ ] Explain locking strategies
- [ ] Know pessimistic vs optimistic
- [ ] Understand distributed vs single-server

### Scalability
- [ ] Database optimization (indexes, queries)
- [ ] Caching strategy
- [ ] Horizontal scaling
- [ ] Partitioning/Sharding

### Code Quality
- [ ] Clean, readable code
- [ ] Proper error handling
- [ ] Following conventions (PEP 8)
- [ ] Comments for complex logic

### Communication
- [ ] Think aloud
- [ ] Ask clarifying questions
- [ ] Explain trade-offs
- [ ] Be open to feedback

---

## Final Tips

1. **Start Simple**: Basic solution first, then optimize.
2. **Ask Questions**: Clarify requirements before coding.
3. **Think Aloud**: Explain your thought process.
4. **Consider Edge Cases**: Empty data, invalid input, concurrency.
5. **Know Trade-offs**: No perfect solution, explain choices.
6. **Practice**: Build projects, not just read about them.

**Remember**: Interviews test problem-solving, not memorization. Understand concepts, don't just memorize code!

---

Good luck with your interviews! 🚀
