# Design Expense Sharing (Splitwise)

## Overview

An expense sharing application helps groups of people track shared expenses and settle debts. When someone pays for a group expense, the app calculates who owes whom and helps simplify settlements.

**Core Problem:** A pays $60 for dinner for A, B, C. Now B owes A $20, C owes A $20.

---

## Expectations

* Code should be functionally correct.
* Code should be modular and readable.
* Code should be extensible and scalable.
* Code should have good OOP design principles.

---

## Requirements Gathering

```
1.
2.
3.
4.
5.
```

<details>
<summary><strong>Sample clarifying questions</strong></summary>

1. What split types? (Equal, Exact amounts, Percentage)
2. Can expenses be split among non-group members?
3. How are settlements recorded?
4. Multi-currency support?
5. Can users be in multiple groups?
6. Should we simplify debts? (A→B→C becomes A→C)

</details>

---

## Requirements

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
<summary><strong>Click to see requirements</strong></summary>

1. Users can create groups and add members.
2. Users can add expenses with description and amount.
3. Expenses can be split: Equal, Exact, or Percentage.
4. System tracks who owes whom.
5. Users can view their total balance (owed/owing).
6. Users can settle up (record payments).
7. System shows expense history.
8. Users can see simplified debts within group.

</details>

---

## Class Diagram

**Think about:**
- User, Group, Expense relationships
- Different split strategies
- Balance calculation approach

**Critical Question: How to calculate balances?**
```
Option A: Store running balance between each pair
Option B: Calculate from expense history each time
Option C: Hybrid

Your choice and tradeoffs:

```

List your classes:

```
Class 1:

Class 2:

Class 3:

Class 4:

Class 5:
```

Draw the class diagram:

```




```

---

## Key Design Decisions

**1. Split Types - Strategy Pattern?**
```
Equal: $60 / 3 = $20 each
Exact: A=$30, B=$20, C=$10
Percent: A=50%, B=30%, C=20%

How to model?

```

**2. Balance Storage**
```
If A paid $60 split among A,B,C:
- B owes A: $20
- C owes A: $20

How to store efficiently?

```

**3. Settlement Simplification**
```
A owes B $10
B owes C $10
Simplified: A owes C $10

Algorithm?

```

---

## API Design

```
1.
2.
3.
4.
5.
```

---

## Hints

<details>
<summary><strong>Hint 1: Split Strategy Pattern</strong></summary>

```python
class SplitStrategy(ABC):
    @abstractmethod
    def calculate_splits(self, amount: int, participants: List[User]) -> Dict[User, int]:
        pass

class EqualSplit(SplitStrategy):
    def calculate_splits(self, amount, participants):
        n = len(participants)
        base = amount // n
        remainder = amount % n
        splits = {}
        for i, user in enumerate(participants):
            splits[user] = base + (1 if i < remainder else 0)
        return splits

class ExactSplit(SplitStrategy):
    def __init__(self, exact_amounts: Dict[User, int]):
        self.exact_amounts = exact_amounts

    def calculate_splits(self, amount, participants):
        assert sum(self.exact_amounts.values()) == amount
        return self.exact_amounts

class PercentSplit(SplitStrategy):
    def __init__(self, percentages: Dict[User, float]):
        self.percentages = percentages

    def calculate_splits(self, amount, participants):
        return {user: int(amount * pct / 100)
                for user, pct in self.percentages.items()}
```

</details>

<details>
<summary><strong>Hint 2: Balance Map</strong></summary>

```python
class BalanceSheet:
    def __init__(self):
        # balances[A][B] = amount A owes B
        self.balances = defaultdict(lambda: defaultdict(int))

    def add_expense(self, paid_by: User, splits: Dict[User, int]):
        for user, amount in splits.items():
            if user != paid_by:
                # user owes paid_by
                self.balances[user][paid_by] += amount

    def get_balance(self, user1, user2) -> int:
        """Positive = user1 owes user2"""
        owes = self.balances[user1][user2]
        owed = self.balances[user2][user1]
        return owes - owed

    def get_net_balance(self, user) -> int:
        """Positive = user owes overall, Negative = user is owed"""
        total = 0
        for other in self.balances:
            total += self.get_balance(user, other)
        return total
```

</details>

<details>
<summary><strong>Hint 3: Class Structure</strong></summary>

```
┌─────────────────┐       ┌─────────────────┐
│      User       │       │      Group      │
├─────────────────┤       ├─────────────────┤
│ - id            │ M:N   │ - id            │
│ - name          │◀─────▶│ - name          │
│ - email         │       │ - members[]     │
└─────────────────┘       │ - expenses[]    │
                          └─────────────────┘
                                  │
                                  │ 1:N
                                  ▼
                          ┌─────────────────────┐
                          │      Expense        │
                          ├─────────────────────┤
                          │ - id                │
                          │ - description       │
                          │ - amount            │
                          │ - paid_by           │
                          │ - split_type        │
                          │ - splits[]          │
                          │ - created_at        │
                          └─────────────────────┘
                                  │
                                  │ 1:N
                                  ▼
                          ┌─────────────────────┐
                          │   ExpenseSplit      │
                          ├─────────────────────┤
                          │ - user_id           │
                          │ - amount            │
                          └─────────────────────┘
```

</details>

<details>
<summary><strong>Hint 4: Simplify Debts Algorithm</strong></summary>

```python
def simplify_debts(balances: Dict[User, int]) -> List[Tuple[User, User, int]]:
    """
    Input: net balance per user (positive = owes, negative = owed)
    Output: minimal transactions to settle
    """
    creditors = []  # (user, amount) - owed money
    debtors = []    # (user, amount) - owes money

    for user, balance in balances.items():
        if balance > 0:
            debtors.append([user, balance])
        elif balance < 0:
            creditors.append([user, -balance])

    transactions = []
    i, j = 0, 0

    while i < len(debtors) and j < len(creditors):
        debtor, debt = debtors[i]
        creditor, credit = creditors[j]

        amount = min(debt, credit)
        transactions.append((debtor, creditor, amount))

        debtors[i][1] -= amount
        creditors[j][1] -= amount

        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    return transactions
```

</details>
