# Splitwise CLI - Command Usage Guide

A comprehensive guide showing the proper order and flow of commands in the Splitwise CLI application.

---

## Table of Contents

1. [Command Dependencies](#command-dependencies)
2. [Getting Started Tutorial](#getting-started-tutorial)
3. [Common Workflows](#common-workflows)
4. [Command Reference](#command-reference)
5. [Troubleshooting](#troubleshooting)

---

## Command Dependencies

Understanding which commands depend on others is crucial for using the CLI effectively.

### Dependency Chain

```
REGISTER (or use seed data)
    ↓
CREATE_GROUP
    ↓
ADD_MEMBER
    ↓
ADD_EXPENSE
    ↓
SHOW_BALANCE / SHOW_GROUP_EXPENSES
    ↓
SETTLE_USER / SETTLE_GROUP
```

### What You Need Before Each Command

| Command | Prerequisites | Example |
|---------|--------------|---------|
| `REGISTER` | None | Can run anytime |
| `CREATE_GROUP` | User must exist | Need creator's user_id |
| `ADD_MEMBER` | Group must exist, both users must exist | Need group_id and user_ids |
| `ADD_EXPENSE` | All users involved must exist, group must exist (if group expense) | Need user_ids, optional group_id |
| `SHOW_BALANCE` | User must exist | Need user_id |
| `SHOW_USER_EXPENSES` | User must exist | Need user_id |
| `SHOW_GROUP_EXPENSES` | Group must exist, user must be member | Need group_id and user_id |
| `SETTLE_USER` | User must exist, user must have balances | Need user_id |
| `SETTLE_GROUP` | Group must exist, user must be member | Need group_id and user_id |
| `UPDATE_USER` | User must exist | Need user_id |

---

## Getting Started Tutorial

This section walks you through your first time using Splitwise CLI from scratch.

### Step 1: Start the Application

```bash
# Make sure you're in the project directory
cd /path/to/class-16-code-splitwise

# Option A: Use seed data (recommended for first time)
python manage.py seed_data
python cli.py

# Option B: Start fresh and register users manually
python cli.py
```

### Step 2: Check Available Users (If Using Seed Data)

After running seed_data, you have these users:

| ID | Name | Username | Password |
|----|------|----------|----------|
| 1 | Rajesh Sharma | rajesh_sharma | pass123 |
| 2 | Priya Patel | priya_patel | pass123 |
| 3 | Amit Kumar | amit_kumar | pass123 |
| 4 | Sneha Reddy | sneha_reddy | pass123 |
| 5 | Vikram Singh | vikram_singh | pass123 |

### Step 3: Create Your First Group

Let's say Rajesh (user_id=1) wants to create a group for a weekend trip:

```bash
splitwise> CREATE_GROUP "Weekend Getaway" 1
✓ Group 'Weekend Getaway' created successfully! ID: 4
```

**Note the Group ID**: You'll need this (4 in this example) for subsequent commands.

### Step 4: Add Members to the Group

Now add Priya (user_id=2) and Amit (user_id=3) to the group:

```bash
# Add Priya
splitwise> ADD_MEMBER 4 2 1
✓ Priya Patel added to group 'Weekend Getaway'

# Add Amit
splitwise> ADD_MEMBER 4 3 1
✓ Amit Kumar added to group 'Weekend Getaway'
```

**Format**: `ADD_MEMBER <group_id> <user_to_add_id> <creator_id>`

### Step 5: Add Your First Expense

Rajesh paid ₹3000 for hotel booking, split equally among 3 people (₹1000 each):

```bash
splitwise> ADD_EXPENSE "Hotel Booking" 3000 1 4 1:3000 1:1000,2:1000,3:1000
✓ Expense 'Hotel Booking' (₹3000) added successfully in group 'Weekend Getaway'! ID: 10
```

**Format**: `ADD_EXPENSE "description" <total_amount> <creator_id> <group_id> <payers> <owers>`

**Breaking down the command**:
- `"Hotel Booking"` - Description (use quotes for multi-word)
- `3000` - Total amount in rupees
- `1` - Created by Rajesh (user_id=1)
- `4` - In group with ID 4
- `1:3000` - Rajesh (user_id=1) paid ₹3000
- `1:1000,2:1000,3:1000` - All three owe ₹1000 each

### Step 6: Check Balances

Let's see who owes whom:

```bash
# Check Priya's balance
splitwise> SHOW_BALANCE 2

============================================================
BALANCE FOR: Priya Patel (@priya_patel)
============================================================

  You owe Rajesh Sharma: ₹1000.00

============================================================
TOTAL: You owe ₹1000.00
============================================================
```

### Step 7: View Group Expenses

See all expenses in the group:

```bash
splitwise> SHOW_GROUP_EXPENSES 4 1

============================================================
EXPENSES FOR GROUP: Weekend Getaway
============================================================

[2025-01-15 14:30]
  Description: Hotel Booking
  Total Amount: ₹3000
  Created by: Rajesh Sharma
  Paid by:
    - Rajesh Sharma: ₹3000
  Owed by:
    - Rajesh Sharma: ₹1000
    - Priya Patel: ₹1000
    - Amit Kumar: ₹1000
------------------------------------------------------------
```

### Step 8: Settle Up

After the trip, settle all debts in the group:

```bash
splitwise> SETTLE_GROUP 4 1

============================================================
SETTLE-UP FOR GROUP: Weekend Getaway
============================================================

Current Balances:
  Rajesh Sharma: +₹2000.00 (to receive)
  Priya Patel: -₹1000.00 (to pay)
  Amit Kumar: -₹1000.00 (to pay)

------------------------------------------------------------

Suggested transactions (2 total):

1. Priya Patel pays ₹1000.00 to Rajesh Sharma
2. Amit Kumar pays ₹1000.00 to Rajesh Sharma

============================================================
```

---

## Common Workflows

### Workflow 1: Weekend Trip with Friends

**Scenario**: You and 3 friends are going on a trip. Different people will pay for different things.

```bash
# 1. Create group (assuming you're user_id=1)
splitwise> CREATE_GROUP "Mumbai Trip" 1

# 2. Add friends (assuming they're user_id 2, 3, 4)
splitwise> ADD_MEMBER 1 2 1
splitwise> ADD_MEMBER 1 3 1
splitwise> ADD_MEMBER 1 4 1

# 3. You pay for hotel
splitwise> ADD_EXPENSE "Hotel" 8000 1 1 1:8000 1:2000,2:2000,3:2000,4:2000

# 4. Friend 2 pays for dinner
splitwise> ADD_EXPENSE "Group Dinner" 2000 2 1 2:2000 1:500,2:500,3:500,4:500

# 5. Friend 3 pays for cab
splitwise> ADD_EXPENSE "Cab to Airport" 800 3 1 3:800 1:200,2:200,3:200,4:200

# 6. Check your balance
splitwise> SHOW_BALANCE 1

# 7. At the end of trip, settle up
splitwise> SETTLE_GROUP 1 1
```

### Workflow 2: Roommates Monthly Expenses

**Scenario**: You and your roommate share an apartment and split utilities equally.

```bash
# 1. Create roommates group
splitwise> CREATE_GROUP "Flat 3B Roommates" 1

# 2. Add roommate
splitwise> ADD_MEMBER 1 2 1

# 3. You pay electricity bill
splitwise> ADD_EXPENSE "January Electricity" 1500 1 1 1:1500 1:750,2:750

# 4. Roommate pays internet bill
splitwise> ADD_EXPENSE "January WiFi" 999 2 1 2:999 1:499.50,2:499.50

# 5. You both pay for groceries together
splitwise> ADD_EXPENSE "Weekly Groceries" 2000 1 1 1:1200,2:800 1:1000,2:1000

# 6. Check who owes what
splitwise> SHOW_BALANCE 1
splitwise> SHOW_BALANCE 2

# 7. At month end, settle up
splitwise> SETTLE_GROUP 1 1
```

### Workflow 3: Office Lunch Group

**Scenario**: Your team has lunch together regularly. Different people pay each time.

```bash
# 1. Create lunch group
splitwise> CREATE_GROUP "Team Lunch Squad" 1

# 2. Add team members
splitwise> ADD_MEMBER 1 2 1
splitwise> ADD_MEMBER 1 3 1

# 3. Monday - You paid at restaurant
splitwise> ADD_EXPENSE "Monday Lunch" 900 1 1 1:900 1:300,2:300,3:300

# 4. Wednesday - Colleague 2 paid at cafe
splitwise> ADD_EXPENSE "Wednesday Cafe" 600 2 1 2:600 1:200,2:200,3:200

# 5. Friday - Colleague 3 paid at food court
splitwise> ADD_EXPENSE "Friday Food" 750 3 1 3:750 1:250,2:250,3:250

# 6. At end of month, settle
splitwise> SETTLE_GROUP 1 1
```

### Workflow 4: Personal Expense (Not in a Group)

**Scenario**: You and a friend went to a movie, not related to any group.

```bash
# You paid for tickets, split equally
splitwise> ADD_EXPENSE "Movie Tickets" 600 1 0 1:600 1:300,2:300

# Check your personal balance with that friend
splitwise> SHOW_BALANCE 1

# Settle just your personal debts
splitwise> SETTLE_USER 1
```

**Note**: `group_id = 0` means it's a personal expense, not associated with any group.

### Workflow 5: Complex Restaurant Bill

**Scenario**: Restaurant bill where people ordered different amounts (unequal split).

```bash
# Total bill ₹3000
# You ordered ₹1200 worth
# Friend 2 ordered ₹1000 worth
# Friend 3 ordered ₹800 worth
# You paid the entire bill

splitwise> ADD_EXPENSE "Dinner at Taj" 3000 1 0 1:3000 1:1200,2:1000,3:800

# Now check who owes you
splitwise> SHOW_BALANCE 1
```

### Workflow 6: Multiple People Paid

**Scenario**: Shopping trip where multiple people paid for different items.

```bash
# Party shopping:
# You paid ₹2000 for decorations
# Friend 2 paid ₹3000 for food
# Total ₹5000, split equally among 4 people (₹1250 each)

splitwise> ADD_EXPENSE "Party Supplies" 5000 1 1 1:2000,2:3000 1:1250,2:1250,3:1250,4:1250

# Result:
# You: Paid ₹2000, Owe ₹1250 → Net: +₹750 (others owe you)
# Friend 2: Paid ₹3000, Owe ₹1250 → Net: +₹1750 (others owe them)
# Friend 3: Paid ₹0, Owe ₹1250 → Net: -₹1250 (owes)
# Friend 4: Paid ₹0, Owe ₹1250 → Net: -₹1250 (owes)
```

---

## Command Reference

Quick reference for all available commands.

### User Management

#### REGISTER - Create a New User
```bash
REGISTER <username> "<full_name>" <email> <phone> <password>
```
**Example**:
```bash
splitwise> REGISTER john_doe "John Doe" john@email.com 9876543210 pass123
```

#### UPDATE_USER - Update User Information
```bash
UPDATE_USER <user_id> <field> <new_value>
```
**Fields**: `name`, `email`, `phone_number`, `password`

**Examples**:
```bash
splitwise> UPDATE_USER 1 email newemail@example.com
splitwise> UPDATE_USER 1 phone_number 9876543299
splitwise> UPDATE_USER 1 password newpass456
```

### Group Management

#### CREATE_GROUP - Create a New Group
```bash
CREATE_GROUP "<group_name>" <creator_user_id>
```
**Example**:
```bash
splitwise> CREATE_GROUP "Trip to Kerala" 1
✓ Group 'Trip to Kerala' created successfully! ID: 5
```

#### ADD_MEMBER - Add User to Group
```bash
ADD_MEMBER <group_id> <user_id_to_add> <creator_user_id>
```
**Example**:
```bash
splitwise> ADD_MEMBER 5 2 1
```
**Note**: Only the group creator can add members.

#### REMOVE_MEMBER - Remove User from Group
```bash
REMOVE_MEMBER <group_id> <user_id_to_remove> <creator_user_id>
```
**Example**:
```bash
splitwise> REMOVE_MEMBER 5 2 1
```
**Note**: Only the group creator can remove members.

### Expense Management

#### ADD_EXPENSE - Add a New Expense
```bash
ADD_EXPENSE "<description>" <amount> <creator_id> <group_id> <payers> <owers>
```

**Payers format**: `user_id:amount,user_id:amount,...`
**Owers format**: `user_id:amount,user_id:amount,...`

**Examples**:

**Equal split (one payer)**:
```bash
splitwise> ADD_EXPENSE "Pizza" 1200 1 0 1:1200 1:400,2:400,3:400
```

**Unequal split**:
```bash
splitwise> ADD_EXPENSE "Restaurant" 2000 1 0 1:2000 1:800,2:700,3:500
```

**Multiple payers, equal split**:
```bash
splitwise> ADD_EXPENSE "Shopping" 3000 1 1 1:2000,2:1000 1:1000,2:1000,3:1000
```

**Personal expense (no group)**:
```bash
splitwise> ADD_EXPENSE "Movie" 500 1 0 1:500 1:250,2:250
```
**Note**: Use `group_id = 0` for personal expenses not in any group.

**Group expense**:
```bash
splitwise> ADD_EXPENSE "Hotel" 6000 1 5 1:6000 1:2000,2:2000,3:2000
```

### Viewing Information

#### SHOW_BALANCE - Show User's Balance
```bash
SHOW_BALANCE <user_id>
```
**Example**:
```bash
splitwise> SHOW_BALANCE 1
```
Shows all people the user owes money to, and all people who owe the user money.

#### SHOW_USER_EXPENSES - Show All User's Expenses
```bash
SHOW_USER_EXPENSES <user_id>
```
**Example**:
```bash
splitwise> SHOW_USER_EXPENSES 1
```
Shows all expenses the user is involved in (both group and personal).

#### SHOW_GROUP_EXPENSES - Show All Group's Expenses
```bash
SHOW_GROUP_EXPENSES <group_id> <user_id>
```
**Example**:
```bash
splitwise> SHOW_GROUP_EXPENSES 5 1
```
**Note**: User must be a member of the group to view its expenses.

### Settlement

#### SETTLE_USER - Settle User's Debts
```bash
SETTLE_USER <user_id>
```
**Example**:
```bash
splitwise> SETTLE_USER 1
```
Shows optimized transactions to settle all of the user's debts (both group and personal).

#### SETTLE_GROUP - Settle Group's Debts
```bash
SETTLE_GROUP <group_id> <user_id>
```
**Example**:
```bash
splitwise> SETTLE_GROUP 5 1
```
Shows optimized transactions to settle all debts within the group.
**Note**: User must be a member of the group.

### Utility Commands

#### HELP - Show All Commands
```bash
HELP
```
Shows a list of all available commands with their formats.

#### EXIT - Exit the Application
```bash
EXIT
```
Exits the Splitwise CLI application.

---

## Troubleshooting

### Common Errors and Solutions

#### Error: "User with ID X not found"

**Cause**: The user ID you're using doesn't exist in the database.

**Solutions**:
1. If using seed data, make sure you ran `python manage.py seed_data` successfully
2. User IDs from seed data are 1-5
3. Check if you need to register the user first with `REGISTER`

**Example**:
```bash
# Wrong
splitwise> SHOW_BALANCE 99
❌ Error: User with ID 99 not found

# Right - use existing user IDs
splitwise> SHOW_BALANCE 1
```

---

#### Error: "Group with ID X not found"

**Cause**: The group ID you're using doesn't exist.

**Solutions**:
1. Create the group first with `CREATE_GROUP`
2. Note the group ID returned when you create it
3. If using seed data, group IDs are 1-3

**Example**:
```bash
# Wrong - group doesn't exist yet
splitwise> ADD_MEMBER 99 2 1
❌ Error: Group with ID 99 not found

# Right - create group first
splitwise> CREATE_GROUP "My Group" 1
✓ Group 'My Group' created successfully! ID: 4

splitwise> ADD_MEMBER 4 2 1
✓ User added successfully
```

---

#### Error: "Total owed (₹X) must equal expense amount (₹Y)"

**Cause**: The amounts in the "owers" part don't add up to the total expense amount.

**Solutions**:
1. Make sure all owers' amounts sum to the total amount
2. Use decimals if needed (e.g., 333.33 instead of 333)

**Example**:
```bash
# Wrong - owers sum to ₹1000, but total is ₹1500
splitwise> ADD_EXPENSE "Dinner" 1500 1 0 1:1500 1:500,2:500
❌ Error: Total owed (₹1000) must equal expense amount (₹1500)

# Right - owers sum to ₹1500
splitwise> ADD_EXPENSE "Dinner" 1500 1 0 1:1500 1:500,2:500,3:500
✓ Expense added successfully
```

---

#### Error: "Total paid (₹X) must equal expense amount (₹Y)"

**Cause**: The amounts in the "payers" part don't add up to the total expense amount.

**Solutions**:
1. Make sure all payers' amounts sum to the total amount
2. If one person paid everything, their amount should equal the total

**Example**:
```bash
# Wrong - payer paid ₹1000, but total is ₹1500
splitwise> ADD_EXPENSE "Dinner" 1500 1 0 1:1000 1:500,2:500,3:500
❌ Error: Total paid (₹1000) must equal expense amount (₹1500)

# Right - payer amount matches total
splitwise> ADD_EXPENSE "Dinner" 1500 1 0 1:1500 1:500,2:500,3:500
✓ Expense added successfully
```

---

#### Error: "You must be a member of 'X' to view its expenses"

**Cause**: You're trying to view group expenses or settle a group you're not a member of.

**Solutions**:
1. Make sure the user_id you're using is a member of the group
2. Add yourself to the group first with `ADD_MEMBER`

**Example**:
```bash
# Wrong - user 5 is not a member of group 1
splitwise> SHOW_GROUP_EXPENSES 1 5
❌ Error: You must be a member of 'Goa Trip' to view its expenses

# Right - user 1 is a member
splitwise> SHOW_GROUP_EXPENSES 1 1
[Shows expenses]
```

---

#### Error: "Only the group creator can add/remove members"

**Cause**: You're trying to add or remove members using a user_id that's not the group creator.

**Solutions**:
1. Use the creator's user_id in the command
2. Check who created the group (shown in group information)

**Example**:
```bash
# Group 1 was created by user 1
# Wrong - user 2 trying to add member
splitwise> ADD_MEMBER 1 3 2
❌ Error: Only the group creator can add members

# Right - creator (user 1) adding member
splitwise> ADD_MEMBER 1 3 1
✓ User added successfully
```

---

#### Error: "Database tables not found"

**Cause**: Migrations haven't been run.

**Solutions**:
```bash
# Run migrations to create database tables
python manage.py makemigrations
python manage.py migrate
```

---

#### Error: "User IDs starting from 6 instead of 1"

**Cause**: Seed data was run multiple times without clearing previous data.

**Solutions**:
```bash
# The seed_data command now handles this automatically
# Just run it again - it will clear old data and reset IDs
python manage.py seed_data
```

---

### Tips for Avoiding Errors

1. **Always note the IDs returned**: When you create a group or user, note the ID - you'll need it later.

2. **Use quotes for descriptions**: If your description has spaces, wrap it in quotes.
   ```bash
   # Wrong
   splitwise> ADD_EXPENSE Hotel Booking 3000 ...

   # Right
   splitwise> ADD_EXPENSE "Hotel Booking" 3000 ...
   ```

3. **Double-check your math**: Make sure payers' amounts and owers' amounts both sum to the total.

4. **Personal expenses use group_id=0**: If it's not a group expense, use 0 for group_id.
   ```bash
   # Personal expense between two friends
   splitwise> ADD_EXPENSE "Coffee" 200 1 0 1:200 1:100,2:100
   ```

5. **Start with seed data**: For your first time, use seed data to have users and groups ready.
   ```bash
   python manage.py seed_data
   python cli.py
   ```

6. **Check balances before settling**: Always run `SHOW_BALANCE` or `SHOW_GROUP_EXPENSES` before settling to verify everything is correct.

---

## Quick Start Cheat Sheet

### First Time Setup
```bash
# 1. Setup database
python manage.py makemigrations
python manage.py migrate

# 2. Load sample data
python manage.py seed_data

# 3. Start CLI
python cli.py
```

### Basic Flow
```bash
# 1. Create group
CREATE_GROUP "Group Name" <creator_id>

# 2. Add members
ADD_MEMBER <group_id> <user_id> <creator_id>

# 3. Add expense
ADD_EXPENSE "Description" <amount> <creator_id> <group_id> <payers> <owers>

# 4. Check balance
SHOW_BALANCE <user_id>

# 5. Settle up
SETTLE_GROUP <group_id> <user_id>
```

### Common Patterns

**Equal split (3 people)**:
```bash
ADD_EXPENSE "Description" 1500 1 0 1:1500 1:500,2:500,3:500
```

**Unequal split**:
```bash
ADD_EXPENSE "Description" 2000 1 0 1:2000 1:800,2:700,3:500
```

**Multiple payers**:
```bash
ADD_EXPENSE "Description" 3000 1 0 1:2000,2:1000 1:1000,2:1000,3:1000
```

**Personal expense (no group)**:
```bash
ADD_EXPENSE "Description" 500 1 0 1:500 1:250,2:250
```

---

## Advanced Usage

### Scenario: Complex Trip with Multiple Days

Day-by-day expense tracking for a 3-day trip:

```bash
# Day 1: Travel
splitwise> ADD_EXPENSE "Flight Tickets" 12000 1 1 1:12000 1:4000,2:4000,3:4000
splitwise> ADD_EXPENSE "Airport Cab" 800 2 1 2:800 1:266.67,2:266.67,3:266.66

# Day 2: Accommodation and Food
splitwise> ADD_EXPENSE "Hotel Night 1" 6000 1 1 1:6000 1:2000,2:2000,3:2000
splitwise> ADD_EXPENSE "Breakfast" 600 3 1 3:600 1:200,2:200,3:200
splitwise> ADD_EXPENSE "Lunch" 1500 2 1 2:1500 1:500,2:500,3:500
splitwise> ADD_EXPENSE "Dinner" 2400 1 1 1:2400 1:800,2:800,3:800

# Day 3: Activities and Return
splitwise> ADD_EXPENSE "Sightseeing Tour" 3000 3 1 3:3000 1:1000,2:1000,3:1000
splitwise> ADD_EXPENSE "Lunch" 1200 1 1 1:1200 1:400,2:400,3:400
splitwise> ADD_EXPENSE "Return Cab" 900 2 1 2:900 1:300,2:300,3:300

# Check individual balances
splitwise> SHOW_BALANCE 1
splitwise> SHOW_BALANCE 2
splitwise> SHOW_BALANCE 3

# View all trip expenses
splitwise> SHOW_GROUP_EXPENSES 1 1

# Final settlement
splitwise> SETTLE_GROUP 1 1
```

### Scenario: Monthly Roommate Expenses

Track all monthly expenses and settle at month end:

```bash
# Week 1
splitwise> ADD_EXPENSE "Groceries Week 1" 2000 1 1 1:2000 1:1000,2:1000
splitwise> ADD_EXPENSE "Electricity Bill" 1500 2 1 2:1500 1:750,2:750

# Week 2
splitwise> ADD_EXPENSE "WiFi Bill" 999 1 1 1:999 1:499.50,2:499.50
splitwise> ADD_EXPENSE "Groceries Week 2" 1800 2 1 2:1800 1:900,2:900

# Week 3
splitwise> ADD_EXPENSE "Gas Cylinder" 900 1 1 1:900 1:450,2:450
splitwise> ADD_EXPENSE "Maid Salary" 2000 1 1 1:1000,2:1000 1:1000,2:1000

# Week 4
splitwise> ADD_EXPENSE "Groceries Week 3" 2200 2 1 2:2200 1:1100,2:1100
splitwise> ADD_EXPENSE "Water Bill" 300 1 1 1:300 1:150,2:150

# Month end settlement
splitwise> SETTLE_GROUP 1 1
```

---

## Summary

**Remember these key principles**:

1. **Order matters**: Create users → Create groups → Add members → Add expenses → Settle
2. **Note the IDs**: Always note the ID returned when creating users/groups
3. **Math must be exact**: Payers and owers must both sum to the total amount
4. **Use group_id=0** for personal expenses not in a group
5. **Check before settling**: Always view balances/expenses before settling
6. **Start with seed data**: Use `python manage.py seed_data` for quick testing

**For more examples**, see: `docs/EXAMPLES.md`
**For algorithm details**, see: `docs/DEBT_SIMPLIFICATION.md`
**For architecture**, see: `docs/ARCHITECTURE.md`

---

**Need help?** Type `HELP` in the CLI to see all available commands.
