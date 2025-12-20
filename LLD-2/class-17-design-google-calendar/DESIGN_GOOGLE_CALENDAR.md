# Design Google Calendar

## Overview

Google Calendar is a time-management and scheduling service that allows users to create, manage, and share events. Think of your typical workflow:

- You create a "Team Standup" meeting every Monday, Wednesday, and Friday at 10 AM
- You invite your teammates, and they can see it on their calendars
- One week, you need to skip Wednesday's meeting - you delete just that occurrence
- Your colleague in London sees the meeting at 3 PM their time (timezone handling!)

This design document walks through how to build such a system, starting from a naive approach and iteratively improving it.

---

## Table of Contents
1. [Requirements](#requirements-gathering)
2. [Class Design Evolution](#class-diagram---incremental-design)
3. [The Slots Concept](#why-slots-the-key-insight)
4. [Handling Recurring Event Updates](#updating-recurring-events---the-tricky-part)
5. [API Design](#api-design)
6. [Timezone Handling](#timezone-handling---critical-complexity)
7. [Edge Cases](#edge-cases-to-consider)

---

## Requirements Gathering

### Functional Requirements

**1. CRUD Operations on Events**
```
Example:
- Priya creates "1:1 with Manager" on her Work calendar
- She later updates the meeting room from "Room A" to "Room B"
- She deletes an old event that already passed
```

**2. Invite Participants to Events**
```
Example:
- Rahul creates "Project Kickoff" and invites 5 team members
- Each team member sees the event on their calendar
- They can RSVP: Accept / Decline / Maybe
```

**3. Event Attributes**
Every event has:

| Attribute | Example |
|-----------|---------|
| Title | "Sprint Planning" |
| Start time | 2024-01-15 10:00 AM |
| End time | 2024-01-15 11:30 AM |
| Participants | [rahul@company.com, priya@company.com] |
| Visibility | Private (only invitees can see) |
| Description | "Discuss Q1 goals and assign tasks" |

**4. Recurring Events**
```
Example scenarios:
- "Daily Standup" → Every day at 9:30 AM
- "Team Sync" → Every Monday and Thursday at 2 PM
- "Monthly Review" → First Monday of every month at 11 AM
- "Birthday Reminder" → January 15th every year
```

**5. Meeting Types**
```
Online Meeting:
  - Title: "Client Call"
  - Link: https://zoom.us/j/123456789
  - Platform: Zoom

Offline Meeting:
  - Title: "Team Lunch"
  - Location: "Cafeteria, Building A, 2nd Floor"
```

**6. Visibility Controls**

| Visibility | Who Can See | What They See |
|------------|-------------|---------------|
| Public | Everyone | Full event details |
| Private | Only invitees | Full event details |
| Busy | Everyone | Just "Busy" block, no details |

### Non-Functional Requirements
- High availability (calendar should always work!)
- Low latency for queries (< 100ms to load a week's events)
- Support for multiple timezones
- Scale to millions of users

---

## Class Diagram - Incremental Design

Let's design this step-by-step, making mistakes and learning from them.

### Attempt 1: The Naive "Everything in One Class" Approach

**First instinct:** Put all event information in a single class.

```
┌─────────────────────────────────────────┐
│                 Event                    │
├─────────────────────────────────────────┤
│ - id: UUID                               │
│ - title: String                          │
│ - start_time: DateTime                   │
│ - end_time: DateTime                     │
│ - is_recurring: Boolean                  │
│ - recurrence_type: String                │  ← "daily", "weekly", etc.
│ - recurrence_end: Date                   │
│ - is_online: Boolean                     │
│ - meeting_link: String                   │  ← Only used if is_online=true
│ - location: String                       │  ← Only used if is_online=false
│ - visibility: String                     │
│ - participants: List[User]               │
└─────────────────────────────────────────┘
```

**What's wrong with this?**

| Problem | Example | Why It's Bad |
|---------|---------|--------------|
| Conditional fields | `meeting_link` is null for offline events | Wasted memory, confusing nulls |
| Redundant booleans | `is_recurring` + `recurrence_type` | If `recurrence_type` exists, it's recurring! |
| No separation of concerns | Event definition mixed with occurrence logic | Hard to query "what's on my calendar this week?" |
| String enums | `visibility: String` | No type safety, typos cause bugs |

**Real problem scenario:**
```
User asks: "Show me all events on January 15th, 2024"

For a daily recurring event starting Jan 1st:
- We must COMPUTE that Jan 15th is a valid occurrence
- We do this for EVERY recurring event in the system
- Very slow! O(n) where n = all recurring events
```

---

### Attempt 2: Extract Location Info

**Improvement:** Separate location concerns into its own class.

```
┌──────────────────────┐      ┌──────────────────────┐
│        Event         │      │     LocationInfo     │
├──────────────────────┤      ├──────────────────────┤
│ - id                 │      │ - type: ONLINE |     │
│ - title              │      │         OFFLINE      │
│ - start_time         │◆────▶│ - meeting_link       │ ← Still has
│ - end_time           │      │ - address            │   conditional
│ - location_info      │      │ - room               │   fields!
│ - visibility         │      └──────────────────────┘
│ - recurrence_info    │
│ - participants       │      ┌──────────────────────┐
│                      │      │   RecurrenceInfo     │
│                      │◆────▶├──────────────────────┤
│                      │      │ - freq_type: DAILY | │
│                      │      │   WEEKLY | MONTHLY   │
└──────────────────────┘      │ - interval           │
                              │ - end_date           │
                              └──────────────────────┘
```

**Better!** But still has issues:
- `LocationInfo` still has conditional fields (meeting_link unused for offline)
- All-day events (like "Holiday") mixed with timed events
- Still no efficient way to query occurrences

---

### Attempt 2.5: LocationInfo as Abstract Base Class

**Key Insight:** Use inheritance to eliminate conditional fields entirely.

```
┌──────────────────────┐      ┌─────────────────────────────┐
│        Event         │      │    LocationInfo (ABC)       │
├──────────────────────┤      ├─────────────────────────────┤
│ - id                 │      │ + get_display_string(): str │
│ - title              │      │ + get_join_url(): str       │
│ - start_time         │      └─────────────────────────────┘
│ - end_time           │                    △
│ - location_info ─────┼───▶                │
│ - visibility         │           ┌────────┴────────┐
│ - recurrence_info    │           │                 │
│ - participants       │           ▼                 ▼
└──────────────────────┘    ┌──────────────┐   ┌───────────────┐
                            │OnlineLocation│   │OfflineLocation│
                            ├──────────────┤   ├───────────────┤
                            │- meeting_link│   │- address      │
                            │- platform    │   │- room_name    │
                            │- password    │   │- building     │
                            └──────────────┘   └───────────────┘
```

**Python Implementation:**

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

class LocationInfo(ABC):
    """Abstract base for event locations"""

    @abstractmethod
    def get_display_string(self) -> str:
        """Return human-readable location"""
        pass

    @abstractmethod
    def get_join_url(self) -> Optional[str]:
        """Return URL if applicable, None otherwise"""
        pass

@dataclass
class OnlineLocation(LocationInfo):
    meeting_link: str
    platform: str      # "zoom", "meet", "teams"
    password: Optional[str] = None

    def get_display_string(self) -> str:
        return f"{self.platform.title()} Meeting"

    def get_join_url(self) -> Optional[str]:
        return self.meeting_link

@dataclass
class OfflineLocation(LocationInfo):
    address: str
    room_name: Optional[str] = None
    building: Optional[str] = None

    def get_display_string(self) -> str:
        parts = [self.address]
        if self.room_name:
            parts.append(f"Room: {self.room_name}")
        if self.building:
            parts.append(f"Building: {self.building}")
        return ", ".join(parts)

    def get_join_url(self) -> Optional[str]:
        return None  # No URL for physical locations
```

**Why ABC is better:**

| Benefit | Explanation |
|---------|-------------|
| No null fields | Each class has only relevant attributes |
| Type safety | Can't accidentally access `meeting_link` on offline location |
| Extensible | Easy to add `HybridLocation` later |
| Polymorphism | Call `location.get_display_string()` without checking type |

---

### Attempt 3: Separate Day Events vs Time Events

**Key Insight:** All-day events are fundamentally different from timed events.

```
Example: "New Year's Holiday"
- It's January 1st in EVERY timezone
- No start/end time, just a date
- Displayed differently (spans top of calendar)

vs.

Example: "Team Standup"
- 10:00 AM in a SPECIFIC timezone
- Someone in London sees different time than someone in NYC
- Has duration (10:00 - 10:30)
```

```
┌─────────────────────────┐     ┌─────────────────────────┐
│       DayEvent          │     │       TimeEvent         │
├─────────────────────────┤     ├─────────────────────────┤
│ - id                    │     │ - id                    │
│ - title                 │     │ - title                 │
│ - date                  │     │ - start_time            │
│ - recurrence_info       │     │ - end_time              │
│ - visibility            │     │ - timezone              │ ← Critical!
│                         │     │ - recurrence_info       │
│ (No timezone needed!)   │     │ - location_info         │
│                         │     │ - visibility            │
│                         │     │ - participants          │
└─────────────────────────┘     └─────────────────────────┘
```

**Still one major problem remains:** How do we efficiently query "What's on my calendar for January 15th?" for recurring events?

---

### Attempt 4: Introduce Slots (Final Design)

**The Problem We're Solving:**

```
Scenario: User has a daily standup (recurring) + 3 one-time meetings

User opens calendar for January 15-21 (one week view)

WITHOUT SLOTS:
1. Fetch all one-time events in date range → Simple query
2. Fetch ALL recurring events → Could be thousands!
3. For EACH recurring event, compute if it falls in Jan 15-21 → Slow!
4. Combine results → Complex

WITH SLOTS:
1. Query: "SELECT * FROM slots WHERE date BETWEEN Jan 15 AND Jan 21"
2. Done! → Fast and simple
```

**The Slots Concept:**

```
Original Recurring Event: "Daily Standup starting Jan 1st"
              │
              │ Pre-generate slots
              ▼
┌─────────────────────────────────────────────────────────┐
│ Slot: Jan 1   │ Slot: Jan 2   │ Slot: Jan 3   │ ...    │
│ event_id: E1  │ event_id: E1  │ event_id: E1  │        │
│ date: Jan 1   │ date: Jan 2   │ date: Jan 3   │        │
└─────────────────────────────────────────────────────────┘
```

**Final Class Diagram:**

```
┌─────────────────┐         ┌─────────────────────────────┐
│      User       │         │         Calendar            │
├─────────────────┤         ├─────────────────────────────┤
│ - id            │◀───────▶│ - id                        │
│ - name          │         │ - title                     │
│ - email         │         │ - owner                     │
│ - calendars[]   │         │ - shared_with[]             │
└─────────────────┘         │ - visibility                │
                            └─────────────────────────────┘
                                          │
                    ┌─────────────────────┴─────────────────────┐
                    ▼                                           ▼
        ┌───────────────────────┐               ┌───────────────────────────┐
        │      DayEvent         │               │        TimeEvent          │
        ├───────────────────────┤               ├───────────────────────────┤
        │ - id                  │               │ - id                      │
        │ - title               │               │ - title                   │
        │ - visibility          │               │ - start_time              │
        │ - recurrence_info     │               │ - end_time                │
        └───────────────────────┘               │ - timezone                │
                    │                           │ - location_info           │
                    │ 1:N                       │ - visibility              │
                    ▼                           │ - recurrence_info         │
        ┌───────────────────────┐               │ - participants[]          │
        │       DaySlot         │               └───────────────────────────┘
        ├───────────────────────┤                           │
        │ - id                  │                           │ 1:N
        │ - event_id (FK)       │                           ▼
        │ - date                │               ┌───────────────────────────┐
        │ - is_modified         │               │        TimeSlot           │
        │ - modified_title      │               ├───────────────────────────┤
        │ - is_cancelled        │               │ - id                      │
        └───────────────────────┘               │ - event_id (FK)           │
                                                │ - start_time              │
                                                │ - end_time                │
                                                │ - is_modified             │
                                                │ - modified_title          │
                                                │ - is_cancelled            │
                                                └───────────────────────────┘
```

**Example in Action:**

```
Event: "Weekly Team Sync" every Monday at 2 PM, starting Jan 1, 2024

TimeEvent (Parent):
┌────────────────────────────────┐
│ id: "evt-123"                  │
│ title: "Weekly Team Sync"      │
│ start_time: 14:00              │
│ end_time: 15:00                │
│ timezone: "Asia/Kolkata"       │
│ recurrence: Weekly, Mon        │
└────────────────────────────────┘

TimeSlots (Generated Children):
┌──────────────────────────────────────────────────────────────────────┐
│ Slot 1          │ Slot 2          │ Slot 3          │ Slot 4         │
│ event_id: evt-123│ event_id: evt-123│ event_id: evt-123│ event_id:evt-123│
│ date: Jan 1     │ date: Jan 8     │ date: Jan 15    │ date: Jan 22   │
│ is_modified: ❌  │ is_modified: ❌  │ is_modified: ✅  │ is_cancelled:✅ │
│                 │                 │ new_title:      │ (User skipped  │
│                 │                 │ "Sprint Review" │  this week)    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Why Slots? The Key Insight

### The Trade-off

| Approach | Query Speed | Storage Cost | Update Complexity |
|----------|-------------|--------------|-------------------|
| **Compute on-the-fly** | Slow | Low | Simple |
| **Store slots** | Fast | Higher | Medium |

### Why Slots Win

**1. Calendar UI Needs Fast Queries**
```
User opens week view → Must show all events in < 100ms

With slots:
  SELECT * FROM time_slots
  WHERE start_time BETWEEN '2024-01-15' AND '2024-01-21'

  → Simple index lookup, instant results!
```

**2. Individual Occurrence Modifications Become Simple**
```
User wants to rename just ONE occurrence of a recurring event

With slots:
  UPDATE time_slots
  SET is_modified = true, modified_title = 'New Name'
  WHERE id = 'slot-123'

  → One row update, done!
```

**3. Cancelling One Occurrence is Easy**
```
User wants to skip Monday's standup (vacation)

With slots:
  UPDATE time_slots
  SET is_cancelled = true
  WHERE id = 'slot-for-monday'

  → Just a flag flip!
```

**4. Slot Generation Strategy**
```
Don't generate infinite slots! Use batched generation:

- When event created: Generate slots for next 1 year
- Monthly job: Generate next batch as time passes
- Max limit: 730 occurrences (2 years) to prevent abuse
```

---

## Updating Recurring Events - The Tricky Part!

This is where Google Calendar shows a dialog: **"Edit this event or all events?"**

There are three scenarios to handle:

### Scenario 1: Update Only This Occurrence

**User Story:** "My standup is at 10 AM every day, but today I want to move it to 11 AM."

```
Original Series:  [Mon 10AM] → [Tue 10AM] → [Wed 10AM] → [Thu 10AM]
                                    ↓
User modifies Wednesday only     [Wed 11AM] (different time)

Result:           [Mon 10AM] → [Tue 10AM] → [Wed 11AM] → [Thu 10AM]
                                               ↑
                                        Only this slot changed
```

**Implementation:**

```python
def update_single_occurrence(slot_id: str, new_data: dict):
    slot = TimeSlot.get(slot_id)

    # Mark this slot as modified
    slot.is_modified = True
    slot.modified_title = new_data.get('title', slot.event.title)
    slot.start_time = new_data.get('start_time', slot.start_time)
    slot.end_time = new_data.get('end_time', slot.end_time)

    slot.save()
    # Parent event remains unchanged!
```

### Scenario 2: Update This and All Future Occurrences

**User Story:** "Starting this week, I want to move standup from 10 AM to 11 AM permanently."

```
Original Series:  [Mon 10AM] → [Tue 10AM] → [Wed 10AM] → [Thu 10AM] → [Fri 10AM]
                                    ↓
User changes from Wednesday onwards

Result:           [Mon 10AM] → [Tue 10AM] | [Wed 11AM] → [Thu 11AM] → [Fri 11AM]
                    ← Series 1 ends →     | ← New Series 2 starts →
```

**Implementation:**

```python
def update_this_and_future(event_id: str, from_slot_id: str, new_data: dict):
    original_event = TimeEvent.get(event_id)
    from_slot = TimeSlot.get(from_slot_id)

    # Step 1: End the original series before this date
    original_event.recurrence_info.end_date = from_slot.date - timedelta(days=1)

    # Delete future slots of original series
    TimeSlot.delete_where(event_id=event_id, date__gte=from_slot.date)

    # Step 2: Create a NEW recurring event starting from this date
    new_event = TimeEvent.create(
        title=new_data.get('title', original_event.title),
        start_time=new_data.get('start_time', original_event.start_time),
        end_time=new_data.get('end_time', original_event.end_time),
        recurrence_info=RecurrenceInfo(
            freq_type=original_event.recurrence_info.freq_type,
            start_date=from_slot.date,
            end_date=original_event.recurrence_info.end_date,  # Original end
        )
    )

    # Step 3: Generate slots for new series
    generate_slots_for_event(new_event)

    return new_event
```

### Scenario 3: Update All Occurrences (Entire Series)

**User Story:** "I want to rename my standup from 'Daily Sync' to 'Team Standup' for ALL occurrences."

```
Original Series:  [Daily Sync] → [Daily Sync] → [Daily Sync] → [Daily Sync]
                       ↓              ↓              ↓              ↓
User renames all

Result:           [Team Standup] → [Team Standup] → [Team Standup] → [Team Standup]
```

**Implementation:**

```python
def update_all_occurrences(event_id: str, new_data: dict):
    event = TimeEvent.get(event_id)

    # Update the parent event
    event.title = new_data.get('title', event.title)
    event.start_time = new_data.get('start_time', event.start_time)
    event.end_time = new_data.get('end_time', event.end_time)
    event.save()

    # Clear modifications on slots (they now inherit from parent)
    TimeSlot.update_where(
        event_id=event_id,
        is_modified=False,
        modified_title=None
    )

    # Regenerate slot times if time changed
    if 'start_time' in new_data or 'end_time' in new_data:
        regenerate_slot_times(event)
```

**Caution:** This affects PAST events too! You might want to only update future slots.

### Summary: Recurring Event Updates

| Update Type | What Happens | Database Changes |
|-------------|--------------|------------------|
| **This only** | Single slot marked as modified | 1 slot update |
| **This & future** | Original series ends, new series created | 1 event update + new event + new slots |
| **All** | Parent event updated, slots inherit | 1 event update + clear slot modifications |

---

## API Design

### Core Endpoints

```
# Calendar CRUD
POST   /api/calendars                    Create new calendar
GET    /api/calendars                    List user's calendars
GET    /api/calendars/{id}               Get calendar details
PUT    /api/calendars/{id}               Update calendar
DELETE /api/calendars/{id}               Delete calendar
POST   /api/calendars/{id}/share         Share with other users

# Event CRUD
POST   /api/calendars/{cal_id}/events           Create event
GET    /api/calendars/{cal_id}/events           List events (with date range)
GET    /api/calendars/{cal_id}/events/{id}      Get event details
PUT    /api/calendars/{cal_id}/events/{id}      Update event
DELETE /api/calendars/{cal_id}/events/{id}      Delete event

# Recurring Event Updates (The 3 scenarios!)
PUT    /api/events/{id}/update-single           Update only this occurrence
PUT    /api/events/{id}/update-future           Update this & all future
PUT    /api/events/{id}/update-all              Update entire series

# Participant Management
POST   /api/events/{id}/participants            Invite participants
DELETE /api/events/{id}/participants/{user_id}  Remove participant
POST   /api/events/{id}/rsvp                    Respond (accept/decline/maybe)
```

### Example: Create a Recurring Event

**Request:**
```json
POST /api/calendars/cal-123/events

{
    "title": "Daily Standup",
    "description": "15-min sync to discuss blockers",
    "start_time": "2024-01-15T10:00:00",
    "end_time": "2024-01-15T10:15:00",
    "timezone": "Asia/Kolkata",
    "visibility": "private",
    "location": {
        "type": "online",
        "platform": "meet",
        "meeting_link": "https://meet.google.com/abc-def-ghi"
    },
    "participants": ["rahul@company.com", "priya@company.com"],
    "recurrence": {
        "frequency": "daily",
        "interval": 1,
        "end_type": "until_date",
        "end_date": "2024-12-31"
    }
}
```

**Response:**
```json
{
    "id": "evt-789",
    "series_id": "series-456",
    "title": "Daily Standup",
    "start_time": "2024-01-15T10:00:00",
    "end_time": "2024-01-15T10:15:00",
    "timezone": "Asia/Kolkata",
    "is_recurring": true,
    "recurrence": {
        "frequency": "daily",
        "interval": 1,
        "end_date": "2024-12-31",
        "total_occurrences": 351
    },
    "participants": [
        {"email": "rahul@company.com", "status": "pending"},
        {"email": "priya@company.com", "status": "pending"}
    ],
    "created_at": "2024-01-10T08:30:00Z"
}
```

### Example: Get Events for a Week

**Request:**
```
GET /api/calendars/cal-123/events?start=2024-01-15&end=2024-01-21&expand=true
```

**Response:**
```json
{
    "events": [
        {
            "id": "slot-001",
            "event_id": "evt-789",
            "title": "Daily Standup",
            "start_time": "2024-01-15T10:00:00+05:30",
            "end_time": "2024-01-15T10:15:00+05:30",
            "is_recurring": true,
            "occurrence_index": 1
        },
        {
            "id": "slot-002",
            "event_id": "evt-789",
            "title": "Daily Standup",
            "start_time": "2024-01-16T10:00:00+05:30",
            "end_time": "2024-01-16T10:15:00+05:30",
            "is_recurring": true,
            "occurrence_index": 2
        },
        {
            "id": "evt-single-001",
            "title": "1:1 with Manager",
            "start_time": "2024-01-17T14:00:00+05:30",
            "end_time": "2024-01-17T15:00:00+05:30",
            "is_recurring": false
        }
        // ... more events
    ],
    "pagination": {
        "total": 12,
        "returned": 12
    }
}
```

---

## Timezone Handling - Critical Complexity!

Timezone bugs are the #1 source of calendar issues. Let's understand why and how to handle them correctly.

### The Core Problem

```
Scenario: Rahul in Mumbai creates a meeting at 10:00 AM

Question: What does Priya in London see?

WRONG approach: Store "10:00 AM"
  → Priya sees "10:00 AM" (should be 4:30 AM!)

RIGHT approach: Store UTC + original timezone
  → Rahul's 10:00 AM IST = 4:30 AM UTC
  → Priya's display converts 4:30 AM UTC → 4:30 AM GMT
```

### Scenario 1: Simple Event (One-time)

```python
# When Rahul creates an event
event = {
    "title": "Team Meeting",
    "local_time": "2024-01-15 10:00",
    "user_timezone": "Asia/Kolkata"  # IST = UTC+5:30
}

# Store in database
stored_event = {
    "title": "Team Meeting",
    "utc_time": "2024-01-15T04:30:00Z",      # Converted to UTC
    "original_timezone": "Asia/Kolkata"       # Preserved for reference
}

# When Priya in London views
display_time = convert_utc_to_local(
    stored_event["utc_time"],
    "Europe/London"  # GMT = UTC+0
)
# Result: "2024-01-15 04:30 AM" (very early morning for her!)
```

### Scenario 2: Recurring Events (The Tricky Part!)

```
Problem: "Daily standup at 10 AM" - what does "10 AM" mean?

Option A: Fixed UTC time
  - Store as 4:30 UTC (10 AM in Mumbai)
  - When India switches to DST (if they ever do), time shifts
  - ❌ User expects 10 AM to stay 10 AM

Option B: Wall clock time + timezone
  - Store "10:00" + "Asia/Kolkata"
  - For each occurrence, calculate: "10:00 in Kolkata on THAT date"
  - ✅ Respects DST changes correctly
```

**Implementation:**

```python
@dataclass
class RecurringEventTime:
    wall_clock_time: time     # "10:00" - what user sees
    timezone: str             # "Asia/Kolkata"

    def get_occurrence_utc(self, date: date) -> datetime:
        """Calculate UTC time for a specific occurrence date"""
        import pytz

        tz = pytz.timezone(self.timezone)

        # Create local datetime for that specific date
        local_dt = datetime.combine(date, self.wall_clock_time)

        # Localize to timezone (handles DST correctly!)
        local_dt = tz.localize(local_dt)

        # Convert to UTC for storage/comparison
        return local_dt.astimezone(pytz.UTC)

# Example
standup = RecurringEventTime(
    wall_clock_time=time(10, 0),  # 10:00 AM
    timezone="America/New_York"
)

# Summer (EDT = UTC-4)
summer_date = date(2024, 7, 15)
print(standup.get_occurrence_utc(summer_date))
# Output: 2024-07-15 14:00:00 UTC

# Winter (EST = UTC-5)
winter_date = date(2024, 1, 15)
print(standup.get_occurrence_utc(winter_date))
# Output: 2024-01-15 15:00:00 UTC

# Note: 1 hour difference due to DST!
```

### Scenario 3: DST Edge Cases

**The "Missing Hour" Problem:**

```
US Spring Forward: March 10, 2024 at 2:00 AM → clocks jump to 3:00 AM
                   2:30 AM DOES NOT EXIST!

What if user has "daily meeting at 2:30 AM"?
```

**The "Duplicate Hour" Problem:**

```
US Fall Back: November 3, 2024 at 2:00 AM → clocks go back to 1:00 AM
              1:30 AM HAPPENS TWICE!

Which 1:30 AM is the meeting?
```

**Solution:**

```python
def handle_dst_edge_cases(wall_time: time, date: date, timezone: str):
    import pytz

    tz = pytz.timezone(timezone)
    local_dt = datetime.combine(date, wall_time)

    try:
        return tz.localize(local_dt)
    except pytz.NonExistentTimeError:
        # Time doesn't exist (spring forward)
        # Move to next valid time (e.g., 2:30 AM → 3:00 AM)
        return tz.localize(local_dt, is_dst=True)
    except pytz.AmbiguousTimeError:
        # Time exists twice (fall back)
        # Pick the first occurrence (DST version)
        return tz.localize(local_dt, is_dst=True)
```

### Scenario 4: All-Day Events (Floating Time)

```
"New Year's Day" should be January 1st in EVERY timezone!

Mumbai: Jan 1, 2024
London: Jan 1, 2024
New York: Jan 1, 2024

NOT: "Jan 1 midnight UTC" (which is Dec 31st in NYC!)
```

**Solution:** Mark as "floating" or "all-day":

```python
@dataclass
class DayEvent:
    title: str
    date: date           # Just the date, no time
    is_floating: bool = True  # Not tied to any timezone

    # No timezone needed - it's the same date everywhere
```

### Best Practices Summary

| Rule | Example |
|------|---------|
| Use IANA timezone names | `"America/New_York"` not `"EST"` |
| Store UTC + original timezone | `utc_time` + `original_timezone` fields |
| For recurring: store wall clock time | `"10:00"` + `"Asia/Kolkata"` |
| Handle DST edge cases explicitly | Check for NonExistentTime, AmbiguousTime |
| All-day events are floating | Just store the date, no timezone |
| API responses: ISO 8601 format | `"2024-01-15T10:00:00+05:30"` |

---

## Edge Cases to Consider

### 1. Conflicting Events

```
User creates "Meeting A" from 10:00-11:00
User creates "Meeting B" from 10:30-11:30

Options:
  A) Block it → "You have a conflict!"
  B) Warn → "This overlaps with Meeting A. Continue?"
  C) Allow → Let users manage their own calendar

Google's approach: C (allow, but show visual overlap)
```

### 2. Cross-Timezone Meetings

```
Organizer in Mumbai schedules "Team Sync" at 10 AM IST
Participant in San Francisco sees it at 9:30 PM PST (previous day!)

Solution: Show warning for "awkward hours" (before 8 AM or after 8 PM)
```

### 3. Event Spanning Multiple Days

```
"Offsite Retreat" from January 15 to January 18

Model as:
  Option A: Multi-day event (single event with date range)
  Option B: Multiple single-day events

Recommendation: Option A with special UI handling
```

### 4. Recurring Event with Exceptions

```
"Every Monday except public holidays"

Implementation:
  - Store list of exception dates
  - When generating slots, skip exception dates
  - Allow manual exception additions
```

### 5. Maximum Recurrence Limits

```
User creates "Forever recurring event"

Problems:
  - Infinite slots to generate
  - Database bloat
  - Performance issues

Solution:
  - Max 730 occurrences (2 years)
  - Or max end date: 5 years from now
  - Background job to extend as time passes
```

### 6. Deleted User's Events

```
User A invites User B to recurring meeting
User B deletes their account

Options:
  - Remove from participants list
  - Keep as "Former Participant"
  - Depends on your privacy requirements
```

### 7. Calendar Deletion

```
User deletes their "Work" calendar with 500 events

Soft delete or hard delete?
  - Soft: Mark as deleted, allow recovery for 30 days
  - Hard: Permanent deletion, free up storage

Also: What about shared calendar? Transfer ownership first?
```

---

## Complete Class Structure (Python)

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, date, time
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

# Enums
class Visibility(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    BUSY = "busy"

class FrequencyType(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class RSVPStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    MAYBE = "maybe"

# Location (ABC pattern)
class LocationInfo(ABC):
    @abstractmethod
    def get_display_string(self) -> str:
        pass

@dataclass
class OnlineLocation(LocationInfo):
    meeting_link: str
    platform: str
    password: Optional[str] = None

    def get_display_string(self) -> str:
        return f"{self.platform.title()} Meeting"

@dataclass
class OfflineLocation(LocationInfo):
    address: str
    room_name: Optional[str] = None
    building: Optional[str] = None

    def get_display_string(self) -> str:
        parts = [self.address]
        if self.room_name:
            parts.append(f"Room {self.room_name}")
        return ", ".join(parts)

# Recurrence
@dataclass
class RecurrenceInfo:
    freq_type: FrequencyType
    interval: int = 1  # Every N days/weeks/months
    days_of_week: List[int] = field(default_factory=list)  # 0=Mon, 6=Sun
    day_of_month: Optional[int] = None
    end_date: Optional[date] = None
    max_occurrences: Optional[int] = None

# Core entities
@dataclass
class User:
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    email: str = ""

@dataclass
class Calendar:
    id: UUID = field(default_factory=uuid4)
    title: str = ""
    owner: User = None
    visibility: Visibility = Visibility.PRIVATE
    shared_with: List[User] = field(default_factory=list)

@dataclass
class TimeEvent:
    id: UUID = field(default_factory=uuid4)
    calendar_id: UUID = None
    title: str = ""
    description: str = ""
    start_time: time = None
    end_time: time = None
    timezone: str = "UTC"
    location_info: Optional[LocationInfo] = None
    visibility: Visibility = Visibility.PRIVATE
    recurrence_info: Optional[RecurrenceInfo] = None
    participants: List[User] = field(default_factory=list)

@dataclass
class TimeSlot:
    id: UUID = field(default_factory=uuid4)
    event_id: UUID = None
    date: date = None
    start_time: datetime = None
    end_time: datetime = None
    is_modified: bool = False
    modified_title: Optional[str] = None
    is_cancelled: bool = False

@dataclass
class DayEvent:
    id: UUID = field(default_factory=uuid4)
    calendar_id: UUID = None
    title: str = ""
    date: date = None
    visibility: Visibility = Visibility.PRIVATE
    recurrence_info: Optional[RecurrenceInfo] = None

@dataclass
class DaySlot:
    id: UUID = field(default_factory=uuid4)
    event_id: UUID = None
    date: date = None
    is_modified: bool = False
    modified_title: Optional[str] = None
    is_cancelled: bool = False
```

---

## Summary

| Topic | Key Takeaways |
|-------|---------------|
| **Class Evolution** | Start simple, extract when needed (LocationInfo ABC, separate Day/Time events) |
| **Slots** | Pre-generate occurrences for fast queries; trade storage for speed |
| **Recurring Updates** | 3 modes: this only (modify slot), this+future (split series), all (update parent) |
| **Timezones** | Store UTC + original timezone; wall clock time for recurring; handle DST edges |
| **API Design** | Separate endpoints for the 3 update modes; expand query param for occurrences |

---

## Further Reading

- [Database Design for Google Calendar: a tutorial](https://kb.databasedesignbook.com/posts/google-calendar/)
- [Google Calendar API Documentation](https://developers.google.com/calendar/api)
- [IANA Timezone Database](https://www.iana.org/time-zones)
- [pytz Library](https://pythonhosted.org/pytz/) for Python timezone handling
