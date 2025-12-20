# Design Shopping Cart

## Overview

A shopping cart system allows users to browse products, add items to cart, manage quantities, apply coupons, and proceed to checkout. This is the core of any e-commerce platform.

**Key Operations:**
- Add/remove items
- Update quantities
- Apply discounts/coupons
- Calculate totals (subtotal, tax, shipping)
- Checkout flow

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

1. Can guest users have carts?
2. How long does cart persist?
3. What happens when item goes out of stock?
4. Multiple discount codes allowed?
5. Is inventory reserved when added to cart?
6. Cart merging when guest logs in?

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

1. Users can add products to cart.
2. Users can update quantity of items.
3. Users can remove items from cart.
4. Cart shows subtotal, taxes, and total.
5. Users can apply discount/coupon codes.
6. System validates stock availability.
7. Cart persists across sessions.
8. Users can proceed to checkout.

</details>

---

## Class Diagram

**Think about:**
- Cart and CartItem relationship
- Product vs CartItem (why separate?)
- Pricing and discount strategies
- Cart → Order transition

**Design Question: Why snapshot product in CartItem?**
```
Product price changes from $100 to $120.
What should cart show?

Your approach:

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

**1. Inventory Check - When?**
```
Option A: Check when adding to cart
Option B: Check only at checkout
Option C: Both

Your choice:

```

**2. Discount/Coupon System**
```
Flat discount, Percentage, Buy-1-Get-1, Min order value
How to model?

```

**3. Cart Expiry**
```
User abandons cart. When to clear?

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
<summary><strong>Hint 1: Cart Structure</strong></summary>

```
┌─────────────────────────┐
│         Cart            │
├─────────────────────────┤
│ - id                    │
│ - user_id               │
│ - items[]               │
│ - coupon_code           │
│ - created_at            │
│ - updated_at            │
├─────────────────────────┤
│ + addItem(product, qty) │
│ + removeItem(productId) │
│ + updateQuantity()      │
│ + applyCoupon(code)     │
│ + getSubtotal()         │
│ + getTotal()            │
│ + checkout()            │
└─────────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────────┐
│       CartItem          │
├─────────────────────────┤
│ - product_id            │
│ - product_name          │ ← Snapshot
│ - unit_price            │ ← Snapshot at add time
│ - quantity              │
│ - added_at              │
├─────────────────────────┤
│ + getItemTotal()        │
└─────────────────────────┘
```

</details>

<details>
<summary><strong>Hint 2: Pricing Calculation</strong></summary>

```python
class Cart:
    def get_subtotal(self) -> int:
        return sum(item.get_total() for item in self.items)

    def get_discount(self) -> int:
        if not self.coupon:
            return 0
        return self.coupon.calculate_discount(self.get_subtotal())

    def get_tax(self) -> int:
        taxable = self.get_subtotal() - self.get_discount()
        return int(taxable * 0.18)  # 18% GST

    def get_total(self) -> int:
        return self.get_subtotal() - self.get_discount() + self.get_tax()
```

</details>

<details>
<summary><strong>Hint 3: Coupon Strategy</strong></summary>

```python
class Coupon(ABC):
    code: str
    min_order_value: int
    max_discount: int
    valid_until: date

    @abstractmethod
    def calculate_discount(self, subtotal: int) -> int:
        pass

    def is_valid(self, subtotal: int) -> bool:
        return (subtotal >= self.min_order_value and
                date.today() <= self.valid_until)

class PercentageCoupon(Coupon):
    percentage: int  # e.g., 20 for 20%

    def calculate_discount(self, subtotal):
        discount = subtotal * self.percentage // 100
        return min(discount, self.max_discount)

class FlatCoupon(Coupon):
    flat_amount: int

    def calculate_discount(self, subtotal):
        return min(self.flat_amount, subtotal)
```

</details>

<details>
<summary><strong>Hint 4: Cart to Order</strong></summary>

```python
def checkout(self) -> Order:
    # Validate stock
    for item in self.items:
        if not Inventory.has_stock(item.product_id, item.quantity):
            raise OutOfStockError(item.product_id)

    # Create order with snapshot of cart
    order = Order.create(
        user_id=self.user_id,
        items=[OrderItem.from_cart_item(i) for i in self.items],
        subtotal=self.get_subtotal(),
        discount=self.get_discount(),
        tax=self.get_tax(),
        total=self.get_total()
    )

    # Reserve inventory
    for item in self.items:
        Inventory.reserve(item.product_id, item.quantity)

    # Clear cart
    self.items = []

    return order
```

</details>
