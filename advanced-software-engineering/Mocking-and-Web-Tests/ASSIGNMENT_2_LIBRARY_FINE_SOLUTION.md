# Assignment 2 Solution: Library Book Fine Calculator

**Instructor Reference - Do not share with students before assignment is complete!**

---

## Comprehensive Test Cases

### Category 1: No Fine Cases

| # | Test Name | Input | Expected Fine | Rationale |
|---|-----------|-------|---------------|-----------|
| 1 | Returned on due date | Due: Jan 10, Return: Jan 10, Good | ₹0 | On time |
| 2 | Returned early | Due: Jan 15, Return: Jan 10, Good | ₹0 | Before due date |
| 3 | Within grace period (1 day) | Due: Jan 10, Return: Jan 11, Good | ₹0 | Grace period |
| 4 | Within grace period (2 days) | Due: Jan 10, Return: Jan 12, Good | ₹0 | End of grace |

---

### Category 2: First Tier (₹5/day) - Days 1-7 After Grace

| # | Test Name | Input | Expected Fine | Rationale |
|---|-----------|-------|---------------|-----------|
| 5 | First day after grace | Due: Jan 10, Return: Jan 13, Good | ₹5 | 1 day × ₹5 |
| 6 | Middle of first tier | Due: Jan 10, Return: Jan 16, Good | ₹20 | 4 days × ₹5 |
| 7 | Last day of first tier | Due: Jan 10, Return: Jan 19, Good | ₹35 | 7 days × ₹5 |

---

### Category 3: Second Tier (₹10/day) - Days 8-14 After Grace

| # | Test Name | Input | Expected Fine | Rationale |
|---|-----------|-------|---------------|-----------|
| 8 | First day of second tier | Due: Jan 10, Return: Jan 20, Good | ₹45 | 7×₹5 + 1×₹10 |
| 9 | Middle of second tier | Due: Jan 10, Return: Jan 23, Good | ₹75 | 7×₹5 + 4×₹10 |
| 10 | Last day of second tier | Due: Jan 10, Return: Jan 26, Good | ₹105 | 7×₹5 + 7×₹10 |

---

### Category 4: Third Tier (₹20/day) - Days 15+ After Grace

| # | Test Name | Input | Expected Fine | Rationale |
|---|-----------|-------|---------------|-----------|
| 11 | First day of third tier | Due: Jan 10, Return: Jan 27, Good | ₹125 | 7×5 + 7×10 + 1×20 |
| 12 | Deep into third tier | Due: Jan 10, Return: Feb 3, Good | ₹265 | 7×5 + 7×10 + 8×20 |

---

### Category 5: Maximum Cap (₹500)

| # | Test Name | Input | Expected Fine | Rationale |
|---|-----------|-------|---------------|-----------|
| 13 | Exactly at cap | Due: Jan 1, Return: Feb 10, Good | ₹500 | Cap kicks in |
| 14 | Way over cap | Due: Jan 1, Return: Jun 1, Good | ₹500 | Still capped |
| 15 | Just under cap | Calculate exact day for ₹495 | ₹495 | Just before cap |

**Note**: Cap calculation:
- First 7 days: 7 × ₹5 = ₹35
- Next 7 days: 7 × ₹10 = ₹70
- Total for 14 days = ₹105
- Remaining to cap: ₹500 - ₹105 = ₹395
- At ₹20/day: ₹395 ÷ ₹20 = 19.75 days
- Cap hits at day 14 + 20 = day 34 after grace (day 36 after due date)

---

### Category 6: Sunday Not Counted

| # | Test Name | Input | Expected Fine | Rationale |
|---|-----------|-------|---------------|-----------|
| 16 | One Sunday in between | Due: Mon Jan 8, Return: Mon Jan 15, Good | Exclude 1 Sunday | 5 overdue days not 7 |
| 17 | Two Sundays in between | Due: Mon Jan 8, Return: Mon Jan 22, Good | Exclude 2 Sundays | 12 overdue days not 14 |
| 18 | Return on Sunday | Due: Fri Jan 5, Return: Sun Jan 14, Good | Sundays excluded | Count correctly |

---

### Category 7: Holidays Not Counted

| # | Test Name | Input | Expected Fine | Rationale |
|---|-----------|-------|---------------|-----------|
| 19 | One holiday in between | Due: Jan 24, Return: Jan 30 (Jan 26 holiday) | Exclude holiday | 4 days not 6 |
| 20 | Holiday on due date | Due: Jan 26 (holiday), Return: Jan 28 | Extended due | Due becomes Jan 27 |
| 21 | Multiple holidays | Period with 2 holidays | Exclude both | Correct calculation |

---

### Category 8: Sunday + Holiday Combination

| # | Test Name | Input | Expected Fine | Rationale |
|---|-----------|-------|---------------|-----------|
| 22 | Sunday + Holiday same period | Due: Sat Aug 10, Return: Mon Aug 19 (Aug 15 is Thu) | Exclude both | 1 Sunday + 1 holiday |
| 23 | Holiday falls on Sunday | If Oct 2 is Sunday | Count as 1 closed day not 2 | No double counting |

---

### Category 9: Due Date on Closed Day

| # | Test Name | Input | Expected Fine | Rationale |
|---|-----------|-------|---------------|-----------|
| 24 | Due on Sunday | Due: Sun Jan 14, Return: Tue Jan 16 | Due extended to Mon Jan 15 | ₹0 (within grace) |
| 25 | Due on holiday | Due: Jan 26 (Fri holiday), Return: Mon Jan 29 | Due extended to Jan 29 | ₹0 |
| 26 | Due on Sunday before holiday Monday | Due: Sun, Mon is holiday | Due → Tuesday | Extended twice |

