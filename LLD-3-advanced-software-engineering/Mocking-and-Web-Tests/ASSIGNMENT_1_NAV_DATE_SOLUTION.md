# Assignment 1 Solution: Mutual Fund NAV Date Calculator

**Instructor Reference - Do not share with students before assignment is complete!**

---

## Comprehensive Test Cases

### Category 1: Basic Weekday Cases (Happy Path)

| # | Test Name | Input | Expected NAV Date | Rationale |
|---|-----------|-------|-------------------|-----------|
| 1 | Weekday morning order | Mon Jan 15, 10:30 AM | Jan 15 | Basic case - before cut-off |
| 2 | Weekday just before cut-off | Tue Jan 16, 1:59 PM | Jan 16 | Boundary - 1 minute before |
| 3 | Weekday after cut-off | Wed Jan 17, 3:00 PM | Jan 18 | After cut-off → next day |
| 4 | Weekday late evening | Thu Jan 18, 11:00 PM | Jan 19 | Late order → next day |

---

### Category 2: Cut-off Time Boundary

| # | Test Name | Input | Expected NAV Date | Rationale |
|---|-----------|-------|-------------------|-----------|
| 5 | Exactly at cut-off | Mon Jan 15, 2:00:00 PM | Jan 16 | Edge case - "at or after" means next day |
| 6 | One second before cut-off | Mon Jan 15, 1:59:59 PM | Jan 15 | Just before boundary |
| 7 | One second after cut-off | Mon Jan 15, 2:00:01 PM | Jan 16 | Just after boundary |
| 8 | Midnight order | Tue Jan 16, 12:00 AM | Jan 16 | Start of day - before cut-off |
| 9 | Just before midnight | Mon Jan 15, 11:59 PM | Jan 16 | End of day - after cut-off |

---

### Category 3: Weekend Orders

| # | Test Name | Input | Expected NAV Date | Rationale |
|---|-----------|-------|-------------------|-----------|
| 10 | Saturday morning | Sat Jan 13, 9:00 AM | Jan 15 (Mon) | Weekend → Monday |
| 11 | Saturday afternoon | Sat Jan 13, 3:00 PM | Jan 15 (Mon) | Weekend → Monday (cut-off irrelevant) |
| 12 | Saturday midnight | Sat Jan 13, 11:59 PM | Jan 15 (Mon) | Weekend → Monday |
| 13 | Sunday morning | Sun Jan 14, 10:00 AM | Jan 15 (Mon) | Weekend → Monday |
| 14 | Sunday evening | Sun Jan 14, 8:00 PM | Jan 15 (Mon) | Weekend → Monday |

---

### Category 4: Friday After Cut-off

| # | Test Name | Input | Expected NAV Date | Rationale |
|---|-----------|-------|-------------------|-----------|
| 15 | Friday before cut-off | Fri Jan 12, 1:00 PM | Jan 12 | Normal Friday |
| 16 | Friday after cut-off | Fri Jan 12, 3:00 PM | Jan 15 (Mon) | Skips weekend |
| 17 | Friday exactly at cut-off | Fri Jan 12, 2:00 PM | Jan 15 (Mon) | Boundary + weekend |

---

### Category 5: Single Holiday

| # | Test Name | Input | Expected NAV Date | Rationale |
|---|-----------|-------|-------------------|-----------|
| 18 | Order on holiday morning | Fri Jan 26, 10:00 AM (Republic Day) | Jan 29 (Mon) | Holiday → next business day |
| 19 | Order on holiday evening | Fri Jan 26, 4:00 PM (Republic Day) | Jan 29 (Mon) | Holiday (cut-off irrelevant) |
| 20 | Day before holiday, before cut-off | Thu Jan 25, 1:00 PM | Jan 25 | Normal - before holiday |
| 21 | Day before holiday, after cut-off | Thu Jan 25, 3:00 PM | Jan 29 (Mon) | Next day is holiday → skip to Monday |

---

### Category 6: Holiday + Weekend Combinations

| # | Test Name | Input | Expected NAV Date | Rationale |
|---|-----------|-------|-------------------|-----------|
| 22 | Friday holiday | Fri Mar 8 (Shivaratri), 10:00 AM | Mar 11 (Mon) | Holiday + weekend → Monday |
| 23 | Monday holiday | Mon Mar 25 (Holi), 10:00 AM | Mar 26 (Tue) | Monday holiday → Tuesday |
| 24 | Friday after cut-off + Monday holiday | Fri Mar 22, 3:00 PM | Mar 26 (Tue) | Fri→Mon→Tue (3-day skip) |
| 25 | Thursday after cut-off + Friday holiday | Thu Mar 7, 4:00 PM | Mar 11 (Mon) | Skip Fri+Sat+Sun |

