# Design Food Delivery System (Swiggy/Zomato)

- [Design Food Delivery System](#design-food-delivery-system-swiggyzomato)
  - [Overview](#overview)
  - [Expectations](#expectations)
  - [Requirements Gathering](#requirements-gathering)
  - [Requirements](#requirements)
  - [Use Case Diagrams](#use-case-diagrams)
  - [Class Diagram](#class-diagram)
  - [Key Design Decisions](#key-design-decisions)
  - [API Design](#api-design)

---

## Overview

A food delivery system connects customers with restaurants, allowing them to browse menus, place orders, and have food delivered to their location. The system manages restaurants, menus, orders, payments, and delivery partners.

**Key Participants:**
- **Customer** - Browses, orders, pays
- **Restaurant** - Lists menu, prepares food
- **Delivery Partner** - Picks up and delivers
- **Platform** - Orchestrates everything

---

## Expectations

* Code should be functionally correct.
* Code should be modular and readable. Clean and professional level code.
* Code should be extensible and scalable. Means it should be able to accommodate new requirements with minimal changes.
* Code should have good OOP design principles.

---

## Requirements Gathering

What are some questions you would ask to gather requirements?

```
1.
2.
3.
4.
5.
```

<details>
<summary><strong>Sample clarifying questions</strong></summary>

1. How is restaurant search/discovery done?
2. Can customers order from multiple restaurants in one order?
3. How is delivery fee calculated?
4. Can items be customized? (extra cheese, no onion)
5. How are delivery partners assigned?
6. What payment methods are supported?
7. Can orders be scheduled for later?
8. How are ratings/reviews handled?

</details>

---

## Requirements

What will be 10 requirements of the system, according to you?

```
1.
2.
3.
4.
5.
6.
7.
8.
9.
10.
```

<details>
<summary><strong>Click to see the actual requirements</strong></summary>

1. Customers can search/browse nearby restaurants.
2. Restaurants have menus with items and prices.
3. Customers can add items to cart.
4. Customers can place orders with delivery address.
5. Orders have status tracking (Placed → Accepted → Preparing → Out for delivery → Delivered).
6. System assigns delivery partner to orders.
7. Customers can pay via multiple methods.
8. Restaurants can accept/reject orders.
9. Delivery partners can update delivery status.
10. Customers and restaurants can rate each other.

</details>

---

## Use Case Diagrams

### Actors

What would be the actors in this system?

```
1.
2.
3.
4.
```

### Use Cases

#### Actor 1: Customer

Use cases:
```
1.
2.
3.
4.
5.
```

#### Actor 2: Restaurant

Use cases:
```
1.
2.
3.
4.
```

#### Actor 3: Delivery Partner

Use cases:
```
1.
2.
3.
```

---

## Class Diagram

What will be the major classes and their attributes?

**Think about:**
- How to model restaurant and its menu?
- How to handle item customizations?
- What is the order lifecycle?
- How to track delivery?

List down your classes:

```
Class 1:

Class 2:

Class 3:

Class 4:

Class 5:

Class 6:

Class 7:
```

**Design Question: Cart vs Order**
```
How are Cart and Order different? When does Cart become Order?

Your thoughts:

```

Draw the class diagram:

```




```

---

## Key Design Decisions

**1. Order Status State Machine**
```
Draw the order states and transitions:

```

**2. How to assign delivery partners?**
```
Your approach:

```

**3. How to handle order from unavailable restaurant?**
```
Your approach:

```

---

## API Design

What APIs would you design for each actor?

**Customer APIs:**
```
1.
2.
3.
4.
```

**Restaurant APIs:**
```
1.
2.
3.
```

**Delivery Partner APIs:**
```
1.
2.
```

---

## Hints

<details>
<summary><strong>Hint 1: Restaurant & Menu</strong></summary>

```
┌─────────────────────┐       ┌─────────────────────┐
│     Restaurant      │       │        Menu         │
├─────────────────────┤       ├─────────────────────┤
│ - id                │       │ - id                │
│ - name              │       │ - restaurant_id     │
│ - address           │ 1:1   │ - categories[]      │
│ - is_open           │──────▶│                     │
│ - rating            │       └─────────────────────┘
│ - cuisines[]        │                │
│ - delivery_radius   │                ▼
└─────────────────────┘       ┌─────────────────────┐
                              │    MenuCategory     │
                              ├─────────────────────┤
                              │ - name (Starters,   │
                              │   Mains, Desserts)  │
                              │ - items[]           │
                              └─────────────────────┘
                                       │
                                       ▼
                              ┌─────────────────────┐
                              │     MenuItem        │
                              ├─────────────────────┤
                              │ - id                │
                              │ - name              │
                              │ - price             │
                              │ - is_available      │
                              │ - is_veg            │
                              │ - customizations[]  │
                              └─────────────────────┘
```

</details>

<details>
<summary><strong>Hint 2: Order Status Flow</strong></summary>

```
PLACED → ACCEPTED → PREPARING → READY → PICKED_UP → DELIVERED
   │         │
   ▼         ▼
CANCELLED  REJECTED

class OrderStatus(Enum):
    PLACED = "placed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    PREPARING = "preparing"
    READY = "ready"
    PICKED_UP = "picked_up"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
```

</details>

<details>
<summary><strong>Hint 3: Order Structure</strong></summary>

```python
class Order:
    id: str
    customer_id: str
    restaurant_id: str
    items: List[OrderItem]
    status: OrderStatus
    delivery_partner_id: Optional[str]
    delivery_address: Address
    subtotal: int
    delivery_fee: int
    taxes: int
    total: int
    placed_at: datetime
    estimated_delivery: datetime
    actual_delivery: Optional[datetime]

class OrderItem:
    menu_item_id: str
    name: str  # Snapshot!
    price: int  # Snapshot!
    quantity: int
    customizations: List[str]
    item_total: int
```

**Why snapshot name/price?**
- Menu item price can change
- Order should reflect price at time of ordering

</details>

<details>
<summary><strong>Hint 4: Delivery Partner Assignment</strong></summary>

```python
class DeliveryPartnerService:
    def find_partner(self, restaurant_location, delivery_location):
        # 1. Get available partners near restaurant
        available = self.get_available_partners_near(restaurant_location)

        # 2. Filter by those who can reach in time
        suitable = [p for p in available
                   if p.can_deliver_to(delivery_location)]

        # 3. Rank by proximity/rating
        ranked = sorted(suitable, key=lambda p: p.distance_from(restaurant_location))

        # 4. Return best match
        return ranked[0] if ranked else None
```

</details>

<details>
<summary><strong>Hint 5: API Design</strong></summary>

```
# Customer
GET  /restaurants?lat=12.9&lng=77.5&cuisine=Indian
GET  /restaurants/{id}/menu
POST /cart/items                    # Add to cart
POST /orders                        # Place order
GET  /orders/{id}                   # Track order
POST /orders/{id}/rate              # Rate order

# Restaurant
GET  /restaurant/orders             # Incoming orders
PUT  /restaurant/orders/{id}/accept
PUT  /restaurant/orders/{id}/ready

# Delivery Partner
GET  /delivery/orders               # Available orders
PUT  /delivery/orders/{id}/pickup
PUT  /delivery/orders/{id}/delivered
```

</details>
