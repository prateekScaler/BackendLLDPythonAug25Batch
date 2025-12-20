# Hints: Elevator System

## Hint 1: Actors

<details>
<summary>Click to reveal</summary>

1. **Passenger** - Requests elevator, selects destination
2. **Building Admin** - Configures system, maintenance mode
3. **System** - Manages elevator assignments

</details>

---

## Hint 2: Two Types of Requests

<details>
<summary>Click to reveal</summary>

**External Request (Hall Call):**
- Made from floor buttons (UP/DOWN)
- Contains: floor number + direction
- User wants to GO somewhere

**Internal Request (Cab Call):**
- Made from inside elevator
- Contains: destination floor
- User IS INSIDE and wants to reach floor

```python
class ExternalRequest:
    floor: int
    direction: Direction  # UP or DOWN

class InternalRequest:
    destination_floor: int
```

</details>

---

## Hint 3: Elevator States

<details>
<summary>Click to reveal</summary>

**State Pattern:**
```
IDLE → MOVING_UP → IDLE
     → MOVING_DOWN → IDLE

class ElevatorState(Enum):
    IDLE = "idle"
    MOVING_UP = "moving_up"
    MOVING_DOWN = "moving_down"
    MAINTENANCE = "maintenance"
```

Elevator behavior changes based on state:
- IDLE: Can go either direction
- MOVING_UP: Only picks up passengers going UP
- MOVING_DOWN: Only picks up passengers going DOWN

</details>

---

## Hint 4: Class Design

<details>
<summary>Click to reveal</summary>

```
┌────────────────────────────┐
│    ElevatorController      │
├────────────────────────────┤
│ - elevators: List[Elevator]│
│ - pending_requests: Queue  │
│ - strategy: ScheduleStrategy│
├────────────────────────────┤
│ + requestElevator(floor, dir)│
│ + assignRequest(request)   │
│ + step() // simulation     │
└────────────────────────────┘
              │
              ▼
┌────────────────────────────┐
│        Elevator            │
├────────────────────────────┤
│ - id                       │
│ - current_floor            │
│ - direction: Direction     │
│ - state: ElevatorState     │
│ - destinations: SortedSet  │
│ - capacity                 │
│ - current_load             │
├────────────────────────────┤
│ + addDestination(floor)    │
│ + move()                   │
│ + openDoors()              │
│ + closeDoors()             │
└────────────────────────────┘

┌────────────────────────────┐
│   ScheduleStrategy (ABC)   │
├────────────────────────────┤
│ + selectElevator(request,  │
│     elevators): Elevator   │
└────────────────────────────┘
         △
    ┌────┴────────┐
    ▼             ▼
┌─────────┐  ┌──────────┐
│  FCFS   │  │  LOOK    │
└─────────┘  └──────────┘
```

</details>

---

## Hint 5: Scheduling - LOOK Algorithm

<details>
<summary>Click to reveal</summary>

**LOOK Algorithm:**
1. Continue in current direction
2. Stop at all requested floors along the way
3. Reverse direction only when no more requests ahead

```python
class Elevator:
    def get_next_floor(self):
        if not self.destinations:
            return None  # Go IDLE

        if self.direction == Direction.UP:
            # Get nearest floor above current
            above = [f for f in self.destinations if f > self.current_floor]
            if above:
                return min(above)
            # No more above, reverse
            self.direction = Direction.DOWN
            return max(self.destinations)

        else:  # DOWN
            below = [f for f in self.destinations if f < self.current_floor]
            if below:
                return max(below)
            self.direction = Direction.UP
            return min(self.destinations)
```

</details>

---

## Hint 6: Selecting Best Elevator

<details>
<summary>Click to reveal</summary>

**Strategy: Nearest Suitable Elevator**

```python
def select_elevator(self, request, elevators):
    suitable = []

    for elevator in elevators:
        if elevator.state == ElevatorState.MAINTENANCE:
            continue

        if elevator.state == ElevatorState.IDLE:
            suitable.append((elevator, abs(elevator.current_floor - request.floor)))

        elif elevator.direction == request.direction:
            # Check if elevator is coming towards this floor
            if (elevator.direction == Direction.UP and
                elevator.current_floor < request.floor):
                suitable.append((elevator, request.floor - elevator.current_floor))

            elif (elevator.direction == Direction.DOWN and
                  elevator.current_floor > request.floor):
                suitable.append((elevator, elevator.current_floor - request.floor))

    if not suitable:
        # All busy going other direction - queue request
        return None

    # Return nearest
    return min(suitable, key=lambda x: x[1])[0]
```

