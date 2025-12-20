# Design Snake & Ladder

- [Design Snake & Ladder](#design-snake--ladder)
  - [Overview](#overview)
  - [Expectations](#expectations)
  - [Requirements Gathering](#requirements-gathering)
  - [Requirements](#requirements)
  - [Use Case Diagrams](#use-case-diagrams)
    - [Actors](#actors)
    - [Use Cases](#use-cases)
  - [Class Diagram](#class-diagram)
  - [Key Design Decisions](#key-design-decisions)
  - [API Design](#api-design)

---

## Overview

Snake and Ladder is a classic board game where players race to reach position 100. The game is played on a 10x10 board (100 cells). Players roll dice and move forward. Landing on a snake's head moves you down to its tail, while landing on a ladder's bottom moves you up to its top.

**Game Rules:**
- 2+ players take turns rolling a single die (1-6)
- Start from position 0 (off the board)
- First to reach exactly position 100 wins
- If roll would take you past 100, you stay in place
- Snakes: Head position → Tail position (move down)
- Ladders: Bottom position → Top position (move up)

```
100 ←─────────────────────────── 91
 ↓                                ↓
81 ─────────────────────────────→ 90
 :          SNAKE ↘               :
61 ─────────────────────────────→ 70
 :               ↘                :
41 ─────────────────→ LADDER ↗ → 50
 :                        ↗      :
21 ─────────────────────────────→ 30
 :                                :
 1 ─────────────────────────────→ 10
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
```

<details>
<summary><strong>Sample clarifying questions</strong></summary>

1. How many players can play? (2-4 typically)
2. Is it a single die or two dice?
3. Do you need exactly 100 to win, or >= 100?
4. Can there be multiple snakes/ladders at different positions?
5. Can a snake and ladder start/end at the same position?
6. Do we need to track game history?
7. Is there a time limit per turn?
8. Do we need to support saving/resuming games?

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

1. The game should support 2-4 players.
2. The board is 10x10 with 100 positions (1-100).
3. Each player starts at position 0 (before the board).
4. Players take turns rolling a single 6-sided die.
5. After rolling, player moves forward by the dice value.
6. If player lands on a snake's head, they slide down to the tail.
7. If player lands on a ladder's bottom, they climb up to the top.
8. First player to reach exactly position 100 wins.
9. If roll would exceed 100, player stays at current position.
10. Game continues until a winner is declared.

</details>

---

## Use Case Diagrams

Are the requirements clear enough to define use cases?
If not, try to think of the actors and their interactions with the system.

### Actors

What would be the actors in this system?

```
1.
2.
```

### Use Cases

What would be the use cases i.e. the interactions between the actors and the system?

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

Add more actors and their use cases as needed.

**Create a use case diagram for the system.**

```



```

---

## Class Diagram

What will be the major classes and their attributes?

```
    Class name
        - Attribute 1
        - Attribute 2
        - Attribute 3
        ...
```

**Think about:**
- What represents the game itself?
- What represents the board?
- How to model Snakes and Ladders? (Are they similar?)
- What represents a player?
- How to model dice?

List down your classes:

```
Class 1:

Class 2:

Class 3:

Class 4:

Class 5:
```

List down the relationships between classes:

```
1.
2.
3.
```

Draw the class diagram:

```




```

---

## Key Design Decisions

Think about these design questions:

**1. Should Snake and Ladder be separate classes or same?**
```
Your thoughts:

```

**2. Should Board know about Snakes/Ladders or should they be separate?**
```
Your thoughts:

```

**3. How would you make Dice extensible (e.g., weighted dice, multiple dice)?**
```
Your thoughts:

```

**4. How would you implement "replay" feature (watch game again)?**
```
Your thoughts:

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

See [HINTS_SNAKE_LADDER.md](./HINTS_SNAKE_LADDER.md) for detailed hints after attempting.
