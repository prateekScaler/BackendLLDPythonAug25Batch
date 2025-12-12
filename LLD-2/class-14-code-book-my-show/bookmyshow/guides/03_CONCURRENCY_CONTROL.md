# Concurrency Control Guide for LLD Interviews

## Table of Contents
1. [The Concurrency Problem](#the-concurrency-problem)
2. [Locking Strategies](#locking-strategies)
3. [Pessimistic Locking](#pessimistic-locking-database-locks)
4. [Optimistic Locking](#optimistic-locking-version-based)
5. [Thread-based Locking](#thread-based-locking)
6. [Comparison and When to Use](#comparison-and-when-to-use)
7. [Real-world Scenarios](#real-world-scenarios)
8. [Interview Questions](#interview-questions)

---

## The Concurrency Problem

### Scenario: Double Booking

**Problem**: Two users try to book the same seat simultaneously.

```
Time  | User A                          | User B
------|---------------------------------|----------------------------------
T1    | Check seat 5A: AVAILABLE ✓      |
T2    |                                 | Check seat 5A: AVAILABLE ✓
T3    | Book seat 5A                    |
T4    |                                 | Book seat 5A
------|---------------------------------|----------------------------------
Result: BOTH USERS BOOKED SAME SEAT! ❌
```

### Why Does This Happen?

**Race Condition**: Outcome depends on timing/sequence of events.

```python
# User A's request
seat = ShowSeat.objects.get(id=5)  # T1: status = AVAILABLE
if seat.status == 'AVAILABLE':     # T1: Check passes
    seat.status = 'BOOKED'          # T3: Book
    seat.save()

# User B's request (running concurrently)
seat = ShowSeat.objects.get(id=5)  # T2: status = AVAILABLE (stale!)
if seat.status == 'AVAILABLE':     # T2: Check passes
    seat.status = 'BOOKED'          # T4: Book (DOUBLE BOOKING!)
    seat.save()
```

### Interview Question: *Why is this a problem?*

**Critical Section**: Code that accesses shared resources (database rows).
- Multiple threads/processes can execute simultaneously
- Database reads are NOT atomic with writes
- Need to ensure **mutual exclusion**

---

## Locking Strategies

### Overview

```
┌────────────────────────────────────────────────────┐
│           Concurrency Control Strategies            │
├────────────────────────────────────────────────────┤
│                                                      │
│  1. Pessimistic Locking (Database Locks)            │
│     - Lock rows during read                          │
│     - Others wait                                    │
│     - High consistency, low concurrency              │
│                                                      │
│  2. Optimistic Locking (Version-based)              │
│     - No locks on read                               │
│     - Check version on write                         │
│     - High concurrency, requires retry               │
│                                                      │
│  3. Application Locks (Thread/Process locks)        │
│     - Python threading.Lock                          │
│     - Only works in single process                   │
│     - NOT for distributed systems                    │
│                                                      │
└────────────────────────────────────────────────────┘
```

---

## Pessimistic Locking (Database Locks)

### Concept

**"Lock first, then modify"**

- Acquire exclusive lock when reading
- Other transactions wait
- Guaranteed consistency
- Lower concurrency (blocking)

### Implementation: SELECT FOR UPDATE

```python
from django.db import transaction

@transaction.atomic
def book_seat_pessimistic(seat_id):
    # Step 1: Acquire lock
    seat = ShowSeat.objects.select_for_update().get(id=seat_id)
    # SQL: SELECT * FROM show_seat WHERE id = 5 FOR UPDATE;
    #      ^ Locks this row!

    # Step 2: Check availability (safe - we have lock)
    if seat.status != 'AVAILABLE':
        raise ValueError("Seat not available")

    # Step 3: Update
    seat.status = 'BOOKED'
    seat.save()

    # Lock released when transaction commits
```

### How It Works

```
Time  | User A                          | User B
------|----------------------------------|----------------------------------
T1    | BEGIN TRANSACTION                |
T2    | SELECT ... FOR UPDATE (lock 5A)  |
T3    |                                  | BEGIN TRANSACTION
T4    | Check: AVAILABLE ✓               | SELECT ... FOR UPDATE (WAITING...)
T5    | Update to BOOKED                 | (still waiting...)
T6    | COMMIT (release lock)            | (still waiting...)
T7    |                                  | Lock acquired!
T8    |                                  | Check: BOOKED ❌
T9    |                                  | ROLLBACK (seat not available)
------|----------------------------------|----------------------------------
Result: User A gets seat, User B fails gracefully ✓
```

### SQL Execution

```sql
-- User A's transaction
BEGIN;
SELECT * FROM show_seat WHERE id = 5 FOR UPDATE;  -- Locks row
-- Row is locked, User B must wait

UPDATE show_seat SET status = 'BOOKED' WHERE id = 5;
COMMIT;  -- Releases lock


-- User B's transaction (waits at SELECT)
BEGIN;
SELECT * FROM show_seat WHERE id = 5 FOR UPDATE;  -- Waits for lock
-- Gets lock after User A commits, sees BOOKED status
ROLLBACK;
```

### Variations

```python
# Default: Wait for lock
seat = ShowSeat.objects.select_for_update().get(id=5)

# nowait=True: Fail immediately if locked
try:
    seat = ShowSeat.objects.select_for_update(nowait=True).get(id=5)
except DatabaseError:
    return "Seat is being booked by another user"

# skip_locked=True: Skip locked rows
available_seats = ShowSeat.objects.select_for_update(
    skip_locked=True
).filter(status='AVAILABLE')
```

### Deadlock Risk

**Problem**: Two transactions waiting for each other.

```
Time  | Transaction A        | Transaction B
------|----------------------|---------------------
T1    | Lock seat 5A         |
T2    |                      | Lock seat 5B
T3    | Try lock 5B (wait)   |
T4    |                      | Try lock 5A (wait)
------|----------------------|---------------------
Result: DEADLOCK! Both waiting forever
```

**Solution**: Always acquire locks in same order!

```python
# Good: Lock in sorted order
seat_ids = [5, 3, 7]
seats = ShowSeat.objects.select_for_update().filter(
    id__in=sorted(seat_ids)  # Always lock in ascending ID order
).order_by('id')
```

---

## Optimistic Locking (Version-based)

### Concept

**"Read freely, check before write"**

- No locks on read
- Version/timestamp column tracks changes
- Update only if version matches
- Retry if version changed

### Implementation: Version Field

```python
class ShowSeat(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    version = models.IntegerField(default=0)  # ← Version field

@transaction.atomic
def book_seat_optimistic(seat_id):
    # Step 1: Read without lock
    seat = ShowSeat.objects.get(id=seat_id)
    old_version = seat.version  # Remember version

    # Step 2: Check availability
    if seat.status != 'AVAILABLE':
        raise ValueError("Seat not available")

    # Step 3: Try to update with version check
    updated = ShowSeat.objects.filter(
        id=seat_id,
        version=old_version,  # Only update if version unchanged
        status='AVAILABLE'
    ).update(
        status='BOOKED',
        version=F('version') + 1  # Increment atomically
    )

    # Step 4: Check if update succeeded
    if updated == 0:
        # Someone else modified it!
        raise OptimisticLockException("Seat was modified by another user")
```

### How It Works

```
Time  | User A                               | User B
------|--------------------------------------|--------------------------------------
T1    | Read seat 5A (version=1, AVAILABLE)  |
T2    |                                      | Read seat 5A (version=1, AVAILABLE)
T3    | Update WHERE version=1               |
      | ✓ Success! (version → 2)             |
T4    |                                      | Update WHERE version=1
      |                                      | ❌ Updated 0 rows (version is now 2!)
T5    |                                      | Detect conflict, RETRY
T6    |                                      | Read seat 5A (version=2, BOOKED)
T7    |                                      | Fail: Seat not available
------|--------------------------------------|--------------------------------------
Result: User A gets seat, User B retries and fails gracefully ✓
```

### SQL Execution

```sql
-- User A's transaction
BEGIN;
SELECT * FROM show_seat WHERE id = 5;  -- version = 1, status = AVAILABLE

UPDATE show_seat
SET status = 'BOOKED', version = version + 1
WHERE id = 5 AND version = 1 AND status = 'AVAILABLE';
-- 1 row updated ✓
COMMIT;


-- User B's transaction (concurrent)
BEGIN;
SELECT * FROM show_seat WHERE id = 5;  -- version = 1, status = AVAILABLE (stale!)

UPDATE show_seat
SET status = 'BOOKED', version = version + 1
WHERE id = 5 AND version = 1 AND status = 'AVAILABLE';
-- 0 rows updated ❌ (version is now 2, not 1!)
ROLLBACK;
```

### Retry Logic

```python
MAX_RETRIES = 3

for attempt in range(MAX_RETRIES):
    try:
        return book_seat_optimistic(seat_id)
    except OptimisticLockException:
        if attempt == MAX_RETRIES - 1:
            raise ValueError("Failed after multiple attempts")
        time.sleep(0.1 * (2 ** attempt))  # Exponential backoff
```

---

## Thread-based Locking

### Concept

**Application-level locking** using Python threading.

**IMPORTANT**: Only works within single Python process!

### Implementation

```python
import threading
from collections import defaultdict

class BookingService:
    # Class-level lock manager
    _seat_locks = defaultdict(threading.Lock)

    def book_seat_thread(self, seat_id):
        # Get lock for this seat
        lock = self._seat_locks[seat_id]

        # Acquire lock
        with lock:
            # Only one thread can execute this at a time
            seat = ShowSeat.objects.get(id=seat_id)

            if seat.status != 'AVAILABLE':
                raise ValueError("Seat not available")

            seat.status = 'BOOKED'
            seat.save()
```

### Why This DOESN'T WORK in Production

```
┌─────────────┐           ┌─────────────┐
│  Server 1   │           │  Server 2   │
│             │           │             │
│  User A ────┼─┐         │             │
│  (Lock 5A)  │ │         │  User B ────┼─┐
│             │ │         │  (Lock 5A)  │ │
│  Thread Lock│ │         │  Thread Lock│ │
│      ✓      │ │         │      ✓      │ │
└─────────────┘ │         └─────────────┘ │
                │                         │
                ├─────────────────────────┤
                │     Database (5A)       │
                │   BOTH ACCESS! ❌       │
                └─────────────────────────┘
```

**Different processes = Different locks!**

### When to Use Thread Locks

1. **Single-server applications** (development, small apps)
2. **In-memory data structures** (caches, queues)
3. **Educational purposes** (understanding concurrency)
4. **Background job processing** (single Celery worker)

### For Distributed Systems

Use **distributed locks** instead:
- **Redis**: `SETNX` command, Redlock algorithm
- **Database locks**: Our pessimistic approach
- **Zookeeper, etcd**: Coordination services

---

## Comparison and When to Use

### Feature Comparison

| Feature               | Pessimistic        | Optimistic         | Thread Locks       |
|-----------------------|--------------------|--------------------|-------------------|
| **Lock Acquisition**  | On read            | None               | On critical section |
| **Concurrency**       | Low (blocking)     | High (non-blocking)| Low (blocking)    |
| **Consistency**       | Guaranteed         | Eventually         | Process-only      |
| **Retry Logic**       | Not needed         | Required           | Not needed        |
| **Deadlock Risk**     | Yes                | No                 | Yes               |
| **Distributed**       | Yes ✓              | Yes ✓              | No ❌             |
| **Complexity**        | Medium             | High               | Low               |
| **Performance**       | Lower              | Higher             | Highest (local)   |

### When to Use Each

**Pessimistic Locking**:
```
✓ High contention (popular movie, few seats)
✓ Critical operations (payment, inventory)
✓ Cannot afford conflicts/retries
✓ Short transactions
✗ Read-heavy workloads
✗ Long-running transactions
```

**Optimistic Locking**:
```
✓ Low contention (regular show, many seats)
✓ Read-heavy workloads
✓ Long-running transactions
✓ High concurrency needed
✗ High conflict probability
✗ Expensive retry operations
```

**Thread Locks**:
```
✓ Single-server application
✓ In-memory data structures
✓ Educational purposes
✗ Distributed systems
✗ Multiple servers (production)
```

---

## Real-world Scenarios

### Scenario 1: Friday Night Blockbuster

**Context**: Avengers Endgame, first show, only 10 seats left.

**Expected**: High contention, many users competing.

**Best Choice**: **Pessimistic Locking**
- Conflicts are certain
- Need guaranteed consistency
- Users expect to wait (show is in demand)
- Retry logic would cause poor UX

```python
# Use select_for_update
seats = ShowSeat.objects.select_for_update().filter(
    show=show,
    status='AVAILABLE'
)[:user_seat_count]
```

### Scenario 2: Weekday Afternoon Movie

**Context**: Regular movie, 200 seats, low demand.

**Expected**: Low contention, few concurrent bookings.

**Best Choice**: **Optimistic Locking**
- Conflicts are rare
- Higher throughput needed
- Rare retry is acceptable
- Better user experience (no waiting for locks)

```python
# Use version field
updated = ShowSeat.objects.filter(
    id__in=seat_ids,
    version=old_version,
    status='AVAILABLE'
).update(status='LOCKED', version=F('version') + 1)
```

### Scenario 3: Browsing Available Seats

**Context**: User viewing seat map, checking availability.

**Expected**: Read-only operation, no updates.

**Best Choice**: **No Locking**
- Just read, don't lock
- Use database indexes for performance
- Stale data is acceptable for browsing

```python
# Simple query, no locks
available_seats = ShowSeat.objects.filter(
    show=show,
    status='AVAILABLE'
).select_related('seat')
```

### Scenario 4: Hybrid Approach (Real BookMyShow)

```python
class BookingService:
    def book_tickets(self, show_id, seat_ids):
        # Step 1: Optimistic check (fast, no lock)
        seats = ShowSeat.objects.filter(
            id__in=seat_ids,
            status='AVAILABLE'
        )

        if seats.count() != len(seat_ids):
            raise ValueError("Some seats not available")

        # Step 2: Pessimistic lock for final booking
        @transaction.atomic
        def final_booking():
            seats = ShowSeat.objects.select_for_update().filter(
                id__in=seat_ids,
                status='AVAILABLE'
            )

            if seats.count() != len(seat_ids):
                raise ValueError("Seats became unavailable")

            # Proceed with booking
            seats.update(status='LOCKED')
            return create_ticket(seats)

        return final_booking()
```

---

## Interview Questions

### Q1: What is a race condition?

**Answer**: When the outcome depends on the sequence/timing of uncontrollable events. In BookMyShow, two users reading seat availability at the same time and both booking it.

### Q2: Pessimistic vs Optimistic - which is better?

**Answer**: Neither is universally better. Depends on:
- **Contention probability**: High → Pessimistic, Low → Optimistic
- **Transaction duration**: Short → Pessimistic, Long → Optimistic
- **Retry cost**: High → Pessimistic, Low → Optimistic

### Q3: Can thread locks work in Django?

**Answer**: Yes, but ONLY for single-server deployments. Production systems use multiple servers (horizontal scaling), so thread locks don't work across servers. Use database locks or distributed locks (Redis) instead.

### Q4: What is a deadlock? How to prevent?

**Answer**: Two transactions waiting for each other's locks.

**Prevention**:
- Always acquire locks in same order (sorted IDs)
- Use timeouts (`select_for_update(nowait=True)`)
- Keep transactions short
- Detect and retry on deadlock

### Q5: How does SELECT FOR UPDATE work?

**Answer**: Acquires exclusive row-level lock. Other transactions trying to `SELECT FOR UPDATE` the same rows will wait until the lock is released (transaction commits/rollbacks).

### Q6: What's the version field in optimistic locking?

**Answer**: Counter incremented on each update. Before updating, check if version matches what was read. If not, data was modified by someone else → retry.

### Q7: How to handle distributed locking?

**Answer**:
1. **Database locks**: Our pessimistic approach (works across servers)
2. **Redis**: `SETNX` (set if not exists) for distributed locks
3. **Zookeeper/etcd**: Dedicated coordination services

### Q8: What is optimistic lock exception?

**Answer**: Thrown when update fails because version doesn't match (data was modified by another transaction). Requires retry logic.

### Q9: Can you have both pessimistic and optimistic?

**Answer**: Yes! Hybrid approach:
- Optimistic for initial checks (fast)
- Pessimistic for final commit (safe)

### Q10: How to test concurrency issues?

**Answer**:
```python
import threading

def test_concurrent_booking():
    def book():
        booking_service.book_seat(seat_id=5)

    # Create 10 threads trying to book same seat
    threads = [threading.Thread(target=book) for _ in range(10)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    # Verify: Only 1 booking succeeded
    assert ShowSeat.objects.get(id=5).status == 'BOOKED'
```

---

## Summary

### Key Takeaways

1. **Concurrency problems** arise when multiple transactions access shared data
2. **Pessimistic locking**: Lock first, modify later (safe, lower concurrency)
3. **Optimistic locking**: Modify with version check, retry on conflict (fast, higher concurrency)
4. **Thread locks**: Only for single-process applications
5. **No silver bullet**: Choose based on contention probability and requirements

### Decision Tree

```
Need concurrency control?
   │
   ├─ Yes ─→ Single server?
   │           │
   │           ├─ Yes ─→ Thread locks OK (but use DB locks anyway for future)
   │           │
   │           └─ No (distributed) ─→ High contention?
   │                                    │
   │                                    ├─ Yes ─→ Pessimistic (SELECT FOR UPDATE)
   │                                    │
   │                                    └─ No ─→ Optimistic (version field)
   │
   └─ No ─→ Read-only / Eventually consistent is OK
```

### Remember

- **BookMyShow uses database locks** (pessimistic or optimistic), NOT thread locks
- **Test concurrency** with threading/multiprocessing
- **Understand trade-offs** for interview discussions
- **Real systems** often use hybrid approaches

**Master these concepts - they're critical for LLD interviews!**