---

### Category 7: Consecutive Holidays

| # | Test Name | Input | Expected NAV Date | Rationale |
|---|-----------|-------|-------------------|-----------|
| 26 | Two consecutive holidays | If Thu-Fri are holidays, Wed 3 PM | Following Monday | Skip Thu+Fri+Sat+Sun |
| 27 | Holiday + Weekend + Holiday | Fri holiday + Mon holiday, Thu 4 PM | Tuesday | Long gap handling |

---

### Category 8: Year Boundary

| # | Test Name | Input | Expected NAV Date | Rationale |
|---|-----------|-------|-------------------|-----------|
| 28 | Dec 31 before cut-off (Tuesday) | Tue Dec 31, 2024, 1:00 PM | Dec 31, 2024 | Year end |
| 29 | Dec 31 after cut-off (Tuesday) | Tue Dec 31, 2024, 3:00 PM | Jan 1, 2025 | Crosses year boundary |
| 30 | Dec 31 Friday after cut-off | Fri Dec 31, 2027, 3:00 PM | Jan 3, 2028 | Year boundary + weekend |
| 31 | New Year's Day order | Wed Jan 1, 2025, 10:00 AM | Jan 2, 2025 | Assuming Jan 1 is holiday |

---

### Category 9: Leap Year

| # | Test Name | Input | Expected NAV Date | Rationale |
|---|-----------|-------|-------------------|-----------|
| 32 | Feb 28 in leap year, after cut-off | Thu Feb 28, 2024, 3:00 PM | Feb 29, 2024 | Leap day exists |
| 33 | Feb 28 in non-leap year, after cut-off | Tue Feb 28, 2023, 3:00 PM | Mar 1, 2023 | No Feb 29 |
| 34 | Feb 29 before cut-off | Thu Feb 29, 2024, 1:00 PM | Feb 29, 2024 | Leap day order |
| 35 | Feb 29 after cut-off | Thu Feb 29, 2024, 3:00 PM | Mar 1, 2024 | Leap day → March |

---

### Category 10: Month Boundaries

| # | Test Name | Input | Expected NAV Date | Rationale |
|---|-----------|-------|-------------------|-----------|
| 36 | Last day of month, after cut-off | Wed Jan 31, 3:00 PM | Feb 1 | Month transition |
| 37 | Last day of 30-day month | Tue Apr 30, 4:00 PM | May 1 | Month transition |
| 38 | Friday month-end + weekend | Fri Mar 29, 3:00 PM | Apr 1 (Mon) | Month + weekend |

---

### Category 11: Edge Cases

| # | Test Name | Input | Expected NAV Date | Rationale |
|---|-----------|-------|-------------------|-----------|
| 39 | Order at exactly midnight transition | Mon Jan 15, 12:00:00 AM | Jan 15 | Day boundary |
| 40 | Multiple consecutive non-business days | Wed before 5-day break | Following Monday | Stress test |
| 41 | DST transition (if applicable) | Around DST change | Correct date | Time zone edge |

---

## Test Case Count by Category

| Category | Count | Complexity |
|----------|-------|------------|
| Basic Weekday | 4 | Low |
| Cut-off Boundary | 5 | Medium |
| Weekend | 5 | Low |
| Friday Cut-off | 3 | Medium |
| Single Holiday | 4 | Medium |
| Holiday + Weekend | 4 | High |
| Consecutive Holidays | 2 | High |
| Year Boundary | 4 | Medium |
| Leap Year | 4 | Medium |
| Month Boundary | 3 | Medium |
| Edge Cases | 3 | High |

**Total: 41 test cases**

---

## Common Student Mistakes

1. **Forgetting Friday after cut-off** - Most miss that this skips entire weekend
2. **Ignoring exact cut-off time** - Is 2:00 PM same day or next?
3. **Not testing holiday + weekend combos** - These compound
4. **Missing leap year** - Feb 29 cases often forgotten
5. **Year boundary** - Dec 31 after cut-off crossing years
6. **Assuming holidays always fall on weekdays** - Saturday holidays still matter for Friday orders

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
- Identified potential ambiguities in requirements
