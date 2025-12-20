# Design Library Management System

- [Design Library Management System](#design-library-management-system)
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

A Library Management System helps manage books, members, and book lending operations. It tracks which books are available, who has borrowed what, due dates, fines, and reservations.

**Key Operations:**
- Search and browse books
- Issue books to members
- Return books
- Reserve books
- Track overdue books and fines
- Manage inventory (add/remove books)

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

1. How many copies of each book can the library have?
2. How many books can a member borrow at once?
3. What is the borrowing period? (14 days, 21 days?)
4. How is fine calculated for overdue books?
5. Can a member reserve a book that's currently issued?
6. Are there different membership types?
7. Can books be renewed?
8. Is there a catalog of digital books (e-books)?

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

1. Library has multiple books, each book can have multiple copies.
2. Members can search books by title, author, or ISBN.
3. Members can issue a book if available.
4. Members can return issued books.
5. Members can reserve a book if all copies are issued.
6. Fine is charged for overdue books (per day).
7. Members have a limit on max books they can borrow.
8. Librarian can add/remove books from the system.
9. System tracks issue date, due date, and return date.
10. Members cannot issue new books if they have overdue books or unpaid fines.

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
5.
```

#### Actor 2

Name of the actor - ` `

Use cases:
```
1.
2.
3.
4.
```

**Create a use case diagram for the system.**

```



```

---

## Class Diagram

What will be the major classes and their attributes?

**Critical Question: Book vs BookCopy**
```
Think: If library has 5 copies of "Harry Potter", how do you model it?

Option A: 5 separate Book objects with same ISBN
Option B: 1 Book object with quantity=5
Option C: 1 Book object + 5 BookCopy objects

Your choice and reasoning:

```

**Think about:**
- What represents a book title vs physical copy?
- What represents the issue/loan transaction?
- What tracks reservations?
- How to model member limits?

List down your classes:

```
Class 1:

Class 2:

Class 3:

Class 4:

Class 5:

Class 6:
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

**1. How to handle concurrent reservations?**
```
Scenario: Last copy returned. Members A, B, C all have reservations.
Who gets it?

Your approach:

```

**2. How to calculate fine?**
```
Your formula:

```

**3. How to handle book renewal?**
```
Can member renew? Under what conditions?

Your approach:

```

---

## API Design

What APIs would you design for this system?

```
1.
2.
3.
4.
5.
6.
```

---

## Hints

See [HINTS_LIBRARY.md](./HINTS_LIBRARY.md) for detailed hints after attempting.
