# Debt Simplification Algorithm

## Table of Contents
- [Problem Statement](#problem-statement)
- [Why Minimize Transactions?](#why-minimize-transactions)
- [Naive Approach (What NOT to do)](#naive-approach-what-not-to-do)
- [Optimized Greedy Algorithm](#optimized-greedy-algorithm)
- [Implementation with Heaps](#implementation-with-heaps)
- [Examples](#examples)
- [Time Complexity Analysis](#time-complexity-analysis)
- [Edge Cases](#edge-cases)

---

## Problem Statement

In a shared expense scenario, multiple users may owe money to each other. When settling up, we want to:

1. **Ensure all debts are cleared**: Everyone reaches a net balance of ₹0
2. **Minimize the number of transactions**: Reduce the hassle of multiple payments

### Example Scenario

**Goa Trip - 4 Friends:**

| Person  | Paid    | Owes    | Net Balance |
|---------|---------|---------|-------------|
| Rajesh  | ₹12,000 | ₹3,800  | +₹8,200     |
| Priya   | ₹2,400  | ₹3,800  | -₹1,400     |
| Amit    | ₹800    | ₹3,800  | -₹3,000     |
| Sneha   | ₹0      | ₹3,800  | -₹3,800     |

**Net Balances:**
- Rajesh should receive ₹8,200
- Priya should pay ₹1,400
- Amit should pay ₹3,000
- Sneha should pay ₹3,800

**Total owed = Total to receive = ₹8,200** ✓

---

## Why Minimize Transactions?

### Without Optimization

Every person could pay every person they owe:

```
Priya  → Rajesh: ₹600
Priya  → ???:    ₹600

Amit   → Rajesh: ₹600
Amit   → ???:    ₹2,400

Sneha  → Rajesh: ₹600
Sneha  → ???:    ₹3,200

... (multiple more transactions)
```

This could require **O(n²)** transactions in the worst case!

### With Optimization

We can settle everyone with just **3 transactions**:

```
1. Sneha → Rajesh: ₹3,800
2. Amit  → Rajesh: ₹3,000
3. Priya → Rajesh: ₹1,200
```

**Everyone is settled with minimum hassle!** ✓

---

## Naive Approach (What NOT to do)

### Approach 1: Pairwise Settlement (Brute Force)

**The Idea:** For every expense, each person who owes pays each person who paid.

```python
# Brute force: Settle each expense individually
for each expense:
    for each person who paid:
        for each person who owes:
            create_transaction(ower, payer, amount)
```

**Why O(n²)?**
- In a group of `n` people
- Each expense can involve up to `n` people
- Worst case: `n` payers × `n` debtors = `n²` transactions per expense
- Multiple expenses multiply this further

---

### Detailed Example: 4-Person Trip

**Expenses:**
1. Hotel (₹12,000): Rajesh paid, 4 people split equally (₹3,000 each)
2. Dinner (₹2,400): Priya paid, 4 people split equally (₹600 each)
3. Cab (₹800): Amit paid, 4 people split equally (₹200 each)

**Brute Force Settlement:**

```
Expense 1 - Hotel:
  Rajesh paid ₹12,000
  Priya owes ₹3,000  → Transaction 1: Priya → Rajesh ₹3,000
  Amit owes ₹3,000   → Transaction 2: Amit → Rajesh ₹3,000
  Sneha owes ₹3,000  → Transaction 3: Sneha → Rajesh ₹3,000
  (3 transactions for this expense)

Expense 2 - Dinner:
  Priya paid ₹2,400
  Rajesh owes ₹600   → Transaction 4: Rajesh → Priya ₹600
  Amit owes ₹600     → Transaction 5: Amit → Priya ₹600
  Sneha owes ₹600    → Transaction 6: Sneha → Priya ₹600
  (3 transactions for this expense)

Expense 3 - Cab:
  Amit paid ₹800
  Rajesh owes ₹200   → Transaction 7: Rajesh → Amit ₹200
  Priya owes ₹200    → Transaction 8: Priya → Amit ₹200
  Sneha owes ₹200    → Transaction 9: Sneha → Amit ₹200
  (3 transactions for this expense)

TOTAL: 9 transactions
```

**Problems with Brute Force:**
1. ❌ **Too many transactions:** 9 transactions for just 3 expenses
2. ❌ **Conflicting flows:** Rajesh pays Priya ₹600 (txn 4) but Priya pays Rajesh ₹3,000 (txn 1)
   - These should cancel out to: Priya pays Rajesh ₹2,400
3. ❌ **Multiple transactions between same pair:** Amit owes Rajesh (txn 2) and Rajesh owes Amit (txn 7)
   - Should net to: Amit pays Rajesh ₹2,800

---

### Optimized Solution: Net Balance

**Step 1: Calculate net balances**
```
Rajesh: Paid ₹12,000 - Owed ₹3,800 = +₹8,200 (to receive)
Priya:  Paid ₹2,400  - Owed ₹3,800 = -₹1,400 (to pay)
Amit:   Paid ₹800    - Owed ₹3,800 = -₹3,000 (to pay)
Sneha:  Paid ₹0      - Owed ₹3,800 = -₹3,800 (to pay)
```

**Step 2: Match using greedy algorithm (largest first)**
```
Transaction 1: Sneha → Rajesh ₹3,800
Transaction 2: Amit  → Rajesh ₹3,000
Transaction 3: Priya → Rajesh ₹1,400

TOTAL: 3 transactions (vs 9 with brute force!)
```

**Reduction:** 9 transactions → 3 transactions = **67% fewer transactions!**

---

### Why O(n²) Complexity?

**Brute Force Approach:**
```python
for expense in expenses:                    # E expenses
    payers = expense.paid_by                # P people paid
    debtors = expense.owed_by               # D people owe

    for payer in payers:                    # P iterations
        for debtor in debtors:              # D iterations
            if debtor != payer:
                create_transaction()        # Transaction created
```

**Analysis:**
- For each expense: P × D transactions
- Worst case: Everyone paid, everyone owes → n × n = n² per expense
- Total transactions: E × n² (E expenses, n² transactions each)
- **Time Complexity: O(E × n²)**

**Example with 10 people, 20 expenses:**
- Brute force: 20 × (10 × 10) = **2,000 transactions**
- Optimized: At most 9 transactions (n - 1)
- **200x reduction!**

---

### Approach 2: Individual Settlement Without Netting

Another naive approach:

```python
# Track all individual debts
debts = {}
for expense in expenses:
    for payer, amount_paid in expense.paid_by:
        for debtor, amount_owed in expense.owed_by:
            if payer != debtor:
                debts[(debtor, payer)] = debts.get((debtor, payer), 0) + amount_owed

# Create transaction for each debt
for (debtor, payer), amount in debts.items():
    create_transaction(debtor, payer, amount)
```

**Still O(n²) transactions:**
```
Example from above:
  Priya → Rajesh: ₹3,000 (Hotel)
  Priya → Amit: ₹200 (Cab)
  Rajesh → Priya: ₹600 (Dinner)
  Rajesh → Amit: ₹200 (Cab)
  Amit → Rajesh: ₹3,000 (Hotel)
  Amit → Priya: ₹600 (Dinner)
  Sneha → Rajesh: ₹3,000 (Hotel)
  Sneha → Priya: ₹600 (Dinner)
  Sneha → Amit: ₹200 (Cab)

Total: 9 transactions (every pair has a transaction)
```

**Problem:** Doesn't account for net flow between pairs.
- Priya → Rajesh: ₹3,000
- Rajesh → Priya: ₹600
- **Should net to:** Priya → Rajesh: ₹2,400 (1 transaction instead of 2)

---

## Optimized Greedy Algorithm

### Core Concept

1. **Calculate Net Balance**: For each person, compute `paid - owed`
2. **Separate Creditors and Debtors**:
   - Creditors: People with positive balance (should receive money)
   - Debtors: People with negative balance (should pay money)
3. **Match Largest Debts**: Use heaps to always match the largest debt with largest credit

### Why This Works

**Key Insight:** The order of who pays whom doesn't matter, only that final balances reach zero.

**Invariant:** `Sum of all positive balances = Sum of all negative balances`

By matching largest values first, we minimize the number of transactions needed.

---

## Implementation with Heaps

### Algorithm Steps

```python
def minimize_transactions(balances):
    """
    Input: Dict of {User: net_balance}
    Output: List of minimal transactions
    """

    # Step 1: Create two max heaps
    creditors = []  # People to receive money (positive balance)
    debtors = []    # People to pay money (negative balance)

    for user, balance in balances.items():
        if balance > 0:
            heappush(creditors, (-balance, user))  # Max heap
        elif balance < 0:
            heappush(debtors, (balance, user))  # Min heap (already negative)

    transactions = []

    # Step 2: Match largest debtor with largest creditor
    while creditors and debtors:
        # Pop largest credit and largest debt
        credit_amt, creditor = heappop(creditors)
        debt_amt, debtor = heappop(debtors)

        credit_amt = abs(credit_amt)
        debt_amt = abs(debt_amt)

        # Settle the minimum of the two
        settle_amount = min(credit_amt, debt_amt)

        transactions.append(
            f"{debtor.name} pays ₹{settle_amount:.2f} to {creditor.name}"
        )

        # If there's remaining balance, push back to heap
        remaining_credit = credit_amt - settle_amount
        remaining_debt = debt_amt - settle_amount

        if remaining_credit > 0.01:
            heappush(creditors, (-remaining_credit, creditor))

        if remaining_debt > 0.01:
            heappush(debtors, (-remaining_debt, debtor))

    return transactions
```

### Why Use Heaps?

- **Efficient**: O(log n) for insert and extract operations
- **Always Get Max**: Automatically maintains max element at the top
- **Greedy Choice**: Always match largest debt with largest credit

---

## Examples

### Example 1: Simple Case - 3 People

**Scenario:** Lunch among colleagues

| Person  | Net Balance |
|---------|-------------|
| Rajesh  | +₹600       |
| Priya   | -₹400       |
| Amit    | -₹200       |

**Visualization:**

```
Initial State:
  Creditors: [Rajesh: +₹600]
  Debtors:   [Priya: -₹400, Amit: -₹200]

Step 1: Match Rajesh (₹600) with Priya (₹400)
  Transaction: "Priya pays ₹400 to Rajesh"

  After Step 1:
    Creditors: [Rajesh: +₹200]  (₹600 - ₹400)
    Debtors:   [Amit: -₹200]

Step 2: Match Rajesh (₹200) with Amit (₹200)
  Transaction: "Amit pays ₹200 to Rajesh"

  After Step 2:
    Creditors: []
    Debtors:   []

✓ Settled with 2 transactions (instead of potentially more)
```

### Example 2: Complex Case - 5 People (Goa Trip)

**Scenario:** Multiple expenses on trip

| Person  | Paid     | Owes     | Net Balance |
|---------|----------|----------|-------------|
| Rajesh  | ₹12,000  | ₹3,800   | +₹8,200     |
| Priya   | ₹2,400   | ₹3,800   | -₹1,400     |
| Amit    | ₹800     | ₹3,800   | -₹3,000     |
| Sneha   | ₹0       | ₹3,800   | -₹3,800     |
| Vikram  | ₹0       | ₹0       | ₹0          |

**Note:** Vikram has ₹0 balance, so excluded from settlement.

**Step-by-Step Execution:**

```
Initial Heaps:
  Creditors (max heap): [Rajesh: ₹8,200]
  Debtors (max heap):   [Sneha: ₹3,800, Amit: ₹3,000, Priya: ₹1,400]

─────────────────────────────────────────────────────────────

ITERATION 1:
  Pop: Rajesh (₹8,200) and Sneha (₹3,800)
  Settle: min(8200, 3800) = ₹3,800

  Transaction 1: "Sneha pays ₹3,800 to Rajesh"

  Remaining:
    Rajesh: ₹8,200 - ₹3,800 = ₹4,400 (push back to creditors)
    Sneha: ₹0 (settled, don't push back)

  After Iteration 1:
    Creditors: [Rajesh: ₹4,400]
    Debtors:   [Amit: ₹3,000, Priya: ₹1,400]

─────────────────────────────────────────────────────────────

ITERATION 2:
  Pop: Rajesh (₹4,400) and Amit (₹3,000)
  Settle: min(4400, 3000) = ₹3,000

  Transaction 2: "Amit pays ₹3,000 to Rajesh"

  Remaining:
    Rajesh: ₹4,400 - ₹3,000 = ₹1,400 (push back)
    Amit: ₹0 (settled)

  After Iteration 2:
    Creditors: [Rajesh: ₹1,400]
    Debtors:   [Priya: ₹1,400]

─────────────────────────────────────────────────────────────

ITERATION 3:
  Pop: Rajesh (₹1,400) and Priya (₹1,400)
  Settle: min(1400, 1400) = ₹1,400

  Transaction 3: "Priya pays ₹1,400 to Rajesh"

  Remaining:
    Rajesh: ₹0 (settled)
    Priya: ₹0 (settled)

  After Iteration 3:
    Creditors: []
    Debtors:   []

─────────────────────────────────────────────────────────────

✓ SETTLED WITH 3 TRANSACTIONS!

Final Transactions:
  1. Sneha pays ₹3,800 to Rajesh
  2. Amit pays ₹3,000 to Rajesh
  3. Priya pays ₹1,400 to Rajesh

All balances are now ₹0!
```

### Example 3: Multiple Creditors

**Scenario:** More complex case with multiple creditors

| Person  | Net Balance |
|---------|-------------|
| Rajesh  | +₹5,000     |
| Priya   | +₹3,000     |
| Amit    | -₹4,000     |
| Sneha   | -₹4,000     |

```
Initial:
  Creditors: [Rajesh: ₹5,000, Priya: ₹3,000]
  Debtors:   [Amit: ₹4,000, Sneha: ₹4,000]

Iteration 1:
  Match Rajesh (₹5,000) with Amit (₹4,000)
  Transaction: "Amit pays ₹4,000 to Rajesh"

  Remaining: Rajesh has ₹1,000 left

Iteration 2:
  Match Priya (₹3,000) with Sneha (₹4,000)
  Transaction: "Sneha pays ₹3,000 to Priya"

  Remaining: Sneha has ₹1,000 left to pay

Iteration 3:
  Match Rajesh (₹1,000) with Sneha (₹1,000)
  Transaction: "Sneha pays ₹1,000 to Rajesh"

✓ Total: 3 transactions
```

**Diagram:**

```
Before:
  Rajesh: +₹5,000  ←─── Amit: -₹4,000
  Priya:  +₹3,000  ←─── Sneha: -₹4,000

After Transaction 1:
  Rajesh: +₹1,000
  Priya:  +₹3,000  ←─── Sneha: -₹4,000

After Transaction 2:
  Rajesh: +₹1,000  ←─── Sneha: -₹1,000
  Priya:  ₹0 ✓

After Transaction 3:
  All settled! ✓
```

---

## Time Complexity Analysis

### Algorithm Complexity

| Operation                    | Complexity | Explanation                              |
|------------------------------|------------|------------------------------------------|
| Calculate net balances       | O(E)       | E = number of expense records            |
| Build heaps                  | O(n log n) | n = number of people with non-zero bal   |
| Extract and settle (loop)    | O(n log n) | At most n iterations, each O(log n)      |
| **Total**                    | **O(E + n log n)** | Dominated by balance calc and heap ops |

### Space Complexity

| Data Structure | Space      | Explanation                     |
|----------------|------------|---------------------------------|
| Balances dict  | O(n)       | Store balance for each person   |
| Heaps          | O(n)       | Store people with non-zero bal  |
| Transactions   | O(n)       | At most n-1 transactions        |
| **Total**      | **O(n)**   | Linear space                    |

### Why This is Optimal

1. **Minimum Transactions**: With n people, minimum transactions needed is at most `n - 1`
   - Our algorithm achieves this

2. **Cannot Do Better**: It's proven that you need at least `n - 1` transactions in the worst case
   - Example: n people, one person paid for all, others owe → need n-1 transactions

3. **Greedy is Optimal**: The greedy approach of matching largest debts gives minimum transactions

---

## Edge Cases

### Case 1: Already Settled

```python
balances = {
    user1: 0,
    user2: 0,
    user3: 0
}

Result: "Already settled up! ✓"
Transactions: []
```

### Case 2: Only Two People

```python
balances = {
    rajesh: +500,
    priya: -500
}

Result:
Transactions: ["Priya pays ₹500 to Rajesh"]
```

### Case 3: One Person Owes Multiple

```python
balances = {
    rajesh: +1000,
    priya: +500,
    amit: -1500
}

Result:
Transaction 1: "Amit pays ₹1000 to Rajesh"
Transaction 2: "Amit pays ₹500 to Priya"
```

### Case 4: Floating Point Precision

```python
# Amounts like ₹333.33 when splitting ₹1000 three ways
# We use tolerance of 0.01 to ignore negligible differences

if abs(balance) < 0.01:
    # Skip this balance
    pass
```

### Case 5: Single Expense

```python
# One person paid, all others owe equally
# Example: Rajesh paid ₹1200, 4 people owe ₹300 each

balances = {
    rajesh: +900,    # Paid 1200, owes 300
    priya: -300,
    amit: -300,
    sneha: -300
}

Result: 3 transactions (each person pays Rajesh)
```

---

## Group Settlement vs User Settlement

### User Settlement

**Purpose:** Settle a single user's debts across ALL expenses (including multiple groups)

**Example:**
```python
# Rajesh has expenses in:
# - Goa Trip group
# - Office Lunch group
# - Personal expenses with friends

SETTLE_USER 1

# Calculates Rajesh's net balance with EVERY person
# across all expenses and groups
```

### Group Settlement

**Purpose:** Settle all members of a specific group based ONLY on that group's expenses

**Example:**
```python
# Settle "Goa Trip" group
# Only considers expenses within this group
# Ignores expenses outside the group

SETTLE_GROUP 1 1

# All members of "Goa Trip" settled
# But may still have balances from other groups/expenses
```

---

## Key Takeaways

1. **Greedy Algorithm Works**
   - Match largest debt with largest credit
   - Guaranteed to minimize transactions

2. **Heaps for Efficiency**
   - O(log n) operations
   - Always maintain max elements accessible

3. **Net Balance is Key**
   - Only net balance matters, not individual transactions
   - `paid - owed = net balance`

4. **Optimal Transaction Count**
   - Worst case: n - 1 transactions
   - Our algorithm achieves this optimum

5. **Real-World Application**
   - Splitwise, PayPal, Venmo use similar algorithms
   - Crucial for user experience (fewer transactions = less hassle)

---

## Further Reading

- **Graph Theory**: Cash flow optimization problem
- **Network Flow**: Min-cost flow algorithms
- **Algorithm Design**: Greedy algorithms and proof of correctness
- **Papers**: "Optimizing Cash Flow in Debt Networks" (various authors)