</details>

---

## Hint 7: Elevator Movement Simulation

<details>
<summary>Click to reveal</summary>

```python
class Elevator:
    def step(self):
        """Simulate one time unit"""
        if self.state == ElevatorState.IDLE:
            if self.destinations:
                self._determine_direction()
            return

        next_floor = self.get_next_floor()
        if next_floor is None:
            self.state = ElevatorState.IDLE
            return

        # Move one floor
        if self.direction == Direction.UP:
            self.current_floor += 1
        else:
            self.current_floor -= 1

        # Check if we should stop
        if self.current_floor in self.destinations:
            self.destinations.remove(self.current_floor)
            self.open_doors()
            # Passengers board/exit
            self.close_doors()
```

</details>

---

## Hint 8: Full Class Diagram

<details>
<summary>Click to reveal</summary>

```
┌─────────────────────────────────────────────────────────┐
│                   ElevatorController                     │
├─────────────────────────────────────────────────────────┤
│ - elevators: List[Elevator]                             │
│ - floors: int                                            │
│ - strategy: ScheduleStrategy                             │
├─────────────────────────────────────────────────────────┤
│ + requestElevator(floor, direction): void                │
│ + selectFloor(elevatorId, floor): void                   │
│ + step(): void  // advance simulation                    │
│ + getStatus(): List[ElevatorStatus]                      │
└─────────────────────────────────────────────────────────┘
              │
              │ manages
              ▼
┌─────────────────────────────────────────────────────────┐
│                      Elevator                            │
├─────────────────────────────────────────────────────────┤
│ - id: int                                                │
│ - current_floor: int                                     │
│ - direction: Direction                                   │
│ - state: ElevatorState                                   │
│ - destinations: SortedSet[int]                           │
│ - capacity: int                                          │
├─────────────────────────────────────────────────────────┤
│ + addDestination(floor): void                            │
│ + step(): void                                           │
│ + canPickup(floor, direction): bool                      │
└─────────────────────────────────────────────────────────┘

┌──────────────────┐    ┌──────────────────┐
│   Direction      │    │  ElevatorState   │
├──────────────────┤    ├──────────────────┤
│ UP               │    │ IDLE             │
│ DOWN             │    │ MOVING_UP        │
│ NONE             │    │ MOVING_DOWN      │
└──────────────────┘    │ MAINTENANCE      │
                        └──────────────────┘

┌─────────────────────────────────────────────────────────┐
│                 ScheduleStrategy (ABC)                   │
├─────────────────────────────────────────────────────────┤
│ + selectElevator(request, elevators): Elevator          │
└─────────────────────────────────────────────────────────┘
              △
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐
│ FCFS   │ │ LOOK   │ │Nearest │
│Strategy│ │Strategy│ │Strategy│
└────────┘ └────────┘ └────────┘
```

</details>

---

## Hint 9: API Design

<details>
<summary>Click to reveal</summary>

```
# External request (hall call)
POST /elevator/request
{
    "floor": 5,
    "direction": "UP"
}
Response: { "assigned_elevator": 2 }

# Internal request (cab call)
POST /elevator/{id}/select-floor
{
    "floor": 10
}

# Get system status
GET /elevator/status
Response: {
    "elevators": [
        {"id": 1, "floor": 5, "direction": "UP", "destinations": [7, 10]},
        {"id": 2, "floor": 3, "direction": "DOWN", "destinations": [1]}
    ]
}

# Maintenance mode
PUT /elevator/{id}/maintenance
{
    "enabled": true
}
```

</details>

---

## Common Mistakes to Avoid

1. **Not separating external vs internal requests** - They have different data
2. **Elevator knows about Controller** - Keep dependencies one-way
3. **No idle state handling** - Elevator must know when to stop
4. **Ignoring direction in scheduling** - Don't pick "going down" elevator for "going up" request
5. **Capacity not checked** - Don't overload elevator
