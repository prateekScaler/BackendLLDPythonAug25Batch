# Category Guide: E-commerce & Marketplace

## Overview

E-commerce LLD problems test your ability to model **product catalogs, shopping carts, order lifecycle, and inventory management**. These are complex systems with many interconnected entities.

---

## Common Entities

| Entity | Purpose | Example |
|--------|---------|---------|
| Product | Item being sold | Book, Electronics, Food item |
| Cart | User's selected items | ShoppingCart |
| Order | Confirmed purchase | Order with status tracking |
| Inventory | Stock management | InventoryItem with quantity |
| Payment | Payment processing | PaymentTransaction |
| User | Buyer/Seller | Customer, Vendor |

---

## Key Design Patterns

### 1. Strategy Pattern - For Pricing/Discounts
```
                    ┌───────────────────────┐
                    │  PricingStrategy      │ (ABC)
                    │  + calculate(cart)    │
                    └───────────┬───────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│ RegularPrice  │      │  BulkDiscount │      │ CouponDiscount│
└───────────────┘      └───────────────┘      └───────────────┘
```

### 2. State Pattern - For Order Lifecycle
```
┌─────────┐    ┌──────────┐    ┌────────┐    ┌───────────┐    ┌───────────┐
│ Created │───▶│ Confirmed│───▶│ Shipped│───▶│ Delivered │───▶│ Completed │
└─────────┘    └──────────┘    └────────┘    └───────────┘    └───────────┘
     │              │              │
     ▼              ▼              ▼
┌─────────┐    ┌──────────┐    ┌────────┐
│Cancelled│    │ Cancelled│    │Returned│
└─────────┘    └──────────┘    └────────┘
```

### 3. Observer Pattern - For Notifications
```
Order status changes → Notify: Email, SMS, Push, Vendor
```

### 4. Decorator Pattern - For Product Add-ons
```
BasePizza → CheeseDecorator → ToppingsDecorator → FinalProduct
```

---

## Class Design: Shopping Cart System

### Core Classes
```
┌─────────────────────┐
│       Product       │
├─────────────────────┤
│ - id                │
│ - name              │
│ - description       │
│ - base_price        │
│ - category          │
│ - seller_id         │
└─────────────────────┘

┌─────────────────────┐
│       CartItem      │
├─────────────────────┤
│ - product           │
│ - quantity          │
│ - unit_price        │
│ + getTotal()        │
└─────────────────────┘

┌─────────────────────┐
│    ShoppingCart     │
├─────────────────────┤
│ - id                │
│ - user_id           │
│ - items[]           │
│ - created_at        │
│ + addItem()         │
│ + removeItem()      │
│ + updateQuantity()  │
│ + getTotal()        │
│ + checkout()        │
└─────────────────────┘
```

### Order Structure
```
┌─────────────────────────┐
│         Order           │
├─────────────────────────┤
│ - id                    │
│ - user_id               │
│ - items: List[OrderItem]│
│ - status: OrderStatus   │
│ - shipping_address      │
│ - payment_id            │
│ - subtotal              │
│ - discount              │
│ - tax                   │
│ - total                 │
│ - created_at            │
│ - updated_at            │
└─────────────────────────┘

┌─────────────────────────┐
│       OrderItem         │
├─────────────────────────┤
│ - product_id            │
│ - product_snapshot      │ ← Important: Store product details at order time
│ - quantity              │
│ - unit_price            │
│ - status                │
└─────────────────────────┘
```

---

## Class Design: Food Delivery

### Additional Entities
```
┌─────────────────────┐       ┌─────────────────────┐
│     Restaurant      │       │        Menu         │
├─────────────────────┤       ├─────────────────────┤
│ - id                │       │ - id                │
│ - name              │──────▶│ - restaurant_id     │
│ - address           │       │ - items[]           │
│ - is_open           │       └─────────────────────┘
│ - rating            │                │
│ - cuisines[]        │                ▼
└─────────────────────┘       ┌─────────────────────┐
                              │      MenuItem       │
                              ├─────────────────────┤
                              │ - id                │
                              │ - name              │
                              │ - price             │
                              │ - category          │
                              │ - is_available      │
                              │ - customizations[]  │
                              └─────────────────────┘

┌─────────────────────────┐
│     DeliveryOrder       │
├─────────────────────────┤
│ - id                    │
│ - restaurant_id         │
│ - customer_id           │
│ - delivery_partner_id   │
│ - items[]               │
│ - status                │
│ - delivery_address      │
│ - estimated_time        │
│ - actual_delivery_time  │
└─────────────────────────┘

Order Status Flow:
PLACED → ACCEPTED → PREPARING → READY → PICKED_UP → DELIVERED
   │         │
   ▼         ▼
REJECTED  CANCELLED
```

---

## Critical: Inventory Management

### The Problem
```
Product has 5 items in stock
User A adds 3 to cart
User B adds 4 to cart
Both try to checkout → Only 5 exist!
```

### Solutions

**1. Reserve on Add to Cart (Pessimistic)**
```python
def add_to_cart(product_id, quantity):
    with transaction():
        inventory = Inventory.select_for_update(product_id)
        if inventory.available >= quantity:
            inventory.available -= quantity
            inventory.reserved += quantity
            cart.add(product_id, quantity)
        else:
            raise OutOfStockError()
```
- Pro: Guarantees availability
- Con: Items locked even if user abandons cart

