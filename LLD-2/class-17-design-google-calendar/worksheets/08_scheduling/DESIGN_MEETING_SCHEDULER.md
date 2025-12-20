# Design Meeting Scheduler

## Overview

A meeting scheduler helps find common available time slots for multiple participants. It integrates with calendars, detects conflicts, and suggests optimal meeting times.

**Key Features:**
- View participant availability
- Find common free slots
- Schedule meetings
- Handle recurring meetings
- Conflict detection

---

## Expectations

* Code should be functionally correct.
* Code should be modular and readable.
* Code should be extensible and scalable.
* Code should have good OOP design principles.

---

## Requirements Gathering

```
1.
2.
3.
4.
5.
```

<details>
<summary><strong>Sample clarifying questions</strong></summary>

1. How many participants maximum?
2. Consider timezone differences?
3. Working hours constraints?
4. Minimum meeting duration?
5. Room/resource booking?
6. Auto-suggest vs manual selection?

</details>

---

## Requirements

```
1.
2.
3.
4.
5.
6.
7.
```

<details>
<summary><strong>Click to see requirements</strong></summary>

1. Users can view their own calendar.
2. Users can check availability of others.
3. System suggests free slots for all participants.
4. Users can schedule meetings with participants.
5. System detects and prevents conflicts.
6. Support for different meeting durations.
7. Consider working hours only.

</details>

---

## Class Diagram

**Think about:**
- Calendar and Event relationship
- How to represent availability
- Finding common free slots algorithm
- Meeting vs Event

**Design Question: Availability Representation**
```
How to store/represent availability?

Option A: List of busy slots
Option B: List of free slots
Option C: Bit array per time slot

Your choice:

```

List your classes:

```
Class 1:

Class 2:

Class 3:

Class 4:
```

Draw the class diagram:

```




```

---

## Key Design Decisions

**1. Finding Common Slots Algorithm**
```
3 users with different busy times.
How to find 1-hour slots when all are free?

Your approach:

```

**2. Timezone Handling**
```
User A in NYC, User B in London.
How to show available slots?

```

**3. Working Hours**
```
Don't suggest 3 AM meetings.
How to enforce?

```

---

## API Design

```
1.
2.
3.
4.
```

---

## Hints

<details>
<summary><strong>Hint 1: Core Classes</strong></summary>

```python
class TimeSlot:
    start: datetime
    end: datetime

    def overlaps(self, other: 'TimeSlot') -> bool:
        return self.start < other.end and other.start < self.end

    def duration_minutes(self) -> int:
        return (self.end - self.start).seconds // 60

class Calendar:
    user_id: str
    events: List[Event]
    working_hours: WorkingHours

    def get_busy_slots(self, date: date) -> List[TimeSlot]:
        return [TimeSlot(e.start, e.end)
                for e in self.events
                if e.date == date]

class WorkingHours:
    start_time: time  # e.g., 09:00
    end_time: time    # e.g., 18:00
    days: List[int]   # 0=Mon, 6=Sun
```

</details>

<details>
<summary><strong>Hint 2: Finding Free Slots</strong></summary>

```python
def find_free_slots(busy_slots: List[TimeSlot],
                    day_start: datetime,
                    day_end: datetime,
                    min_duration: int) -> List[TimeSlot]:
    """Find free slots of at least min_duration minutes"""

    # Sort busy slots
    sorted_busy = sorted(busy_slots, key=lambda s: s.start)

    # Merge overlapping busy slots
    merged = merge_intervals(sorted_busy)

    # Find gaps
    free_slots = []
    current = day_start

    for busy in merged:
        if busy.start > current:
            gap = TimeSlot(current, busy.start)
            if gap.duration_minutes() >= min_duration:
                free_slots.append(gap)
        current = max(current, busy.end)

    # Check gap after last busy slot
    if current < day_end:
        gap = TimeSlot(current, day_end)
        if gap.duration_minutes() >= min_duration:
            free_slots.append(gap)

    return free_slots
```

</details>

<details>
<summary><strong>Hint 3: Common Availability</strong></summary>

```python
def find_common_availability(
    user_ids: List[str],
    date_range: Tuple[date, date],
    duration_minutes: int
) -> List[TimeSlot]:
    """Find slots when ALL users are free"""

    common_slots = []

    for day in get_dates_in_range(*date_range):
        # Get free slots for each user
        all_free_slots = []
        for user_id in user_ids:
            calendar = Calendar.get(user_id)
            busy = calendar.get_busy_slots(day)
            working = calendar.working_hours

            day_start = datetime.combine(day, working.start_time)
            day_end = datetime.combine(day, working.end_time)

            free = find_free_slots(busy, day_start, day_end, duration_minutes)
            all_free_slots.append(free)

        # Find intersection of all free slots
        common = intersect_all_slots(all_free_slots)
        common_slots.extend(common)

    return common_slots

def intersect_all_slots(slot_lists: List[List[TimeSlot]]) -> List[TimeSlot]:
    """Find time ranges where all lists have free time"""
    if not slot_lists:
        return []

    result = slot_lists[0]
    for slots in slot_lists[1:]:
        result = intersect_two_slot_lists(result, slots)

    return result
```

</details>

<details>
<summary><strong>Hint 4: Class Diagram</strong></summary>

```
┌─────────────────────────────┐
│      MeetingScheduler       │
├─────────────────────────────┤
│ + findAvailability(users,   │
│     dateRange, duration)    │
│ + scheduleMeeting(meeting)  │
│ + checkConflicts(user, slot)│
└─────────────────────────────┘

┌─────────────────────────────┐
│         Calendar            │
├─────────────────────────────┤
│ - user_id                   │
│ - events[]                  │
│ - working_hours             │
├─────────────────────────────┤
│ + getBusySlots(date)        │
│ + getFreeSlots(date)        │
│ + addEvent(event)           │
└─────────────────────────────┘

┌─────────────────────────────┐
│          Meeting            │
├─────────────────────────────┤
│ - id                        │
│ - title                     │
│ - organizer_id              │
│ - participants[]            │
│ - start_time                │
│ - end_time                  │
│ - location                  │
│ - status                    │
└─────────────────────────────┘

┌─────────────────────────────┐
│         TimeSlot            │
├─────────────────────────────┤
│ - start: datetime           │
│ - end: datetime             │
├─────────────────────────────┤
│ + overlaps(other)           │
│ + duration()                │
│ + contains(time)            │
└─────────────────────────────┘
```

</details>

<details>
<summary><strong>Hint 5: API Design</strong></summary>

```
# Check availability
GET /users/{id}/availability?date=2024-01-15

# Find common slots
POST /meetings/suggest
{
    "participants": ["user1", "user2", "user3"],
    "duration_minutes": 60,
    "date_range": {
        "start": "2024-01-15",
        "end": "2024-01-19"
    }
}

Response:
{
    "suggested_slots": [
        {"start": "2024-01-15T10:00", "end": "2024-01-15T11:00"},
        {"start": "2024-01-16T14:00", "end": "2024-01-16T15:00"}
    ]
}

# Schedule meeting
POST /meetings
{
    "title": "Project Sync",
    "participants": ["user1", "user2"],
    "start_time": "2024-01-15T10:00",
    "end_time": "2024-01-15T11:00"
}
```

</details>