---

### Category 10: Book Condition - Damaged

| # | Test Name | Input | Expected Fine | Rationale |
|---|-----------|-------|---------------|-----------|
| 27 | Damaged, on time | Due: Jan 10, Return: Jan 10, Damaged, ₹500 | ₹100 | Flat damage fee |
| 28 | Damaged + late | Due: Jan 10, Return: Jan 15, Damaged | Late fine + ₹100 | Both applied |
| 29 | Damaged + max late | Due: Jan 1, Return: Jun 1, Damaged | ₹500 + ₹100 = ₹600 | Cap + damage |

---

### Category 11: Book Condition - Lost

| # | Test Name | Input | Expected Fine | Rationale |
|---|-----------|-------|---------------|-----------|
| 30 | Lost, on time | Due: Jan 10, Return: Jan 10, Lost, ₹500 | ₹550 | Price + ₹50 |
| 31 | Lost, very late | Due: Jan 1, Return: Jun 1, Lost, ₹500 | ₹550 | No late fine, just price + processing |
| 32 | Lost, expensive book | Due: Jan 10, Return: Jan 20, Lost, ₹2000 | ₹2050 | Price + ₹50 only |

---

### Category 12: Boundary & Edge Cases

| # | Test Name | Input | Expected Fine | Rationale |
|---|-----------|-------|---------------|-----------|
| 33 | Return same day as due (noon) | Due: Jan 10, Return: Jan 10 | ₹0 | Same day = on time |
| 34 | Grace period boundary | Due: Jan 10, Return: Jan 12 at 11:59 PM | ₹0 | Still grace |
| 35 | Just after grace | Due: Jan 10, Return: Jan 13 at 12:00 AM | ₹5 | First fine day |

---

### Category 13: Leap Year

| # | Test Name | Input | Expected Fine | Rationale |
|---|-----------|-------|---------------|-----------|
| 36 | Due on Feb 28, return Mar 2 (leap year) | 2024 | Count Feb 29 | Correct day count |
| 37 | Due on Feb 28, return Mar 2 (non-leap) | 2023 | No Feb 29 | 2 days |
| 38 | Due on Feb 29 | 2024 | Valid due date | Leap year handling |

---

### Category 14: Year Boundary

| # | Test Name | Input | Expected Fine | Rationale |
|---|-----------|-------|---------------|-----------|
| 39 | Due Dec 30, Return Jan 5 | Crosses year | Calculate correctly | Year boundary |
| 40 | Due Dec 25 (holiday), Return Jan 2 | Holiday extension + year boundary | Extended due | Complex case |

---

## Fine Calculation Formula Summary

```python
# Step 1: Adjust due date if it falls on closed day
effective_due_date = next_open_day(due_date)

# Step 2: Calculate raw overdue days
raw_days = return_date - effective_due_date

# Step 3: Subtract closed days (Sundays + holidays)
closed_days = count_sundays(effective_due_date, return_date)
            + count_holidays(effective_due_date, return_date)
overdue_days = raw_days - closed_days - grace_period  # grace = 2

# Step 4: Calculate fine by tier
if overdue_days <= 0:
    fine = 0
elif overdue_days <= 7:
    fine = overdue_days * 5
elif overdue_days <= 14:
    fine = (7 * 5) + ((overdue_days - 7) * 10)
else:
    fine = (7 * 5) + (7 * 10) + ((overdue_days - 14) * 20)

# Step 5: Apply cap
fine = min(fine, 500)

# Step 6: Handle book condition
if condition == "damaged":
    fine += 100
elif condition == "lost":
    fine = book_price + 50  # Replaces all late fines
```

---

## Test Case Count by Category

| Category | Count | Complexity |
|----------|-------|------------|
| No Fine | 4 | Low |
| First Tier | 3 | Low |
| Second Tier | 3 | Medium |
| Third Tier | 2 | Medium |
| Cap | 3 | Medium |
| Sundays | 3 | Medium |
| Holidays | 3 | Medium |
| Sunday + Holiday | 2 | High |
| Due on Closed Day | 3 | High |
| Damaged | 3 | Medium |
| Lost | 3 | Medium |
| Boundaries | 3 | High |
| Leap Year | 3 | Medium |
| Year Boundary | 2 | Medium |

**Total: 40 test cases**

---

## Common Student Mistakes

1. **Forgetting grace period** - Start counting fine from day 3, not day 1
2. **Double-counting Sunday holidays** - If holiday falls on Sunday, count as 1 closed day
3. **Not extending due date** - Due on Sunday means effective due is Monday
4. **Lost book late fine** - Lost = price + processing, NO late fine added
5. **Tier calculation errors** - Days 1-7 is 7 days at ₹5, not 8 days
6. **Cap applies before damage fee** - ₹500 cap + ₹100 damage = ₹600, not ₹500 total
7. **Confusing "after grace" with "after due"** - Grace is 2 days AFTER due date

---

## Grading Rubric

| Score Range | Test Cases Listed | Quality |
|-------------|-------------------|---------|
| 45-50 | 25+ cases | Covers all categories, includes combinations |
| 35-44 | 18-24 cases | Covers most categories, some combinations |
| 25-34 | 12-17 cases | Basic coverage, misses edge cases |
| 15-24 | 6-11 cases | Only obvious cases |
| 0-14 | <6 cases | Incomplete |

### Bonus Points (+5)

- Found an edge case not in this solution
- Clearly categorized test cases
- Identified potential ambiguities in requirements (e.g., "What if book is both damaged AND lost?")
