# Category Guide: Scheduling & Calendar Systems

## Overview

Scheduling systems deal with **time-based events, recurring patterns, and conflict detection**. They test your understanding of datetime handling, timezone complexity, and efficient querying of time-based data.

---

## Common Entities

| Entity | Purpose | Example |
|--------|---------|---------|
| Event | Time-based occurrence | Meeting, Appointment |
| Calendar | Collection of events | Personal, Work calendar |
| Recurrence | Repeating pattern | Daily, Weekly, Monthly |
| Slot | Individual occurrence | One instance of recurring event |
| Participant | Event attendee | Required, Optional attendee |

---

## Key Design Patterns

### 1. Strategy Pattern - For Recurrence Calculation
```
                    ┌───────────────────────┐
                    │ RecurrenceStrategy    │ (ABC)
                    │ + getOccurrences()    │
                    └───────────┬───────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│    Daily      │      │    Weekly     │      │   Monthly     │
└───────────────┘      └───────────────┘      └───────────────┘
```

### 2. Factory Pattern - For Event Types
```
class EventFactory:
    def create(type, data):
        if type == "MEETING": return Meeting(data)
        if type == "REMINDER": return Reminder(data)
        if type == "ALL_DAY": return AllDayEvent(data)
```

### 3. Observer Pattern - For Notifications
```
Event time approaching → Notify participants
Event updated → Notify all attendees
```

---

## Core Class Design

### Event Hierarchy
```
┌─────────────────────────────┐
│          Event              │
├─────────────────────────────┤
│ - id                        │
│ - title                     │
│ - description               │
│ - calendar_id               │
│ - organizer_id              │
│ - visibility                │
│ - recurrence_info           │
└─────────────────────────────┘
              △
              │
    ┌─────────┴─────────┐
    ▼                   ▼
┌───────────────┐ ┌─────────────────┐
│   TimeEvent   │ │    DayEvent     │
├───────────────┤ ├─────────────────┤
│ - start_time  │ │ - date          │
│ - end_time    │ │ (No time needed)│
│ - timezone    │ └─────────────────┘
│ - location    │
│ - participants│
└───────────────┘
```

### Slot-based Design (For Efficient Querying)
```
┌─────────────────┐         ┌─────────────────────┐
│     Event       │         │       Slot          │
├─────────────────┤         ├─────────────────────┤
│ - id            │ 1:N     │ - id                │
│ - title         │────────▶│ - event_id          │
│ - recurrence    │         │ - start_time        │
└─────────────────┘         │ - end_time          │
                            │ - is_modified       │
                            │ - is_cancelled      │
                            └─────────────────────┘

Event = Definition (rules)
Slot = Individual occurrence (for fast queries)
```

### Recurrence Info
```
┌─────────────────────────────┐
│       RecurrenceInfo        │
├─────────────────────────────┤
│ - frequency: DAILY|WEEKLY|  │
│              MONTHLY|YEARLY │
│ - interval: int             │ ← Every N periods
│ - days_of_week[]            │ ← For weekly
│ - day_of_month              │ ← For monthly
│ - end_type: NEVER|UNTIL|    │
│             COUNT           │
│ - end_date                  │
│ - occurrence_count          │
└─────────────────────────────┘
```

---

## Critical: Updating Recurring Events

### The Three Scenarios
```
Original:  [E1] → [E2] → [E3] → [E4] → [E5]
                        ↑
                   Edit E3

Option 1: THIS ONLY     → E3 becomes exception
Option 2: THIS & FUTURE → Split into 2 series
Option 3: ALL           → Update original event
```

### Implementation
```python
def update_event(event_id, slot_date, changes, scope):
    event = Event.get(event_id)

    if scope == UpdateScope.THIS_ONLY:
        # Mark slot as modified
        slot = Slot.get(event_id, slot_date)
        slot.is_modified = True
        slot.apply_changes(changes)

    elif scope == UpdateScope.THIS_AND_FUTURE:
        # End original series
        event.recurrence.end_date = slot_date - timedelta(days=1)

        # Create new series
        new_event = Event.create_from(event, changes)
        new_event.recurrence.start_date = slot_date
        generate_slots(new_event)

    elif scope == UpdateScope.ALL:
        # Update event directly
        event.apply_changes(changes)
        regenerate_slots(event)
```

---

## Critical: Timezone Handling

### The Problem
```
User creates "Meeting at 9 AM" in New York
After DST change: Should still show 9 AM
Participant in London: Should see correct local time
```

### Solutions

**Store Local Time + Timezone (Recommended)**
```
start_time: 09:00
timezone: "America/New_York"

Not UTC! Because:
- "9 AM meeting" should stay at 9 AM after DST
- UTC value changes with DST
```

**For All-Day Events**
```
No timezone needed - "Holiday on Jan 1" is Jan 1 everywhere
Store just the date
```

### Edge Cases
```
| Case                    | Solution                    |
|-------------------------|----------------------------|
| DST gap (2:30 AM gone)  | Skip to next valid time    |
| DST overlap (2:30 twice)| Pick first occurrence      |
| Different TZ start/end  | Store timezone for each    |
```

---

## Meeting Scheduler (Conflict Detection)

