# Category Guide: Financial & Transaction Systems

## Overview

Financial systems demand **transaction integrity, proper state management, and auditability**. These problems test your ability to handle money-related operations where correctness is critical.

---

## Common Entities

| Entity | Purpose | Example |
|--------|---------|---------|
| Account | Holds balance/funds | BankAccount, Wallet |
| Transaction | Record of money movement | Deposit, Withdrawal, Transfer |
| User | Account holder | Customer, Merchant |
| Card | Payment instrument | DebitCard, CreditCard |
| Ledger | Transaction history | Entry with debit/credit |

---

## Key Design Patterns

### 1. State Pattern - For ATM/Transaction States
```
                    ┌─────────────────┐
                    │   ATMState      │ (ABC)
                    │  + insertCard() │
                    │  + enterPin()   │
                    │  + selectTxn()  │
                    └────────┬────────┘
                             │
    ┌──────────────┬─────────┼─────────┬──────────────┐
    ▼              ▼         ▼         ▼              ▼
┌────────┐   ┌─────────┐ ┌────────┐ ┌─────────┐ ┌──────────┐
│  Idle  │──▶│HasCard  │─▶│Authed  │─▶│  InTxn  │─▶│Dispensing│
└────────┘   └─────────┘ └────────┘ └─────────┘ └──────────┘
```

### 2. Strategy Pattern - For Split Types (Splitwise)
```
                    ┌─────────────────┐
                    │  SplitStrategy  │ (ABC)
                    │  + split()      │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  EqualSplit   │   │ ExactSplit    │   │ PercentSplit  │
└───────────────┘   └───────────────┘   └───────────────┘
```

### 3. Command Pattern - For Transactions (Undo support)
```
class Transaction(ABC):
    def execute(self)
    def undo(self)

class WithdrawTransaction(Transaction):
    def execute(self): account.debit(amount)
    def undo(self): account.credit(amount)
```

---

## Class Design Tips

### Account Design
```
┌─────────────────────────────┐
│         Account             │
├─────────────────────────────┤
│ - id                        │
│ - user_id                   │
│ - balance                   │
│ - account_type              │
│ - status                    │
├─────────────────────────────┤
│ + credit(amount)            │
│ + debit(amount)             │
│ + getBalance()              │
│ + freeze()                  │
└─────────────────────────────┘
         △
         │
    ┌────┴────┐
    ▼         ▼
Savings    Current
Account    Account
```

### Transaction with Double-Entry
```
┌─────────────────────────────┐
│       Transaction           │
├─────────────────────────────┤
│ - id                        │
│ - type: TxnType             │
│ - from_account              │
│ - to_account                │
│ - amount                    │
│ - status                    │
│ - created_at                │
│ - reference_id              │
└─────────────────────────────┘

Every transaction = Debit one account + Credit another
Transfer $100:
  - Debit Account A: -$100
  - Credit Account B: +$100
```

### Expense Split Design (Splitwise)
```
┌─────────────────┐       ┌─────────────────────┐
│     Group       │       │      Expense        │
├─────────────────┤       ├─────────────────────┤
│ - id            │       │ - id                │
│ - name          │◀──────│ - group_id          │
│ - members[]     │       │ - paid_by           │
│ - expenses[]    │       │ - amount            │
└─────────────────┘       │ - split_type        │
                          │ - splits[]          │
                          └─────────────────────┘
                                   │
                                   ▼
                          ┌─────────────────────┐
                          │       Split         │
                          ├─────────────────────┤
                          │ - user_id           │
                          │ - amount_owed       │
                          └─────────────────────┘
```

---

## Critical: Balance Calculation (Splitwise)

### Approach 1: Store Running Balance (Fast reads, complex writes)
```
user_balances = {
    ("Alice", "Bob"): 50,    # Alice owes Bob $50
    ("Bob", "Charlie"): 30,  # Bob owes Charlie $30
}
```

### Approach 2: Calculate from Transactions (Slow reads, simple writes)
```python
def get_balance(user_a, user_b):
    # Sum all expenses where A paid and B owes
    a_paid = sum(expense.get_owed_by(user_b)
                 for expense in expenses if expense.paid_by == user_a)
    # Sum all expenses where B paid and A owes
    b_paid = sum(expense.get_owed_by(user_a)
                 for expense in expenses if expense.paid_by == user_b)
    return a_paid - b_paid
```

