# Splitwise CLI Examples

Complete walkthrough examples for using the Splitwise CLI application.

---

## Example 1: Weekend Trip with Friends

### Scenario
Four friends (Rajesh, Priya, Amit, Sneha) go on a weekend trip to Lonavala. Different people pay for different things.

### Step-by-Step Commands

```bash
# Start the CLI
python cli.py

# 1. Register users (if not using seed data)
splitwise> REGISTER rajesh_s "Rajesh Sharma" rajesh@email.com 9876543210 pass123
splitwise> REGISTER priya_p "Priya Patel" priya@email.com 9876543211 pass123
splitwise> REGISTER amit_k "Amit Kumar" amit@email.com 9876543212 pass123
splitwise> REGISTER sneha_r "Sneha Reddy" sneha@email.com 9876543213 pass123

# 2. Create group for the trip
splitwise> CREATE_GROUP "Lonavala Weekend Trip" 1
✓ Group 'Lonavala Weekend Trip' created successfully! ID: 1

# 3. Add members to the group
splitwise> ADD_MEMBER 1 2 1
✓ Priya Patel added to group 'Lonavala Weekend Trip'

splitwise> ADD_MEMBER 1 3 1
✓ Amit Kumar added to group 'Lonavala Weekend Trip'

splitwise> ADD_MEMBER 1 4 1
✓ Sneha Reddy added to group 'Lonavala Weekend Trip'

# 4. Add expenses

# Day 1: Hotel booking - Rajesh paid ₹8000, split equally
splitwise> ADD_EXPENSE "Hotel Booking" 8000 1 1 1:8000 1:2000,2:2000,3:2000,4:2000
✓ Expense 'Hotel Booking' (₹8000) added successfully in group 'Lonavala Weekend Trip'! ID: 1

# Day 1: Dinner - Priya paid ₹1600, split equally
splitwise> ADD_EXPENSE "Dinner at Resort" 1600 2 1 2:1600 1:400,2:400,3:400,4:400
✓ Expense 'Dinner at Resort' (₹1600) added successfully in group 'Lonavala Weekend Trip'! ID: 2

# Day 2: Breakfast - Amit paid ₹800
splitwise> ADD_EXPENSE "Breakfast" 800 3 1 3:800 1:200,2:200,3:200,4:200
✓ Expense 'Breakfast' (₹800) added successfully in group 'Lonavala Weekend Trip'! ID: 3

# Day 2: Sightseeing cab - Sneha paid ₹1200
splitwise> ADD_EXPENSE "Sightseeing Cab" 1200 4 1 4:1200 1:300,2:300,3:300,4:300
✓ Expense 'Sightseeing Cab' (₹1200) added successfully in group 'Lonavala Weekend Trip'! ID: 4

# Day 2: Lunch - Rajesh and Amit both paid
splitwise> ADD_EXPENSE "Lunch at Hill Station" 2000 1 1 1:1200,3:800 1:500,2:500,3:500,4:500
✓ Expense 'Lunch at Hill Station' (₹2000) added successfully in group 'Lonavala Weekend Trip'! ID: 5

# 5. Check individual balance
splitwise> SHOW_BALANCE 2

============================================================
BALANCE FOR: Priya Patel (@priya_p)
============================================================

  You owe Rajesh Sharma: ₹2000.00
  You owe Amit Kumar: ₹500.00
  You owe Sneha Reddy: ₹300.00
  Rajesh Sharma owes you: ₹400.00

============================================================
TOTAL: You owe ₹2400.00
============================================================

# 6. Check group expenses
splitwise> SHOW_GROUP_EXPENSES 1 1

============================================================
EXPENSES FOR GROUP: Lonavala Weekend Trip
============================================================

[2025-01-15 18:45]
  Description: Lunch at Hill Station
  Total Amount: ₹2000
  Created by: Rajesh Sharma
  Paid by:
    - Rajesh Sharma: ₹1200
    - Amit Kumar: ₹800
  Owed by:
    - Rajesh Sharma: ₹500
    - Priya Patel: ₹500
    - Amit Kumar: ₹500
    - Sneha Reddy: ₹500
------------------------------------------------------------
... (other expenses)

# 7. Settle up the group
splitwise> SETTLE_GROUP 1 1

============================================================
SETTLE-UP FOR GROUP: Lonavala Weekend Trip
============================================================

Current Balances:
  Rajesh Sharma: +₹4200.00 (to receive)
  Amit Kumar: -₹700.00 (to pay)
  Priya Patel: -₹2400.00 (to pay)
  Sneha Reddy: -₹900.00 (to pay)

------------------------------------------------------------

Suggested transactions (3 total):

1. Priya Patel pays ₹2400.00 to Rajesh Sharma
2. Sneha Reddy pays ₹900.00 to Rajesh Sharma
3. Amit Kumar pays ₹700.00 to Rajesh Sharma

============================================================
```

### Summary
- **Total Trip Cost:** ₹13,600
- **Per Person:** ₹3,400
- **Transactions Needed:** Only 3 (instead of potentially many more)

