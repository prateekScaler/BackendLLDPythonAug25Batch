# Design Vending Machine

- [Design Vending Machine](#design-vending-machine)
  - [Overview](#overview)
  - [Expectations](#expectations)
  - [Requirements Gathering](#requirements-gathering)
  - [Requirements](#requirements)
  - [Use Case Diagrams](#use-case-diagrams)
  - [Class Diagram](#class-diagram)
  - [State Machine Design](#state-machine-design)
  - [API Design](#api-design)

---

## Overview

A vending machine dispenses products (snacks, drinks) when a user inserts money and makes a selection. The machine must track inventory, handle payments, dispense products, and return change.

**Physical Components:**
- Product display with slots (A1, A2, B1, B2, etc.)
- Coin/Note acceptor
- Keypad for selection
- Display screen
- Product dispenser
- Change dispenser

```
┌─────────────────────────────────┐
│  ┌─────┬─────┬─────┬─────┐     │
│  │ A1  │ A2  │ A3  │ A4  │     │
│  │ $2  │ $3  │ $2  │ $4  │     │
│  ├─────┼─────┼─────┼─────┤     │
│  │ B1  │ B2  │ B3  │ B4  │     │
│  │ $1  │ $2  │ $3  │ $2  │     │
│  └─────┴─────┴─────┴─────┘     │
│                                 │
│  [Display: Insert Money]        │
│                                 │
│  [1] [2] [3] [A]               │
│  [4] [5] [6] [B]               │
│  [7] [8] [9] [C]               │
│                                 │
│  💰 ──────  🎁 ──────           │
│   Money     Product             │
└─────────────────────────────────┘
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

1. What payment methods are supported? (Coins, Notes, Card, UPI?)
2. Can the machine give change?
3. What happens if product is out of stock after money inserted?
4. Can user cancel and get refund?
5. How is inventory restocked?
6. What denominations of coins/notes are accepted?
7. Is there a maximum amount the machine can hold?
8. What products does it sell? (Single type or multiple?)

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

1. Machine displays available products with prices.
2. User can insert coins/notes.
3. Machine shows current balance.
4. User selects product by code (e.g., A1).
5. If balance >= price and item in stock, dispense product.
6. Return change if balance > price.
7. User can cancel and get refund.
8. Handle out-of-stock scenarios.
9. Admin can restock products.
10. Admin can collect money from machine.

</details>

---

## Use Case Diagrams

### Actors

What would be the actors in this system?

```
1.
2.
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
- What represents the machine itself?
- How to model product slots/inventory?
- How to handle different states (idle, has money, dispensing)?
- How to represent money/payment?

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

## State Machine Design

This problem is perfect for the **State Pattern**!

**What states can the vending machine be in?**

```
1.
2.
3.
4.
```

**What transitions exist between states?**

Draw the state machine:

```




```

**What actions trigger state transitions?**

| Current State | Action | Next State |
|---------------|--------|------------|
| | | |
| | | |
| | | |
| | | |

---

## Key Design Decisions

**1. Should State be implemented as Enum or State Pattern?**
```
Your thoughts:

```

**2. How to handle partial payment?**
```
Your thoughts:

```

**3. How to make change calculation efficient?**
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

See [HINTS_VENDING_MACHINE.md](./HINTS_VENDING_MACHINE.md) for detailed hints after attempting.
