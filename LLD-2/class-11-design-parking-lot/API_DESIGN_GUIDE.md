# API Design and Best Practices Guide

A comprehensive guide to RESTful API design with examples from common Low-Level Design (LLD) case studies.

---

## Table of Contents
- [API Design Fundamentals](#api-design-fundamentals)
- [RESTful API Principles](#restful-api-principles)
- [HTTP Methods](#http-methods)
- [URL Design Best Practices](#url-design-best-practices)
- [Request and Response Design](#request-and-response-design)
- [Common LLD Case Study Examples](#common-lld-case-study-examples)
- [Error Handling](#error-handling)
- [Versioning](#versioning)
- [Authentication and Authorization](#authentication-and-authorization)

---

## API Design Fundamentals

APIs (Application Programming Interfaces) are contracts between different software components. Good API design ensures:
- **Clarity**: Easy to understand and use
- **Consistency**: Predictable patterns across endpoints
- **Flexibility**: Adaptable to various use cases
- **Efficiency**: Minimal overhead and fast responses
- **Security**: Protected against unauthorized access

---

## RESTful API Principles

REST (Representational State Transfer) is an architectural style for designing networked applications.

### Key Principles:
1. **Stateless**: Each request contains all information needed
2. **Client-Server**: Separation of concerns
3. **Cacheable**: Responses should indicate if they can be cached
4. **Uniform Interface**: Consistent naming and structure
5. **Layered System**: Architecture can be composed of layers

---

## HTTP Methods

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Retrieve resources | Yes | Yes |
| POST | Create new resources | No | No |
| PUT | Update/Replace entire resource | Yes | No |
| PATCH | Partial update of resource | No | No |
| DELETE | Remove resource | Yes | No |

### When to Use Each Method:

**GET**: Reading data without side effects
```
GET /users/123
GET /parking-lots?status=active
```

**POST**: Creating new resources
```
POST /users
POST /parking-lots/1/tickets
```

**PUT**: Complete replacement of a resource
```
PUT /users/123
PUT /parking-spots/456
```

**PATCH**: Partial updates
```
PATCH /users/123
PATCH /parking-spots/456/status
```

**DELETE**: Removing resources
```
DELETE /users/123
DELETE /parking-lots/1
```

---

## URL Design Best Practices

### 1. Use Nouns, Not Verbs
❌ Bad:
```
POST /create-user
GET /get-all-users
DELETE /delete-user/123
```

✅ Good:
```
POST /users
GET /users
DELETE /users/123
```

### 2. Use Plural Nouns for Collections
❌ Bad:
```
GET /user
GET /parking-spot
```

✅ Good:
```
GET /users
GET /parking-spots
```

### 3. Use Hyphens for Multi-Word Resources
❌ Bad:
```
/parkingspots
/paymentmethods
```

✅ Good:
```
/parking-spots
/payment-methods
```

### 4. Use Hierarchical Structure for Relationships
```
GET /parking-lots/1/floors
GET /parking-lots/1/floors/2/spots
GET /users/123/orders
GET /orders/456/items
```

### 5. Use Query Parameters for Filtering, Sorting, and Pagination
```
GET /users?role=admin&status=active
GET /parking-spots?floor=2&type=medium&status=available
GET /orders?sort=created_at&order=desc&page=2&limit=20
```

### 6. Keep URLs Lowercase
❌ Bad:
```
/Users/123/Orders
/ParkingLots
```

✅ Good:
```
/users/123/orders
/parking-lots
```

---

## Request and Response Design

### Request Body Structure

Use clear, descriptive field names in snake_case:

```json
{
  "license_plate": "KA01AB1234",
  "vehicle_type": "car",
  "entry_gate_id": "gate-1"
}
```

### Response Body Structure

Include metadata and consistent structure:

```json
{
  "status": "success",
  "data": {
    "ticket_id": "TKT-12345",
    "entry_time": "2024-12-04T10:30:00Z",
    "parking_spot": {
      "spot_id": "A-101",
      "floor_number": 1,
      "spot_type": "medium"
    }
  },
  "message": "Ticket issued successfully"
}
```

### Pagination Response

```json
{
  "status": "success",
  "data": [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"}
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "page_size": 20,
    "total_items": 200
  }
}
```

---

## Common LLD Case Study Examples

### 1. Parking Lot System

#### Admin APIs
```
# Parking Lot Management
POST   /parking-lots
GET    /parking-lots/{id}
GET    /parking-lots
PUT    /parking-lots/{id}
DELETE /parking-lots/{id}

# Floor Management
POST   /parking-lots/{lot_id}/floors
GET    /parking-lots/{lot_id}/floors
GET    /parking-lots/{lot_id}/floors/{floor_id}
PUT    /parking-lots/{lot_id}/floors/{floor_id}
DELETE /parking-lots/{lot_id}/floors/{floor_id}

# Spot Management
POST   /parking-spots
GET    /parking-spots?floor_id={id}&status={status}
PUT    /parking-spots/{id}
PATCH  /parking-spots/{id}/status
DELETE /parking-spots/{id}
```

#### Attendant APIs
```
# Ticket Management
POST   /tickets
GET    /tickets/{id}
GET    /tickets?status=active&entry_date={date}

# Slot Availability
GET    /parking-spots/available?vehicle_type={type}
GET    /parking-lots/{id}/availability

# Payment
POST   /payments
GET    /payments/{id}

# Checkout
POST   /checkout
```

#### Example Requests/Responses

**Issue Ticket**
```http
POST /tickets
Content-Type: application/json

{
  "license_plate": "KA01AB1234",
  "vehicle_type": "car",
  "entry_gate_id": "gate-1"
}

Response: 201 Created
{
  "status": "success",
  "data": {
    "ticket_id": "TKT-12345",
    "entry_time": "2024-12-04T10:30:00Z",
    "parking_spot": {
      "spot_id": "A-101",
      "floor_number": 1,
      "spot_type": "medium"
    },
    "vehicle": {
      "license_plate": "KA01AB1234",
      "vehicle_type": "car"
    }
  }
}
```

**Checkout**
```http
POST /checkout
Content-Type: application/json

{
  "ticket_id": "TKT-12345",
  "exit_gate_id": "gate-2",
  "payment": {
    "method": "upi",
    "amount": 130.00
  }
}

Response: 200 OK
{
  "status": "success",
  "data": {
    "invoice_id": "INV-67890",
    "ticket_id": "TKT-12345",
    "entry_time": "2024-12-04T10:30:00Z",
    "exit_time": "2024-12-04T12:45:00Z",
    "duration_hours": 2.25,
    "amount": 130.00,
    "payment_status": "completed"
  }
}
```

---

### 2. Library Management System

```
# Book Management
POST   /books
GET    /books
GET    /books/{id}
PUT    /books/{id}
DELETE /books/{id}
GET    /books?title={title}&author={author}&available=true

# Member Management
POST   /members
GET    /members/{id}
PUT    /members/{id}
DELETE /members/{id}

# Borrowing Operations
POST   /borrows
GET    /borrows?member_id={id}&status=active
PUT    /borrows/{id}/return

# Reservations
POST   /reservations
GET    /reservations?member_id={id}
DELETE /reservations/{id}
```

**Example: Borrow a Book**
```http
POST /borrows
Content-Type: application/json

{
  "member_id": "MEM-123",
  "book_id": "BK-456"
}

Response: 201 Created
{
  "status": "success",
  "data": {
    "borrow_id": "BRW-789",
    "member_id": "MEM-123",
    "book_id": "BK-456",
    "borrow_date": "2024-12-04",
    "due_date": "2024-12-18",
    "status": "active"
  }
}
```

---

### 3. Hotel Booking System

```
# Room Management
POST   /hotels/{hotel_id}/rooms
GET    /hotels/{hotel_id}/rooms
GET    /hotels/{hotel_id}/rooms/{room_id}
PUT    /hotels/{hotel_id}/rooms/{room_id}

# Search and Availability
GET    /hotels/{hotel_id}/rooms/available?check_in={date}&check_out={date}&room_type={type}

# Booking Management
POST   /bookings
GET    /bookings/{id}
GET    /bookings?guest_id={id}&status=confirmed
PATCH  /bookings/{id}/cancel

# Payment
POST   /bookings/{id}/payments
GET    /bookings/{id}/payments
```

**Example: Search Available Rooms**
```http
GET /hotels/HTL-001/rooms/available?check_in=2024-12-10&check_out=2024-12-12&room_type=deluxe

Response: 200 OK
{
  "status": "success",
  "data": [
    {
      "room_id": "RM-101",
      "room_number": "101",
      "room_type": "deluxe",
      "price_per_night": 5000,
      "amenities": ["wifi", "tv", "ac"]
    },
    {
      "room_id": "RM-102",
      "room_number": "102",
      "room_type": "deluxe",
      "price_per_night": 5000,
      "amenities": ["wifi", "tv", "ac", "balcony"]
    }
  ]
}
```

---

### 4. E-Commerce System

```
# Product Management
POST   /products
GET    /products
GET    /products/{id}
PUT    /products/{id}
DELETE /products/{id}
GET    /products?category={cat}&price_min={min}&price_max={max}

# Cart Management
POST   /carts/{cart_id}/items
GET    /carts/{cart_id}
PUT    /carts/{cart_id}/items/{item_id}
DELETE /carts/{cart_id}/items/{item_id}

# Order Management
POST   /orders
GET    /orders/{id}
GET    /orders?user_id={id}&status=pending
PATCH  /orders/{id}/status

# Inventory
GET    /products/{id}/inventory
PATCH  /products/{id}/inventory
```

**Example: Add Item to Cart**
```http
POST /carts/CART-123/items
Content-Type: application/json

{
  "product_id": "PROD-456",
  "quantity": 2
}

Response: 201 Created
{
  "status": "success",
  "data": {
    "cart_id": "CART-123",
    "items": [
      {
        "product_id": "PROD-456",
        "product_name": "Wireless Mouse",
        "quantity": 2,
        "unit_price": 599.00,
        "total_price": 1198.00
      }
    ],
    "cart_total": 1198.00
  }
}
```

---

### 5. Ride-Sharing System (Uber/Ola)

```
# Driver Management
POST   /drivers
GET    /drivers/{id}
PATCH  /drivers/{id}/location
PATCH  /drivers/{id}/status

# Ride Management
POST   /rides
GET    /rides/{id}
GET    /rides?rider_id={id}&status=completed
PATCH  /rides/{id}/accept
PATCH  /rides/{id}/start
PATCH  /rides/{id}/complete
PATCH  /rides/{id}/cancel

# Matching
POST   /rides/request
GET    /drivers/nearby?lat={lat}&lng={lng}&radius={km}

# Fare Calculation
POST   /fares/estimate
GET    /rides/{id}/fare
```

**Example: Request a Ride**
```http
POST /rides/request
Content-Type: application/json

{
  "rider_id": "RDR-123",
  "pickup_location": {
    "latitude": 12.9716,
    "longitude": 77.5946,
    "address": "MG Road, Bangalore"
  },
  "dropoff_location": {
    "latitude": 12.9352,
    "longitude": 77.6245,
    "address": "Indiranagar, Bangalore"
  },
  "ride_type": "sedan"
}

Response: 201 Created
{
  "status": "success",
  "data": {
    "ride_id": "RIDE-789",
    "status": "searching",
    "estimated_fare": {
      "min": 180,
      "max": 220
    },
    "estimated_time": "5-7 minutes"
  }
}
```

---

### 6. Food Delivery System (Swiggy/Zomato)

```
# Restaurant Management
POST   /restaurants
GET    /restaurants
GET    /restaurants/{id}
GET    /restaurants/{id}/menu

# Menu Management
POST   /restaurants/{id}/menu-items
PUT    /restaurants/{id}/menu-items/{item_id}
PATCH  /restaurants/{id}/menu-items/{item_id}/availability

# Order Management
POST   /orders
GET    /orders/{id}
PATCH  /orders/{id}/status

# Delivery Management
GET    /delivery-partners/available?location={loc}
PATCH  /orders/{id}/assign-delivery-partner
PATCH  /delivery-partners/{id}/location
```

**Example: Place Order**
```http
POST /orders
Content-Type: application/json

{
  "customer_id": "CUST-123",
  "restaurant_id": "REST-456",
  "items": [
    {
      "item_id": "ITEM-789",
      "quantity": 2,
      "customizations": ["extra cheese", "no onions"]
    }
  ],
  "delivery_address": {
    "street": "123 Main St",
    "city": "Bangalore",
    "zipcode": "560001"
  },
  "payment_method": "upi"
}

Response: 201 Created
{
  "status": "success",
  "data": {
    "order_id": "ORD-999",
    "status": "placed",
    "estimated_delivery_time": "30-40 minutes",
    "total_amount": 450.00
  }
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource |
| 422 | Unprocessable Entity | Validation errors |
| 500 | Internal Server Error | Server error |

### Error Response Format

```json
{
  "status": "error",
  "error": {
    "code": "INVALID_INPUT",
    "message": "Vehicle type is required",
    "details": {
      "field": "vehicle_type",
      "constraint": "required"
    }
  }
}
```

### Validation Errors

```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "license_plate",
        "message": "Invalid format"
      },
      {
        "field": "vehicle_type",
        "message": "Must be one of: car, bike, truck"
      }
    ]
  }
}
```

---

## Versioning

### URL Versioning (Recommended)
```
GET /v1/users
GET /v2/users
```

### Header Versioning
```http
GET /users
Accept: application/vnd.api.v1+json
```

### Query Parameter Versioning
```
GET /users?version=1
```

---

## Authentication and Authorization

### Token-Based (JWT)

```http
POST /auth/login
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "password123"
}

Response:
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
```

### Using Token in Requests

```http
GET /users/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### API Key Authentication

```http
GET /parking-spots
X-API-Key: your-api-key-here
```

---

## Additional Best Practices

### 1. Use HTTPS
Always use HTTPS in production to encrypt data in transit.

### 2. Rate Limiting
```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1701693600
```

### 3. CORS Headers
```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
```

### 4. Compression
```http
Accept-Encoding: gzip, deflate
Content-Encoding: gzip
```

### 5. Caching
```http
Cache-Control: max-age=3600
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
```

### 6. Documentation
Use tools like:
- **Swagger/OpenAPI**: Interactive API documentation
- **Postman Collections**: Shareable API examples
- **README files**: Quick reference guides

---

## Python Implementation Example

Here's a quick example using Flask:

```python
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Sample data store
tickets = {}

@app.route('/tickets', methods=['POST'])
def issue_ticket():
    """Issue a new parking ticket"""
    data = request.get_json()
    
    # Validation
    if not data.get('license_plate'):
        return jsonify({
            'status': 'error',
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'license_plate is required'
            }
        }), 400
    
    # Create ticket
    ticket_id = f"TKT-{len(tickets) + 1}"
    ticket = {
        'ticket_id': ticket_id,
        'license_plate': data['license_plate'],
        'vehicle_type': data.get('vehicle_type', 'car'),
        'entry_time': datetime.now().isoformat(),
        'status': 'active'
    }
    
    tickets[ticket_id] = ticket
    
    return jsonify({
        'status': 'success',
        'data': ticket
    }), 201

@app.route('/tickets/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    """Get ticket details"""
    ticket = tickets.get(ticket_id)
    
    if not ticket:
        return jsonify({
            'status': 'error',
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Ticket not found'
            }
        }), 404
    
    return jsonify({
        'status': 'success',
        'data': ticket
    }), 200

@app.route('/tickets', methods=['GET'])
def get_all_tickets():
    """Get all tickets with optional filtering"""
    status = request.args.get('status')
    
    filtered_tickets = tickets.values()
    
    if status:
        filtered_tickets = [
            t for t in filtered_tickets 
            if t['status'] == status
        ]
    
    return jsonify({
        'status': 'success',
        'data': list(filtered_tickets)
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Summary Checklist

When designing APIs, ensure:

- ✅ Use nouns for resources, not verbs
- ✅ Use plural nouns for collections
- ✅ Use appropriate HTTP methods
- ✅ Use hierarchical URLs for relationships
- ✅ Use query parameters for filtering/sorting/pagination
- ✅ Return appropriate status codes
- ✅ Include clear error messages
- ✅ Use consistent naming conventions (snake_case)
- ✅ Version your APIs
- ✅ Document your APIs
- ✅ Implement authentication/authorization
- ✅ Use HTTPS in production
- ✅ Implement rate limiting
- ✅ Handle errors gracefully

---

## Common Mistakes and Nuances

### 1. PUT vs PATCH - The Most Common Confusion

Many developers use PUT and PATCH interchangeably, but they have very different semantics.

**PUT: Complete Replacement**
- Replaces the **entire resource** with the request body
- All fields must be provided (even unchanged ones)
- Idempotent: Multiple identical requests have the same effect
- If you omit a field, it will be set to null/default

**PATCH: Partial Update**
- Updates **only the fields** provided in the request
- Other fields remain unchanged
- Not necessarily idempotent (depends on implementation)
- Only send the fields you want to change

#### Example Scenario: Updating a User Profile

**Original Resource:**
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+91-9876543210",
  "address": "123 Main St",
  "status": "active"
}
```

**Using PUT (Complete Replacement):**
```http
PUT /users/123
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+91-9876543210",
  "address": "123 Main St",
  "status": "active"
}
```
❌ **Problem**: You must send ALL fields, even if you only want to change the email. If you forget a field:

```http
PUT /users/123
{
  "email": "john.doe@example.com"
}
```
**Result**: All other fields (name, phone, address, status) will be set to null/default!

**Using PATCH (Partial Update):**
```http
PATCH /users/123
Content-Type: application/json

{
  "email": "john.doe@example.com"
}
```
✅ **Correct**: Only email is updated, all other fields remain unchanged.

#### When to Use What:

| Scenario | Use | Example |
|----------|-----|---------|
| Updating email only | PATCH | `PATCH /users/123` |
| Updating status only | PATCH | `PATCH /parking-spots/456/status` |
| Replacing entire profile | PUT | `PUT /users/123` |
| Toggle feature flags | PATCH | `PATCH /users/123/preferences` |
| Complete resource edit | PUT | `PUT /products/789` |

#### Common Mistake in Parking Lot System:
```http
# ❌ WRONG: Using PUT for partial updates
PUT /parking-spots/456/status
{
  "status": "OCCUPIED"
}
# This might erase spot_number, spot_type, and other fields!

# ✅ CORRECT: Use PATCH for partial updates
PATCH /parking-spots/456/status
{
  "status": "OCCUPIED"
}
```

**Real Example from Django REST Framework:**
```python
# PUT handler - expects all fields
def put(self, request, pk):
    spot = ParkingSpot.objects.get(pk=pk)
    serializer = ParkingSpotSerializer(spot, data=request.data)  # Full validation
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

# PATCH handler - accepts partial data
def patch(self, request, pk):
    spot = ParkingSpot.objects.get(pk=pk)
    serializer = ParkingSpotSerializer(spot, data=request.data, partial=True)  # Partial validation
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
```

---

### 2. GET with Request Body vs POST - When Query Params Are Too Many

**The Problem:**
- URLs have length limits (~2000-8000 characters depending on browser/server)
- Complex filters with many parameters exceed this limit
- Query strings become unreadable: `?param1=value1&param2=value2&param3=value3...`
- Arrays in query params are messy: `?ids=1&ids=2&ids=3` or `?ids=1,2,3`

#### Three Possible Solutions:

#### Option 1: GET with Request Body (NOT Recommended)

```http
GET /products/search
Content-Type: application/json

{
  "filters": {
    "category": "electronics",
    "brands": ["apple", "samsung", "sony"],
    "price_range": {"min": 10000, "max": 50000}
  }
}
```

**❌ Problems:**
- HTTP spec allows it, but many tools/libraries don't support it
- Axios ignores GET body by default
- Many proxies/caches strip GET request bodies
- Semantically confusing (GET should be "safe" and not have a body)
- Can't bookmark or share the URL

**Tools that DON'T support GET with body:**
- Most browsers (in forms)
- Many HTTP clients (Postman shows warnings)
- CDNs and caching layers
- AWS API Gateway (rejects it)

#### Option 2: POST Instead of GET (Recommended)

```http
POST /products/search
Content-Type: application/json

{
  "category": "electronics",
  "subcategory": "laptops",
  "brands": ["apple", "dell", "hp", "lenovo", "asus", "acer"],
  "price_range": {
    "min": 30000,
    "max": 150000
  },
  "features": ["ssd", "16gb_ram", "dedicated_gpu", "backlit_keyboard"],
  "ratings": [4, 5],
  "availability": "in_stock",
  "sellers": ["amazon", "flipkart", "croma"],
  "sort": {
    "field": "price",
    "order": "asc"
  },
  "pagination": {
    "page": 1,
    "limit": 20
  }
}
```

**✅ Benefits:**
- Widely supported
- No URL length limits
- Clean and readable
- Can handle complex nested structures
- Works with all HTTP clients

**⚠️ Trade-offs:**
- POST requests aren't cached by default
- Can't bookmark/share URLs easily
- Not semantically pure REST (POST implies creation)

**How to handle caching:**
```http
POST /products/search
Cache-Control: max-age=300

# Or use request ID for caching
POST /products/search
{
  "request_id": "hash_of_search_params",  # For cache key
  "filters": {...}
}
```

#### Option 3: Hybrid Approach

```http
# Simple search: Use GET
GET /products?category=electronics&price_max=50000

# Complex search: Use POST
POST /products/search
{
  "complex_filters": {...}
}
```

#### Popular Real-World Examples:

**1. Elasticsearch (Most Famous Example)**
```http
# Elasticsearch uses POST for search (not GET)
POST /products/_search
Content-Type: application/json

{
  "query": {
    "bool": {
      "must": [
        {"match": {"category": "electronics"}},
        {"range": {"price": {"gte": 10000, "lte": 50000}}}
      ],
      "filter": {
        "terms": {"brand": ["apple", "samsung", "sony"]}
      }
    }
  },
  "sort": [{"price": "asc"}],
  "size": 20,
  "from": 0
}
```
**Why Elasticsearch chose POST:**
- Complex query DSL with nested objects
- URL would be thousands of characters long
- Better developer experience

**2. Google APIs (Gmail, Drive)**
```http
# Gmail API uses POST for complex searches
POST https://gmail.googleapis.com/gmail/v1/users/me/messages
{
  "q": "from:example@gmail.com has:attachment newer_than:2d",
  "maxResults": 100,
  "labelIds": ["INBOX", "IMPORTANT"]
}
```

**3. Microsoft Graph API**
```http
# Complex filtering uses POST
POST https://graph.microsoft.com/v1.0/users/query
{
  "filter": "startswith(displayName, 'J')",
  "select": ["displayName", "mail"],
  "top": 50
}
```

**4. GitHub GraphQL API**
```http
POST https://api.github.com/graphql
{
  "query": "query { viewer { repositories(first: 10) { nodes { name } } } }"
}
```

**5. Stripe API (Payment Filtering)**
```http
POST /v1/charges/search
{
  "query": "amount>999 AND status:'succeeded'",
  "limit": 100
}
```

#### Practical Guideline:

| Query Complexity | Use | Example |
|-----------------|-----|---------|
| 1-3 simple params | GET with query params | `GET /products?category=electronics&status=active` |
| 4-6 params, no arrays | GET with query params | `GET /users?role=admin&status=active&sort=name` |
| Multiple arrays or nested objects | POST with body | `POST /products/search` with filters object |
| More than ~100 chars in URL | POST with body | Complex searches |
| Need to bookmark/cache | GET (try to simplify) | Public search pages |
| Internal API, complex filters | POST | Elasticsearch-style queries |

#### Implementation Example:

```python
# Flask example supporting both approaches
from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple search with GET
@app.route('/products', methods=['GET'])
def search_products_simple():
    category = request.args.get('category')
    max_price = request.args.get('price_max')

    # Simple filtering
    products = filter_products(category=category, max_price=max_price)
    return jsonify(products)

# Complex search with POST
@app.route('/products/search', methods=['POST'])
def search_products_complex():
    data = request.get_json()

    # Extract complex filters
    filters = data.get('filters', {})
    sort = data.get('sort', {})
    pagination = data.get('pagination', {})

    # Complex filtering logic
    products = complex_filter_products(
        filters=filters,
        sort=sort,
        pagination=pagination
    )

    return jsonify({
        'data': products,
        'pagination': {...}
    })

# Batch retrieval with POST
@app.route('/products/batch', methods=['POST'])
def get_products_batch():
    data = request.get_json()
    product_ids = data.get('product_ids', [])

    # ❌ Bad: GET /products?ids=1,2,3,4,5,6,7,8,9,10,11,12...
    # ✅ Good: POST /products/batch with array in body

    products = get_products_by_ids(product_ids)
    return jsonify(products)
```

#### Best Practice Summary:

1. **Start with GET + query params** for simple cases
2. **Switch to POST when:**
   - URL exceeds ~200 characters
   - Need to pass arrays of 5+ items
   - Need nested filter objects
   - Building an Elasticsearch-like search API
3. **Never use GET with request body** (compatibility nightmare)
4. **Name POST search endpoints clearly:** `/search`, `/_search`, `/query`, `/filter`
5. **Document the deviation** from pure REST principles
6. **Consider caching implications** when using POST

---

### 3. Other Important Nuances

#### 3.1. DELETE with Request Body (Controversial)

**The Problem:**
- HTTP spec technically allows DELETE with a body
- But many frameworks, proxies, and clients ignore or reject it
- Creates portability issues

**❌ Problematic:**
```http
DELETE /users/123
Content-Type: application/json

{
  "reason": "Requested by user",
  "backup_data": true
}
```
**Why it fails:** Many HTTP clients (Axios, Fetch API), proxies (Nginx, CloudFlare), and frameworks (some versions of Express) ignore DELETE bodies.

**✅ Better Alternatives:**

**Option 1: Query Parameters (Simple Cases)**
```http
DELETE /users/123?reason=user_requested&backup=true
```

**Option 2: POST for Complex Deletes**
```http
POST /users/123/delete
{
  "reason": "Requested by user",
  "backup_data": true,
  "notify_admins": true
}
```

**Option 3: PATCH to Mark as Deleted (Soft Delete)**
```http
PATCH /users/123
{
  "status": "deleted",
  "deleted_at": "2024-12-05T10:30:00Z",
  "deletion_reason": "Requested by user"
}
```

#### 3.2. Idempotency Matters

**Idempotent**: Calling the same request multiple times produces the same result as calling it once.

| Method | Idempotent? | Example |
|--------|-------------|---------|
| GET | ✅ Yes | Reading doesn't change state |
| PUT | ✅ Yes | Replacing with same data = same result |
| PATCH | ⚠️ **Maybe** | Depends on implementation |
| POST | ❌ No | Creates new resource each time |
| DELETE | ✅ Yes | Deleting already-deleted = still deleted |

**Common Mistake with PATCH (Non-Idempotent):**
```http
# ❌ NOT Idempotent - adds 100 each time!
PATCH /users/123/wallet
{
  "operation": "add",
  "amount": 100
}
# First call: balance = 1100
# Second call: balance = 1200 (DIFFERENT RESULT!)
```

**✅ Idempotent PATCH:**
```http
PATCH /users/123/wallet
{
  "operation": "set",
  "balance": 1100
}
# First call: balance = 1100
# Second call: balance = 1100 (SAME RESULT!)
```

**Parking Lot Example:**
```http
# ❌ Non-idempotent
PATCH /parking-spots/123
{
  "increment_usage_count": 1
}

# ✅ Idempotent
PATCH /parking-spots/123
{
  "status": "OCCUPIED",
  "occupied_at": "2024-12-05T10:30:00Z"
}
```

#### 3.3. Nested Resources - How Deep Should You Go?

**❌ Too Deep (Bad):**
```http
GET /parking-lots/1/floors/2/spots/3/tickets/4/payments/5
```
**Problems:**
- Hard to maintain
- Difficult to understand
- Creating a spot requires knowing lot → floor → spot hierarchy
- What if you only have payment ID?

**✅ Better (Flat with Query Params):**
```http
GET /parking-lots/1
GET /floors?parking_lot_id=1
GET /spots?floor_id=2
GET /tickets?spot_id=3
GET /payments?ticket_id=4

# Direct access when you have ID
GET /payments/5
```

**Rule of Thumb:**
- **Max 2 levels** for nested resources: `/parking-lots/1/floors`
- Use **query parameters** beyond that: `/spots?floor_id=2`
- **Direct access** should always be available: `/spots/123`

#### 3.4. Batch/Bulk Operations

**Creating Multiple Resources:**
```http
POST /parking-spots/batch
{
  "spots": [
    {"spot_number": 1, "spot_type": "SMALL", "floor_id": 2},
    {"spot_number": 2, "spot_type": "MEDIUM", "floor_id": 2},
    {"spot_number": 3, "spot_type": "LARGE", "floor_id": 2}
  ]
}

Response: 201 Created
{
  "status": "partial_success",
  "successful": [
    {"id": 101, "spot_number": 1},
    {"id": 102, "spot_number": 2}
  ],
  "failed": [
    {
      "spot_number": 3,
      "error": "Spot number already exists"
    }
  ]
}
```

**Fetching Multiple Resources by IDs:**
```http
# ❌ Bad: GET /users?ids=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15...
# URL becomes too long with 100+ IDs

# ✅ Good: POST for batch retrieval
POST /users/batch-get
{
  "user_ids": [1, 2, 3, 4, 5, ..., 100]
}
```

#### 3.5. Long-Running/Async Operations

When operations take time (reports, data processing, video transcoding):

**Pattern: 202 Accepted + Status Polling**
```http
# Initial request
POST /reports/monthly
{
  "month": "2024-12",
  "format": "pdf"
}

# Response: 202 Accepted
{
  "status": "processing",
  "job_id": "JOB-12345",
  "status_url": "/jobs/JOB-12345",
  "estimated_completion_time": "2 minutes"
}

# Poll status
GET /jobs/JOB-12345

# While processing
{
  "status": "processing",
  "progress": 45,
  "message": "Generating charts..."
}

# When complete
{
  "status": "completed",
  "result_url": "/reports/monthly-2024-12.pdf",
  "download_url": "/downloads/JOB-12345"
}

# If failed
{
  "status": "failed",
  "error": "Insufficient data for report generation"
}
```

**Use Cases:**
- Report generation
- Data export (CSV, PDF)
- Video/image processing
- Batch operations
- Complex calculations

#### 3.6. File Uploads - Size Matters

**Small Files (<5MB): Base64 in JSON**
```http
POST /users/123/avatar
{
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
}
```
✅ Pros: Simple, works with JSON APIs
❌ Cons: 33% size increase, not suitable for large files

**Medium Files (5-50MB): Multipart Form Data**
```http
POST /documents
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="title"

Monthly Report
------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="report.pdf"
Content-Type: application/pdf

[binary data]
------WebKitFormBoundary--
```

**Large Files (>50MB): Presigned URLs**
```http
# Step 1: Get upload URL
POST /uploads/initiate
{
  "filename": "large_video.mp4",
  "content_type": "video/mp4",
  "size": 524288000
}

# Response
{
  "upload_url": "https://s3.amazonaws.com/bucket/key?signature=...",
  "upload_id": "UP-123",
  "expires_in": 3600
}

# Step 2: Upload directly to S3 (client-side)
PUT https://s3.amazonaws.com/bucket/key?signature=...
[binary data]

# Step 3: Confirm upload
POST /uploads/UP-123/complete
{
  "etag": "abc123..."
}
```

---

## Quick Reference: Common Mistakes

| Mistake | Wrong | Correct |
|---------|-------|---------|
| Partial update | `PUT /users/123` with partial data | `PATCH /users/123` with partial data |
| Complex search | `GET /products?many&long&params...` | `POST /products/search` with body |
| GET with body | `GET /search` + request body | `POST /search` with body |
| DELETE with body | `DELETE /users/1` + body | `DELETE /users/1?reason=...` or `POST /users/1/delete` |
| Too nested | `/lots/1/floors/2/spots/3/tickets/4` | `/tickets?spot_id=3` |
| Batch GET | `GET /users?ids=1,2,3,...,100` | `POST /users/batch-get` |
| Non-idempotent PATCH | `{"operation": "increment"}` | `{"operation": "set", "value": 100}` |

---

## Resources

- [RESTful API Design Best Practices](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Elasticsearch Search API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html) - Example of POST for search
- [Flask Documentation](https://flask.palletsprojects.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [HTTP/1.1 Specification (RFC 7231)](https://tools.ietf.org/html/rfc7231) - Official HTTP methods spec

---