### Find Available Slots
```python
def find_available_slots(participants, duration, date_range):
    """Find time slots when all participants are free"""
    slots = []

    for day in date_range:
        # Get busy times for all participants on this day
        busy_times = []
        for user_id in participants:
            events = get_events(user_id, day)
            busy_times.extend([(e.start, e.end) for e in events])

        # Merge overlapping busy times
        merged_busy = merge_intervals(busy_times)

        # Find gaps >= duration
        free_slots = find_gaps(merged_busy, day.start, day.end, duration)
        slots.extend(free_slots)

    return slots
```

### Conflict Detection
```python
def has_conflict(user_id, new_event):
    existing = get_events(user_id, new_event.date)
    for event in existing:
        if overlaps(event, new_event):
            return True, event
    return False, None

def overlaps(e1, e2):
    return e1.start < e2.end and e2.start < e1.end
```

---

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Store UTC only | DST breaks recurring events | Store local time + timezone |
| No slots table | Slow calendar queries | Pre-generate slots |
| Update all slots | "This only" edit fails | Track modified slots |
| Infinite recurrence | Can't generate all slots | Limit or generate on-demand |
| Missing RSVP | Don't know who's coming | Add participant response |

---

## Coding Hacks for Demo

### 1. Recurrence Generation
```python
def generate_occurrences(event, until_date):
    occurrences = []
    current = event.start_date

    while current <= until_date:
        if not event.is_exception(current):
            occurrences.append(current)

        if event.recurrence.frequency == "DAILY":
            current += timedelta(days=event.recurrence.interval)
        elif event.recurrence.frequency == "WEEKLY":
            current += timedelta(weeks=event.recurrence.interval)
        # ... etc

    return occurrences
```

### 2. Quick Overlap Check
```python
def events_overlap(e1_start, e1_end, e2_start, e2_end):
    return e1_start < e2_end and e2_start < e1_end

# For finding free slots
def find_gaps(busy_intervals, day_start, day_end, min_duration):
    sorted_busy = sorted(busy_intervals)
    free = []
    current = day_start

    for start, end in sorted_busy:
        if start - current >= min_duration:
            free.append((current, start))
        current = max(current, end)

    if day_end - current >= min_duration:
        free.append((current, day_end))

    return free
```

### 3. RSVP Tracking
```python
class EventParticipant:
    def __init__(self, event_id, user_id):
        self.event_id = event_id
        self.user_id = user_id
        self.response = RSVPStatus.PENDING  # YES, NO, MAYBE, PENDING
        self.is_organizer = False
        self.is_optional = False
```

### 4. Calendar View Query
```python
def get_calendar_view(user_id, start_date, end_date):
    # Get user's calendars
    calendars = Calendar.get_by_user(user_id)

    # Get slots in date range
    slots = Slot.query.filter(
        Slot.event.calendar_id.in_([c.id for c in calendars]),
        Slot.start_time >= start_date,
        Slot.end_time <= end_date,
        Slot.is_cancelled == False
    ).all()

    return slots
```

---

## API Design

### Calendar
```
POST   /calendars                    # Create calendar
GET    /calendars                    # List user's calendars
GET    /calendars/{id}/events        # Get events in date range
```

### Events
```
POST   /events                       # Create event
GET    /events/{id}                  # Get event details
PUT    /events/{id}?scope=THIS       # Update (scope: THIS|FUTURE|ALL)
DELETE /events/{id}?scope=THIS       # Delete (scope: THIS|FUTURE|ALL)

# Participants
POST   /events/{id}/participants     # Invite
POST   /events/{id}/rsvp             # Respond to invite
```

### Meeting Scheduler
```
GET    /availability?users=1,2,3&date=2024-01-15
POST   /meetings/suggest             # Suggest meeting times

# Request
POST /meetings/suggest
{
    "participants": ["user-1", "user-2"],
    "duration_minutes": 60,
    "date_range": {
        "start": "2024-01-15",
        "end": "2024-01-19"
    }
}

# Response
{
    "suggested_slots": [
        {"start": "2024-01-15T10:00", "end": "2024-01-15T11:00"},
        {"start": "2024-01-15T14:00", "end": "2024-01-15T15:00"},
        ...
    ]
}
```

### Event Creation
```json
POST /events
{
    "calendar_id": "cal-123",
    "title": "Team Standup",
    "start_time": "09:00",
    "end_time": "09:30",
    "timezone": "America/New_York",
    "recurrence": {
        "frequency": "WEEKLY",
        "days_of_week": [1, 3, 5],  // Mon, Wed, Fri
        "end_type": "UNTIL",
        "end_date": "2024-12-31"
    },
    "participants": [
        {"user_id": "user-1", "optional": false},
        {"user_id": "user-2", "optional": true}
    ]
}
```

---

## Interview Questions to Expect

1. "How do you handle **recurring event updates**?"
   → Three scopes: this only (exception), this+future (split), all (update)

2. "How to efficiently **query events for a date range**?"
   → Pre-generate slots, simple date range query on slots table

3. "How would you find **meeting slots** for 10 people?"
   → Merge all busy times, find gaps >= meeting duration

4. "How to handle **timezone changes** for recurring events?"
   → Store local time + IANA timezone, compute on display

5. "How to implement **event reminders**?"
   → Background job checking upcoming events, send notifications

---

## Checklist Before Interview

- [ ] Understand Event vs Slot design
- [ ] Know recurring event update scenarios
- [ ] Can explain timezone storage approach
- [ ] Know how to detect conflicts
- [ ] Can find available meeting slots
- [ ] Understand DST edge cases
- [ ] Can design participant RSVP flow
