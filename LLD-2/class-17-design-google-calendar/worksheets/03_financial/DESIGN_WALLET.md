# Design Digital Wallet

## Overview

A digital wallet allows users to store money, make payments, transfer funds, and track transaction history. Think PayTM, PhonePe, or Google Pay wallet functionality.

**Core Operations:**
- Add money (from bank/card)
- Pay merchants
- Transfer to other users
- Transaction history

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

1. What's the maximum wallet balance allowed?
2. What payment methods to add money?
3. Is there cashback/rewards system?
4. KYC requirements for higher limits?
5. Can wallet go negative (credit)?
6. Refund handling?

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

1. Users can add money to wallet from bank/card.
2. Users can check wallet balance.
3. Users can pay merchants using wallet.
4. Users can transfer money to other users.
5. All transactions are recorded with details.
6. Users can view transaction history.
7. Insufficient balance prevents transactions.
8. Support for refunds back to wallet.

</details>

---

## Class Diagram

**Think about:**
- Wallet and its balance
- Different transaction types
- Transaction states
- Idempotency (prevent duplicate transactions)

**Design Question: Transaction Types**
```
CREDIT: Add money, Receive transfer, Refund
DEBIT: Payment, Send transfer

Single Transaction class or separate?

```

List your classes:

```
Class 1:

Class 2:

Class 3:

Class 4:
```

Draw the class diagram:

```




```

---

## Key Design Decisions

**1. Balance Update - Sync or Async?**
```
User pays $50. When to deduct?

Your approach:

```

**2. Preventing Double Transactions**
```
User clicks "Pay" twice quickly. How to prevent?

```

**3. Transaction States**
```
What states can a transaction be in?

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
<summary><strong>Hint 1: Transaction Types</strong></summary>

```python
class TransactionType(Enum):
    CREDIT_ADD_MONEY = "credit_add_money"
    CREDIT_RECEIVED = "credit_received"
    CREDIT_REFUND = "credit_refund"
    CREDIT_CASHBACK = "credit_cashback"
    DEBIT_PAYMENT = "debit_payment"
    DEBIT_TRANSFER = "debit_transfer"

class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
```

</details>

<details>
<summary><strong>Hint 2: Wallet Operations</strong></summary>

```python
class Wallet:
    user_id: str
    balance: int  # In cents/paise
    created_at: datetime

    def credit(self, amount: int, txn_type: TransactionType) -> Transaction:
        with db.transaction():
            self.balance += amount
            return Transaction.create(
                wallet_id=self.id,
                amount=amount,
                type=txn_type,
                status=TransactionStatus.COMPLETED
            )

    def debit(self, amount: int, txn_type: TransactionType) -> Transaction:
        with db.transaction():
            if self.balance < amount:
                raise InsufficientBalanceError()
            self.balance -= amount
            return Transaction.create(...)
```

</details>

<details>
<summary><strong>Hint 3: Idempotency</strong></summary>

```python
def process_payment(wallet_id, amount, idempotency_key):
    # Check if already processed
    existing = Transaction.get_by_idempotency_key(idempotency_key)
    if existing:
        return existing  # Return same response

    # Process new transaction
    wallet = Wallet.get(wallet_id)
    txn = wallet.debit(amount, TransactionType.DEBIT_PAYMENT)
    txn.idempotency_key = idempotency_key
    return txn
```

</details>

<details>
<summary><strong>Hint 4: Class Structure</strong></summary>

```
┌─────────────────────────┐
│         Wallet          │
├─────────────────────────┤
│ - id                    │
│ - user_id               │
│ - balance               │
│ - status: ACTIVE|FROZEN │
│ - created_at            │
├─────────────────────────┤
│ + credit(amount)        │
│ + debit(amount)         │
│ + getBalance()          │
│ + freeze()              │
└─────────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────────┐
│      Transaction        │
├─────────────────────────┤
│ - id                    │
│ - wallet_id             │
│ - amount                │
│ - type                  │
│ - status                │
│ - reference_id          │
│ - idempotency_key       │
│ - description           │
│ - created_at            │
└─────────────────────────┘
```

</details>
