# Assignment 1: Mutual Fund NAV Date Calculator

**Duration**: 15 minutes
**Format**: GitHub Discussion Thread
**No coding required** - Just list the test cases you can think of!

---

## Problem Statement

You are building a mutual fund investment platform. When a customer places a purchase order, they get units allotted at the **NAV (Net Asset Value)** of a specific date. But the NAV date is **not always** the order date!

### Business Rules

```
┌─────────────────────────────────────────────────────────────────┐
│                    NAV DATE CALCULATION RULES                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. CUT-OFF TIME: 2:00 PM IST                                  │
│     • Order before 2 PM → Same day NAV                         │
│     • Order at/after 2 PM → Next business day NAV              │
│                                                                 │
│  2. BUSINESS DAYS: Monday to Friday only                        │
│     • Saturday/Sunday orders → Next Monday NAV                  │
│                                                                 │
│  3. MARKET HOLIDAYS: NSE holiday calendar applies               │
│     • Holiday orders → Next business day NAV                    │
│                                                                 │
│  4. CONSECUTIVE NON-BUSINESS DAYS:                              │
│     • Friday 3 PM order + Monday holiday → Tuesday NAV          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Function Signature

```python
def calculate_nav_date(order_datetime: datetime) -> date:
    """
    Given an order timestamp, return the NAV date that will be applied.

    Args:
        order_datetime: When the customer placed the order (IST timezone)

    Returns:
        The date whose NAV will be used for unit allotment
    """
    pass
```

### Sample Holiday Calendar (2024)

| Date | Day | Holiday |
|------|-----|---------|
| Jan 26 | Friday | Republic Day |
| Mar 8 | Friday | Maha Shivaratri |
| Mar 25 | Monday | Holi |
| Aug 15 | Thursday | Independence Day |
| Oct 2 | Wednesday | Gandhi Jayanti |
| Nov 1 | Friday | Diwali |
| Dec 25 | Wednesday | Christmas |

---

## Your Task

**List ALL the test cases you can think of.**

For each test case, provide:
1. **Test Name** (descriptive)
2. **Input** (order date & time)
3. **Expected NAV Date**
4. **Why this case is important**

### Example Format

```
Test Case: Order on weekday before cut-off
Input: Monday, Jan 15, 2024, 10:30 AM
Expected: Jan 15, 2024 (same day)
Why: Basic happy path - order within business hours
```

---

## Hints: Categories to Think About

Before you start, consider these dimensions:

- **Time**: Before cut-off, exactly at cut-off, after cut-off, midnight
- **Days**: Weekday, Saturday, Sunday
- **Holidays**: Single holiday, consecutive holidays, holiday + weekend
- **Edge cases**: Year boundaries, month boundaries, leap years
- **Combinations**: Friday 3 PM + Monday holiday, Thursday before long weekend

**Think systematically!** Don't just list random cases.

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
