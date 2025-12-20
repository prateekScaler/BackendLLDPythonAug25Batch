# Design Elevator System

- [Design Elevator System](#design-elevator-system)
  - [Overview](#overview)
  - [Expectations](#expectations)
  - [Requirements Gathering](#requirements-gathering)
  - [Requirements](#requirements)
  - [Use Case Diagrams](#use-case-diagrams)
  - [Class Diagram](#class-diagram)
  - [Key Design Decisions](#key-design-decisions)
  - [API Design](#api-design)

---

## Overview

An elevator system manages one or more elevators in a building to efficiently transport people between floors. Users can request an elevator from any floor and specify their destination. The system must decide which elevator to dispatch and in what order to serve requests.

**Key Components:**
- **External Buttons:** UP/DOWN buttons on each floor
- **Internal Panel:** Floor buttons inside elevator
- **Display:** Shows current floor and direction
- **Elevator Controller:** Brain that manages all elevators

```
Floor 10  [▲]     ┌─────────┐
Floor 9   [▲][▼]  │    ▲    │
Floor 8   [▲][▼]  │  [5]    │  ← Elevator going up, at floor 5
Floor 7   [▲][▼]  │         │
Floor 6   [▲][▼]  └─────────┘
Floor 5   [▲][▼]      ║
Floor 4   [▲][▼]      ║
Floor 3   [▲][▼]  ┌─────────┐
Floor 2   [▲][▼]  │    ▼    │  ← Elevator going down, at floor 3
Floor 1       [▼]  │  [3]    │
                  └─────────┘
```

---

## Expectations

* Code should be functionally correct.
* Code should be modular and readable. Clean and professional level code.
* Code should be extensible and scalable. Means it should be able to accommodate new requirements with minimal changes.
* Code should have good OOP design principles.

---

## Requirements Gathering

What are some questions you would ask to gather requirements?

```
1.
2.
3.
4.
5.
6.
```

<details>
<summary><strong>Sample clarifying questions</strong></summary>

1. How many elevators are in the building?
2. How many floors does the building have?
3. What is the scheduling algorithm to use?
4. Is there a weight limit for elevators?
5. Are there VIP/Express elevators that skip certain floors?
6. Should elevators handle emergency scenarios?
7. Are there floors with restricted access?
8. Do all elevators serve all floors?

</details>

---

## Requirements

What will be 8-10 requirements of the system, according to you?

```
1.
2.
3.
4.
5.
6.
7.
8.
```

<details>
<summary><strong>Click to see the actual requirements</strong></summary>

1. Building has N floors and M elevators.
2. Each floor (except ground and top) has UP and DOWN buttons.
3. Each elevator has buttons for all floors (internal panel).
4. Elevator displays current floor and direction.
5. System should efficiently assign elevator to requests.
6. Elevator should stop at requested floors in optimal order.
7. Multiple passengers can board if going same direction.
8. Elevator has weight/capacity limit.
9. System should minimize wait time for passengers.
10. Handle elevator maintenance mode.

</details>

---

## Use Case Diagrams

### Actors

What would be the actors in this system?

```
1.
2.
3.
```

### Use Cases

#### Actor 1

Name of the actor - ` `

Use cases:
```
1.
2.
3.
4.
```

#### Actor 2

Name of the actor - ` `

Use cases:
```
1.
2.
3.
```

**Create a use case diagram for the system.**

```



```

---

## Class Diagram

What will be the major classes and their attributes?

**Think about:**
- What manages all elevators?
- What represents a single elevator?
- How to represent a floor request vs internal request?
- How to model elevator state (idle, moving up, moving down)?
- What scheduling strategy to use?

List down your classes:

```
Class 1:

Class 2:

Class 3:

Class 4:

Class 5:

Class 6:
```

**Design Questions to Consider:**

1. Should `Request` contain direction or destination?
```
Your answer:
```

2. How does the Controller decide which elevator to assign?
```
Your answer:
```

3. How does an elevator decide which floor to stop at next?
```
Your answer:
```

List down the relationships between classes:

```
1.
2.
3.
4.
```

Draw the class diagram:

```




```

---

## Key Design Decisions

**1. Scheduling Algorithms - Which would you choose?**

| Algorithm | Description | Pros | Cons |
|-----------|-------------|------|------|
| FCFS | First come first serve | Simple | Inefficient |
| SSTF | Shortest seek time first | Fast response | Starvation possible |
| SCAN | Go one direction, then reverse | Fair | Longer wait at ends |
| LOOK | Like SCAN, but reverse when no more requests | Efficient | Complex |

```
Your choice and reasoning:

```

**2. How to handle "going up" passenger on "going down" elevator?**
```
Your answer:

```

**3. How would you add VIP/Emergency mode?**
```
Your answer:

```

---

## API Design

What APIs would you design if this were a backend service?

```
1.
2.
3.
4.
5.
```

---

## Hints

See [HINTS_ELEVATOR.md](./HINTS_ELEVATOR.md) for detailed hints after attempting.