**2. Check at Checkout (Optimistic)**
```python
def checkout(cart):
    with transaction():
        for item in cart.items:
            inventory = Inventory.select_for_update(item.product_id)
            if inventory.available < item.quantity:
                raise OutOfStockError(item.product_id)
            inventory.available -= item.quantity
        create_order(cart)
```
- Pro: No orphaned reservations
- Con: User may face out-of-stock at checkout

**3. Hybrid - Reserve with Expiry**
```python
# Reserve with 15-minute expiry
reservation = InventoryReservation(
    product_id=product_id,
    quantity=quantity,
    expires_at=now() + timedelta(minutes=15)
)
# Background job releases expired reservations
```

---

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Price in CartItem only | Price changes affect cart | Snapshot price when adding |
| No product snapshot in Order | Product deleted = order broken | Store product details with order |
| Cart never expires | Zombie carts with reserved inventory | Expire carts, release inventory |
| Missing order status history | Can't track order journey | Store status change log |
| Coupling Order to Product | Product changes affect order | OrderItem has its own data |

---

## Coding Hacks for Demo

### 1. Cart Total Calculation
```python
class ShoppingCart:
    def get_subtotal(self):
        return sum(item.quantity * item.unit_price for item in self.items)

    def get_total(self, discount_code=None):
        subtotal = self.get_subtotal()
        discount = self.calculate_discount(subtotal, discount_code)
        tax = (subtotal - discount) * 0.18  # 18% GST
        return subtotal - discount + tax
```

### 2. Coupon Validation
```python
class Coupon:
    def is_valid(self, cart):
        if self.expires_at < now():
            return False
        if cart.get_subtotal() < self.min_order_value:
            return False
        if self.usage_count >= self.max_uses:
            return False
        return True

    def apply(self, subtotal):
        if self.type == CouponType.PERCENTAGE:
            return min(subtotal * self.value / 100, self.max_discount)
        return min(self.value, subtotal)
```

### 3. Order Status Transitions
```python
VALID_TRANSITIONS = {
    OrderStatus.CREATED: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
    OrderStatus.CONFIRMED: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
    OrderStatus.SHIPPED: [OrderStatus.DELIVERED, OrderStatus.RETURNED],
    OrderStatus.DELIVERED: [OrderStatus.COMPLETED, OrderStatus.RETURNED],
}

def update_status(self, new_status):
    if new_status not in VALID_TRANSITIONS.get(self.status, []):
        raise InvalidTransitionError()
    self.status = new_status
```

### 4. Restaurant Search
```python
def search_restaurants(location, cuisine=None, rating_min=None):
    query = Restaurant.query.filter(
        Restaurant.is_open == True,
        Restaurant.delivery_radius.contains(location)
    )
    if cuisine:
        query = query.filter(Restaurant.cuisines.contains(cuisine))
    if rating_min:
        query = query.filter(Restaurant.rating >= rating_min)
    return query.order_by(Restaurant.rating.desc()).all()
```

---

## API Design

### Shopping Cart
```
GET    /cart                       # Get user's cart
POST   /cart/items                 # Add item to cart
PUT    /cart/items/{id}            # Update quantity
DELETE /cart/items/{id}            # Remove item
POST   /cart/checkout              # Initiate checkout

# Add to Cart
POST /cart/items
{
    "product_id": "prod-123",
    "quantity": 2
}
```

### Orders
```
POST   /orders                     # Create order from cart
GET    /orders                     # List user's orders
GET    /orders/{id}                # Get order details
PUT    /orders/{id}/cancel         # Cancel order
POST   /orders/{id}/return         # Initiate return
```

### Food Delivery
```
GET    /restaurants                # Search restaurants
GET    /restaurants/{id}/menu      # Get menu
POST   /orders                     # Place order
GET    /orders/{id}/track          # Track order
```

### Order Response
```json
{
    "id": "order-123",
    "status": "CONFIRMED",
    "items": [
        {
            "product_id": "prod-1",
            "name": "Product Name",
            "quantity": 2,
            "unit_price": 999,
            "total": 1998
        }
    ],
    "subtotal": 1998,
    "discount": 200,
    "tax": 324,
    "total": 2122,
    "shipping_address": {...},
    "estimated_delivery": "2024-01-17"
}
```

---

## Interview Questions to Expect

1. "How do you handle **flash sales** with limited inventory?"
   → Queue-based processing, atomic inventory decrement, rate limiting

2. "How would you implement **product recommendations**?"
   → Collaborative filtering, "users who bought X also bought Y"

3. "How to handle **order cancellation** after shipping?"
   → Return flow, refund processing, inventory restoration

4. "How would you add **multi-vendor support**?"
   → Vendor entity, split orders by vendor, separate payouts

5. "How to implement **real-time order tracking**?"
   → WebSocket for updates, delivery partner location updates

---

## Checklist Before Interview

- [ ] Can design Product → Cart → Order flow
- [ ] Know inventory management strategies
- [ ] Understand order status lifecycle
- [ ] Can handle pricing and discounts
- [ ] Know how to snapshot product in order
- [ ] Can explain cart expiry handling
- [ ] Understand multi-vendor order splitting
