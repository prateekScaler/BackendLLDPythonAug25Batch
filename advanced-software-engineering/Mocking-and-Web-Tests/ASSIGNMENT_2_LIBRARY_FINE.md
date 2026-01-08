# Assignment 2: Library Book Fine Calculator

**Duration**: 15 minutes
**Format**: GitHub Discussion Thread
**No coding required** - Just list the test cases you can think of!

---

## Problem Statement

You are building a library management system. When a member returns a book late, a fine is calculated based on how many days they are overdue.

### Business Rules

```
┌─────────────────────────────────────────────────────────────────┐
│                      FINE CALCULATION RULES                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. GRACE PERIOD: First 2 days after due date = No fine        │
│                                                                 │
│  2. FINE STRUCTURE (after grace period):                        │
│     • Days 1-7 overdue: ₹5 per day                             │
│     • Days 8-14 overdue: ₹10 per day                           │
│     • Days 15+ overdue: ₹20 per day                            │
│                                                                 │
│  3. MAXIMUM FINE: ₹500 (capped)                                 │
│                                                                 │
│  4. LIBRARY CLOSED DAYS: Sundays + National Holidays            │
│     • Closed days are NOT counted as overdue days              │
│     • If due date falls on closed day → Extended to next open  │
│                                                                 │
│  5. BOOK CONDITION:                                             │
│     • Damaged book: Additional ₹100 flat fee                   │
│     • Lost book: Book price + ₹50 processing fee (no late fine)│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Function Signature

```python
def calculate_fine(
    due_date: date,
    return_date: date,
    book_condition: str,  # "good", "damaged", "lost"
    book_price: float
) -> float:
    """
    Calculate the fine for a returned book.

    Args:
        due_date: When the book was due
        return_date: When the book was actually returned
        book_condition: Condition of book on return
        book_price: Original price of the book

    Returns:
        Total fine amount in rupees
    """
    pass
```

### Sample Holidays (2024)

| Date | Holiday |
|------|---------|
| Jan 26 | Republic Day |
| Aug 15 | Independence Day |
| Oct 2 | Gandhi Jayanti |

---

## Your Task

**List ALL the test cases you can think of.**

For each test case, provide:
1. **Test Name** (descriptive)
2. **Input** (due date, return date, condition, price)
3. **Expected Fine**
4. **Why this case is important**

### Example Format

```
Test Case: Book returned on time
Input: Due Jan 10, Returned Jan 10, Condition: good, Price: ₹500
Expected: ₹0
Why: Happy path - no fine for on-time return
```

---

## Hints: Categories to Think About

- **Return timing**: On time, within grace, just after grace, way overdue
- **Fine tiers**: Exactly at tier boundaries (day 7, day 14)
- **Maximum cap**: When does ₹500 cap kick in?
- **Closed days**: Sundays in between, holidays in between, consecutive closed days
- **Due date edge cases**: Due on Sunday, due on holiday
- **Book condition**: Each condition type, damaged + late combo
- **Edge cases**: Same day return, return before due date, leap year Feb 29

---

## Submission Guidelines

Reply to this discussion thread with your test cases.

**Format your response clearly:**

```
### Test Case 1: [Name]
- Input: ...
- Expected: ...
- Why: ...

### Test Case 2: [Name]
- Input: ...
- Expected: ...
- Why: ...
```

---

## Evaluation Criteria

| Criteria | Weight |
|----------|--------|
| **Coverage**: Did you cover all business rules? | 30% |
| **Edge Cases**: Did you think of boundary conditions? | 30% |
| **Combinations**: Did you test rule interactions? | 20% |
| **Clarity**: Are test cases clearly described? | 20% |

**Bonus points** for finding edge cases not listed in the hints!
