# Hints: Vending Machine

## Hint 1: Actors

<details>
<summary>Click to reveal</summary>

1. **User/Customer** - Inserts money, selects product, collects product & change
2. **Admin/Operator** - Restocks products, collects money, maintenance

</details>

---

## Hint 2: States

<details>
<summary>Click to reveal</summary>

```
┌─────────┐     insertMoney      ┌────────────┐
│  IDLE   │ ───────────────────▶ │ HAS_MONEY  │
└─────────┘                      └────────────┘
     ▲                                 │
     │                                 │ selectProduct
     │ cancel                          │ (if valid)
     │                                 ▼
     │                          ┌────────────┐
     └────────── done ──────────│ DISPENSING │
                                └────────────┘
```

**States:**
- `IDLE` - Waiting for user
- `HAS_MONEY` - Money inserted, waiting for selection
- `DISPENSING` - Dispensing product
- `RETURNING_CHANGE` - Returning excess money (optional, can merge with DISPENSING)

</details>

---

## Hint 3: State Pattern Implementation

<details>
<summary>Click to reveal</summary>

```python
class VendingMachineState(ABC):
    def __init__(self, machine):
        self.machine = machine

    @abstractmethod
    def insert_money(self, amount): pass

    @abstractmethod
    def select_product(self, code): pass

    @abstractmethod
    def dispense(self): pass

    @abstractmethod
    def cancel(self): pass


class IdleState(VendingMachineState):
    def insert_money(self, amount):
        self.machine.balance += amount
        self.machine.set_state(HasMoneyState(self.machine))

    def select_product(self, code):
        raise InvalidOperationError("Insert money first")

    def dispense(self):
        raise InvalidOperationError("Nothing to dispense")

    def cancel(self):
        pass  # Nothing to cancel


class HasMoneyState(VendingMachineState):
    def insert_money(self, amount):
        self.machine.balance += amount

    def select_product(self, code):
        product = self.machine.get_product(code)
        if product is None:
            raise InvalidProductError()
        if product.quantity == 0:
            raise OutOfStockError()
        if self.machine.balance < product.price:
            raise InsufficientBalanceError()

        self.machine.selected_product = product
        self.machine.set_state(DispensingState(self.machine))

    def cancel(self):
        self.machine.return_money(self.machine.balance)
        self.machine.balance = 0
        self.machine.set_state(IdleState(self.machine))


class DispensingState(VendingMachineState):
    def dispense(self):
        product = self.machine.selected_product
        # Dispense product
        product.quantity -= 1
        self.machine.dispense_product(product)

        # Return change
        change = self.machine.balance - product.price
        if change > 0:
            self.machine.return_money(change)

        # Reset
        self.machine.balance = 0
        self.machine.selected_product = None
        self.machine.set_state(IdleState(self.machine))
```

</details>

---

## Hint 4: Class Design

<details>
<summary>Click to reveal</summary>

```
┌─────────────────────────────┐
│      VendingMachine         │
├─────────────────────────────┤
│ - inventory: Dict[str, Slot]│
│ - balance: int              │
│ - state: State              │
│ - selected_product: Product │
├─────────────────────────────┤
│ + insertMoney(amount)       │
│ + selectProduct(code)       │
│ + cancel()                  │
│ + getProducts()             │
└─────────────────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐  ┌────────────────────┐
│  Slot  │  │ VendingMachineState│ (ABC)
├────────┤  ├────────────────────┤
│- code  │  │+ insertMoney()     │
│- product│ │+ selectProduct()   │
│- quantity│ │+ dispense()       │
│- maxQty │  │+ cancel()         │
└────────┘  └────────────────────┘
    │                △
    ▼                │
┌────────┐    ┌──────┼──────┐
│Product │    │      │      │
├────────┤   Idle  HasMoney Dispensing
│- name  │  State  State    State
│- price │
└────────┘
```

</details>

---

## Hint 5: Change Calculation (Greedy)

<details>
<summary>Click to reveal</summary>

```python
class ChangeCalculator:
    DENOMINATIONS = [100, 50, 20, 10, 5, 2, 1]  # In cents or rupees

    def calculate_change(self, amount, available_coins):
        """
        Returns dict of denomination -> count
        Or raises InsufficientChangeError
        """
        change = {}
        remaining = amount

        for denom in self.DENOMINATIONS:
            if remaining <= 0:
                break

            count_needed = remaining // denom
            count_available = available_coins.get(denom, 0)
            count_to_use = min(count_needed, count_available)

            if count_to_use > 0:
                change[denom] = count_to_use
                remaining -= count_to_use * denom

        if remaining > 0:
            raise InsufficientChangeError()

        return change
```