---

## Example 2: Roommates Sharing Expenses

### Scenario
Three roommates (Amit, Sneha, Vikram) sharing an apartment in Mumbai, tracking monthly expenses.

### Commands

```bash
# 1. Create roommate group
splitwise> CREATE_GROUP "Mumbai 3BHK Flat" 3
✓ Group 'Mumbai 3BHK Flat' created successfully! ID: 2

# 2. Add roommates
splitwise> ADD_MEMBER 2 4 3
✓ Sneha Reddy added to group 'Mumbai 3BHK Flat'

splitwise> ADD_MEMBER 2 5 3
✓ Vikram Singh added to group 'Mumbai 3BHK Flat'

# 3. January expenses

# Electricity bill - Amit paid
splitwise> ADD_EXPENSE "January Electricity" 2100 3 2 3:2100 3:700,4:700,5:700
✓ Expense 'January Electricity' (₹2100) added successfully in group 'Mumbai 3BHK Flat'!

# Groceries - Sneha paid
splitwise> ADD_EXPENSE "Monthly Groceries" 4500 4 2 4:4500 3:1500,4:1500,5:1500
✓ Expense 'Monthly Groceries' (₹4500) added successfully in group 'Mumbai 3BHK Flat'!

# Internet - Vikram paid
splitwise> ADD_EXPENSE "WiFi Bill" 999 5 2 5:999 3:333,4:333,5:333
✓ Expense 'WiFi Bill' (₹999) added successfully in group 'Mumbai 3BHK Flat'!

# Maid - All three paid together
splitwise> ADD_EXPENSE "Maid Salary" 3000 3 2 3:1000,4:1000,5:1000 3:1000,4:1000,5:1000
✓ Expense 'Maid Salary' (₹3000) added successfully in group 'Mumbai 3BHK Flat'!

# Gas cylinder - Amit paid
splitwise> ADD_EXPENSE "Gas Cylinder" 900 3 2 3:900 3:300,4:300,5:300
✓ Expense 'Gas Cylinder' (₹900) added successfully in group 'Mumbai 3BHK Flat'!

# 4. Check Sneha's balance
splitwise> SHOW_BALANCE 4

============================================================
BALANCE FOR: Sneha Reddy (@sneha_r)
============================================================

  Amit Kumar owes you: ₹533.00
  Vikram Singh owes you: ₹333.00
  You owe Amit Kumar: ₹1000.00

============================================================
TOTAL: You owe ₹134.00
============================================================

# 5. Settle the group for the month
splitwise> SETTLE_GROUP 2 3

============================================================
SETTLE-UP FOR GROUP: Mumbai 3BHK Flat
============================================================

Current Balances:
  Sneha Reddy: +₹1833.00 (to receive)
  Amit Kumar: +₹1567.00 (to receive)
  Vikram Singh: -₹3400.00 (to pay)

------------------------------------------------------------

Suggested transactions (2 total):

1. Vikram Singh pays ₹1833.00 to Sneha Reddy
2. Vikram Singh pays ₹1567.00 to Amit Kumar

============================================================
```

---

## Example 3: Office Lunch Group

### Scenario
Colleagues having lunch together regularly. Different people pay each time.

### Commands

```bash
# 1. Create office lunch group
splitwise> CREATE_GROUP "Office Lunch Squad" 2
✓ Group 'Office Lunch Squad' created successfully! ID: 3

# 2. Add colleagues
splitwise> ADD_MEMBER 3 1 2
splitwise> ADD_MEMBER 3 5 2

# 3. Week 1 lunches

# Monday - Priya paid at Barbeque Nation
splitwise> ADD_EXPENSE "Monday BBQ Lunch" 1800 2 3 2:1800 1:600,2:600,5:600
✓ Expense 'Monday BBQ Lunch' (₹1800) added successfully!

# Wednesday - Rajesh paid at Subway
splitwise> ADD_EXPENSE "Wednesday Subway" 900 1 3 1:900 1:300,2:300,5:300
✓ Expense 'Wednesday Subway' (₹900) added successfully!

# Friday - Vikram paid at Chinese restaurant
splitwise> ADD_EXPENSE "Friday Chinese Food" 1500 5 3 5:1500 1:500,2:500,5:500
✓ Expense 'Friday Chinese Food' (₹1500) added successfully!

# 4. Coffee break - Only Priya and Rajesh (not a group expense)
splitwise> ADD_EXPENSE "Starbucks Coffee" 450 2 0 2:450 1:225,2:225
✓ Expense 'Starbucks Coffee' (₹450) added successfully!

# 5. Check Rajesh's expenses
splitwise> SHOW_USER_EXPENSES 1

============================================================
EXPENSES FOR: Rajesh Sharma (@rajesh_s)
============================================================

[2025-01-20 16:30]
  Description: Starbucks Coffee
  Total Amount: ₹450
  Paid by:
    - Priya Patel: ₹450
  Owed by:
    - Rajesh Sharma: ₹225
    - Priya Patel: ₹225

[2025-01-20 13:15]
  Description: Friday Chinese Food
  Total Amount: ₹1500
  Group: Office Lunch Squad
  ...

# 6. Settle just Rajesh's personal debts
splitwise> SETTLE_USER 1

============================================================
SETTLE-UP FOR: Rajesh Sharma (@rajesh_s)
============================================================

Suggested transactions (2 total):

1. Rajesh Sharma pays ₹400.00 to Vikram Singh
2. Rajesh Sharma pays ₹325.00 to Priya Patel

============================================================
```