### Approach 3: Hybrid - Balance Map with Transactions
```
Store balance map for quick reads
Update balance map on each expense
Keep transaction log for audit
```

---

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Float for money | Precision errors | Use Decimal or cents (integer) |
| No idempotency | Duplicate transactions | Use unique transaction reference |
| Missing audit trail | Can't trace issues | Log all state changes |
| Race conditions | Balance goes negative | Use DB transactions with locks |
| God class ATM | ATM handles everything | Extract State classes |

---

## Coding Hacks for Demo

### 1. Money as Integer (cents)
```python
class Money:
    def __init__(self, cents: int):
        self._cents = cents

    @classmethod
    def from_dollars(cls, dollars: float):
        return cls(int(dollars * 100))

    def to_dollars(self) -> float:
        return self._cents / 100
```

### 2. Split Calculation
```python
def equal_split(amount: int, num_people: int) -> List[int]:
    base = amount // num_people
    remainder = amount % num_people
    # First 'remainder' people pay 1 cent more
    return [base + (1 if i < remainder else 0) for i in range(num_people)]

# $100 split 3 ways: [3334, 3333, 3333] cents = $33.34, $33.33, $33.33
```

### 3. Balance Map for Splitwise
```python
class BalanceSheet:
    def __init__(self):
        self.balances = defaultdict(lambda: defaultdict(int))

    def add_expense(self, paid_by, splits: Dict[str, int]):
        for user, amount in splits.items():
            if user != paid_by:
                self.balances[user][paid_by] += amount
                self.balances[paid_by][user] -= amount

    def get_balance(self, user1, user2) -> int:
        return self.balances[user1][user2]
```

### 4. ATM State Transitions
```python
class ATM:
    def __init__(self):
        self.state = IdleState(self)

    def insert_card(self, card):
        self.state.insert_card(card)

    def set_state(self, state):
        self.state = state
```

---

## API Design

### ATM APIs (Internal)
```
POST   /atm/card/insert           # Insert card
POST   /atm/pin/verify            # Verify PIN
POST   /atm/transaction/withdraw  # Withdraw cash
POST   /atm/transaction/deposit   # Deposit cash
POST   /atm/transaction/balance   # Check balance
POST   /atm/card/eject            # End session
```

### Splitwise-like APIs
```
# Groups
POST   /groups                    # Create group
GET    /groups/{id}               # Get group details
POST   /groups/{id}/members       # Add member

# Expenses
POST   /groups/{id}/expenses      # Add expense
GET    /groups/{id}/expenses      # List expenses

# Balances
GET    /groups/{id}/balances      # Get all balances in group
GET    /users/{id}/balances       # Get user's total balances
POST   /settlements               # Record a settlement
```

### Add Expense Request
```json
POST /groups/{id}/expenses
{
    "description": "Dinner",
    "amount": 6000,  // cents
    "paid_by": "user-1",
    "split_type": "EQUAL",  // or EXACT, PERCENT
    "splits": [
        {"user_id": "user-1"},
        {"user_id": "user-2"},
        {"user_id": "user-3"}
    ]
}
```

### For Exact Split
```json
{
    "split_type": "EXACT",
    "splits": [
        {"user_id": "user-1", "amount": 2000},
        {"user_id": "user-2", "amount": 2500},
        {"user_id": "user-3", "amount": 1500}
    ]
}
```

---

## Interview Questions to Expect

1. "How do you ensure **transaction atomicity**?"
   → Database transactions, compensating transactions for failures

2. "How would you handle **concurrent withdrawals**?"
   → Pessimistic locking, check balance within transaction

3. "How does **settlement simplification** work in Splitwise?"
   → Min-cash-flow algorithm, net balances before settling

4. "How would you add **recurring expenses**?"
   → Store recurrence rule, generate expenses via background job

5. "How to handle **partial ATM dispensing failure**?"
   → Track dispensed amount, rollback or adjust transaction

---

## Checklist Before Interview

- [ ] Can explain ATM state machine
- [ ] Know how to avoid floating point for money
- [ ] Can implement different split strategies
- [ ] Understand double-entry bookkeeping concept
- [ ] Can handle concurrent balance updates
- [ ] Know balance calculation approaches
- [ ] Can explain transaction rollback