</details>

---

## Hint 6: Inventory Management

<details>
<summary>Click to reveal</summary>

```python
class Slot:
    def __init__(self, code: str, product: Product, max_quantity: int):
        self.code = code
        self.product = product
        self.quantity = 0
        self.max_quantity = max_quantity

    def is_available(self):
        return self.quantity > 0

    def restock(self, count: int):
        self.quantity = min(self.quantity + count, self.max_quantity)

    def dispense(self):
        if self.quantity <= 0:
            raise OutOfStockError()
        self.quantity -= 1
        return self.product


class Inventory:
    def __init__(self):
        self.slots: Dict[str, Slot] = {}

    def add_slot(self, code: str, product: Product, max_qty: int):
        self.slots[code] = Slot(code, product, max_qty)

    def get_slot(self, code: str) -> Slot:
        return self.slots.get(code)

    def get_available_products(self) -> List[Slot]:
        return [s for s in self.slots.values() if s.is_available()]
```

</details>

---

## Hint 7: Full Class Diagram

<details>
<summary>Click to reveal</summary>

```
┌─────────────────────────────────────────────────────────┐
│                    VendingMachine                        │
├─────────────────────────────────────────────────────────┤
│ - inventory: Inventory                                   │
│ - cash_register: CashRegister                           │
│ - state: VendingMachineState                            │
│ - current_balance: int                                   │
│ - selected_slot: Slot                                    │
├─────────────────────────────────────────────────────────┤
│ + insertMoney(amount: int): void                        │
│ + selectProduct(code: str): void                        │
│ + cancel(): void                                         │
│ + dispense(): void                                       │
│ + displayProducts(): List[ProductInfo]                  │
│ + setState(state: VendingMachineState): void            │
└─────────────────────────────────────────────────────────┘
              │
     ┌────────┼────────────────┐
     ▼        ▼                ▼
┌──────────┐ ┌─────────────┐ ┌─────────────────────────────┐
│Inventory │ │CashRegister │ │  VendingMachineState (ABC)  │
├──────────┤ ├─────────────┤ ├─────────────────────────────┤
│- slots   │ │- coins: Map │ │ + insertMoney(amt)          │
├──────────┤ ├─────────────┤ │ + selectProduct(code)       │
│+getSlot()│ │+addMoney()  │ │ + dispense()                │
│+restock()│ │+getChange() │ │ + cancel()                  │
└──────────┘ │+collectCash()│ └─────────────────────────────┘
             └─────────────┘              △
                                          │
                              ┌───────────┼───────────┐
                              ▼           ▼           ▼
                         ┌────────┐  ┌─────────┐ ┌───────────┐
                         │IdleState│ │HasMoney │ │Dispensing │
                         │        │  │State    │ │State      │
                         └────────┘  └─────────┘ └───────────┘

┌────────────┐     ┌────────────┐
│   Slot     │     │  Product   │
├────────────┤     ├────────────┤
│ - code     │────▶│ - id       │
│ - product  │     │ - name     │
│ - quantity │     │ - price    │
│ - maxQty   │     └────────────┘
└────────────┘
```

</details>

---

## Hint 8: API Design

<details>
<summary>Click to reveal</summary>

```
# User APIs
GET  /machine/products                # List available products
POST /machine/money                   # Insert money
     { "amount": 50 }
POST /machine/select                  # Select product
     { "code": "A1" }
POST /machine/cancel                  # Cancel and refund

# Admin APIs
POST /machine/restock                 # Restock slot
     { "code": "A1", "quantity": 10 }
POST /machine/collect-cash            # Collect all cash
GET  /machine/status                  # Get inventory & cash status
```

**Response for /products:**
```json
{
    "products": [
        {"code": "A1", "name": "Chips", "price": 20, "available": true},
        {"code": "A2", "name": "Soda", "price": 30, "available": false},
        ...
    ],
    "current_balance": 0,
    "state": "IDLE"
}
```

</details>

---

## Common Mistakes to Avoid

1. **Not using State pattern** - Too many if-else for state checks
2. **Money as float** - Use integers (cents/paise)
3. **No change validation** - Must check if change is available BEFORE dispensing
4. **Direct state changes** - Always go through state methods
5. **Forgetting to reset** - Clear balance and selected product after transaction