---

## Example 4: Complex Split Scenario

### Scenario
Restaurant bill where people ordered different amounts. Unequal split based on consumption.

### Commands

```bash
# At restaurant - Total bill ₹3000
# Rajesh: ₹1200 (main course + drinks)
# Priya: ₹900 (main course)
# Amit: ₹600 (appetizer only)
# Sneha: ₹300 (just dessert)

# Rajesh paid the entire bill
splitwise> ADD_EXPENSE "Dinner Restaurant" 3000 1 0 1:3000 1:1200,2:900,3:600,4:300
✓ Expense 'Dinner Restaurant' (₹3000) added successfully! ID: 15

# Check who owes what
splitwise> SHOW_BALANCE 1

============================================================
BALANCE FOR: Rajesh Sharma (@rajesh_s)
============================================================

  Priya Patel owes you: ₹900.00
  Amit Kumar owes you: ₹600.00
  Sneha Reddy owes you: ₹300.00

============================================================
TOTAL: You are owed ₹1800.00
============================================================
```

---

## Example 5: Multiple Payers Scenario

### Scenario
Shopping trip where multiple people paid for different items.

### Commands

```bash
# Group shopping for a party
# Rajesh paid ₹2000 for decorations
# Priya paid ₹3000 for food
# Total: ₹5000, split equally among 4 people (₹1250 each)

splitwise> ADD_EXPENSE "Party Shopping" 5000 1 1 1:2000,2:3000 1:1250,2:1250,3:1250,4:1250
✓ Expense 'Party Shopping' (₹5000) added successfully in group 'Lonavala Weekend Trip'!

# Result:
# Rajesh: Paid ₹2000, Owes ₹1250 → Net: +₹750 (to receive)
# Priya: Paid ₹3000, Owes ₹1250 → Net: +₹1750 (to receive)
# Amit: Paid ₹0, Owes ₹1250 → Net: -₹1250 (to pay)
# Sneha: Paid ₹0, Owes ₹1250 → Net: -₹1250 (to pay)
```

---

## Common Patterns

### Equal Split
```bash
# 3 people, one pays, split equally
ADD_EXPENSE "description" 1500 1 0 1:1500 1:500,2:500,3:500
```

### Unequal Split
```bash
# 3 people, different amounts
ADD_EXPENSE "description" 1500 1 0 1:1500 1:600,2:600,3:300
```

### Multiple Payers, Equal Split
```bash
# 2 people paid, 3 people split equally
ADD_EXPENSE "description" 1500 1 0 1:900,2:600 1:500,2:500,3:500
```

### Group Expense
```bash
# In group (group_id=1)
ADD_EXPENSE "description" 1500 1 1 1:1500 1:500,2:500,3:500
```

### Personal Expense (No Group)
```bash
# Not in any group (group_id=0)
ADD_EXPENSE "description" 1500 1 0 1:1500 1:750,2:750
```

---

## Tips & Tricks

1. **Use Quotes for Descriptions:**
   ```bash
   ADD_EXPENSE "Dinner at Beach Shack" 1500 1 0 ...
   ```

2. **Group ID 0 = Personal Expense:**
   ```bash
   # Personal expense between friends
   ADD_EXPENSE "Movie" 600 1 0 1:600 1:300,2:300
   ```

3. **Check Before Settling:**
   ```bash
   # First see who owes what
   SHOW_GROUP_EXPENSES 1 1
   SHOW_BALANCE 1

   # Then settle
   SETTLE_GROUP 1 1
   ```

4. **Validation is Automatic:**
   - Total paid must equal total owed
   - Total must equal expense amount
   - All user IDs must exist
   - You'll get clear error messages if something's wrong

5. **Update User Info:**
   ```bash
   UPDATE_USER 1 phone_number 9876543299
   UPDATE_USER 1 email newemail@example.com
   ```

---

## Error Examples

### Wrong: Totals Don't Match
```bash
splitwise> ADD_EXPENSE "Dinner" 1500 1 0 1:1500 1:500,2:500
❌ Error: Total owed (₹1000) must equal expense amount (₹1500)
```

### Wrong: User Doesn't Exist
```bash
splitwise> ADD_EXPENSE "Dinner" 1500 1 0 1:1500 1:500,99:1000
❌ Error: User with ID 99 not found
```

### Wrong: Not a Group Member
```bash
splitwise> SHOW_GROUP_EXPENSES 1 99
❌ Error: You must be a member of 'Goa Trip' to view its expenses
```

---

