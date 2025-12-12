# BookMyShow API Documentation

## Table of Contents
1. [Authentication](#authentication)
2. [User APIs](#user-apis)
3. [City & Theater APIs](#city--theater-apis)
4. [Movie APIs](#movie-apis)
5. [Show APIs](#show-apis)
6. [Booking APIs](#booking-apis)
7. [Error Handling](#error-handling)

---

## Base URL

```
Development: http://localhost:8000/api/
Production: https://api.bookmyshow.com/api/
```

---

## Authentication

Most endpoints require authentication using Token/Session.

### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "john_doe",
    "password": "password123"
}
```

**Response**:
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com"
    }
}
```

### Include Token in Requests
```http
Authorization: Bearer 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

---

## User APIs

### Register User

```http
POST /api/register/
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "password": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Response** (201 Created):
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "first_name": "John",
    "last_name": "Doe"
}
```

---

## City & Theater APIs

### List Cities

```http
GET /api/cities/
```

**Response**:
```json
[
    {
        "id": "mumbai",
        "name": "Mumbai",
        "theater_count": 15,
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": "delhi",
        "name": "Delhi",
        "theater_count": 12,
        "created_at": "2024-01-01T00:00:00Z"
    }
]
```

### Get City Details

```http
GET /api/cities/mumbai/
```

**Response**:
```json
{
    "id": "mumbai",
    "name": "Mumbai",
    "theater_count": 15,
    "created_at": "2024-01-01T00:00:00Z"
}
```

### List Theaters

```http
GET /api/theaters/
GET /api/theaters/?city=mumbai
GET /api/theaters/?search=PVR
```

**Response**:
```json
[
    {
        "id": "pvr-mumbai-1",
        "name": "PVR Juhu",
        "city_name": "Mumbai",
        "screen_count": 6
    },
    {
        "id": "inox-mumbai-1",
        "name": "INOX R-City",
        "city_name": "Mumbai",
        "screen_count": 8
    }
]
```

### Get Theater Details

```http
GET /api/theaters/pvr-mumbai-1/
```

**Response**:
```json
{
    "id": "pvr-mumbai-1",
    "name": "PVR Juhu",
    "address": "Juhu Tara Road, Mumbai",
    "city": "mumbai",
    "city_name": "Mumbai",
    "screens": [
        {
            "id": "screen-1",
            "name": "Audi 1",
            "seat_count": 100,
            "available_seat_types": ["GOLD", "PLATINUM"]
        }
    ],
    "screen_count": 6
}
```

---

## Movie APIs

### List Movies

```http
GET /api/movies/
GET /api/movies/?category=Action
GET /api/movies/?search=Avengers
```

**Response**:
```json
[
    {
        "id": "movie-1",
        "name": "Avengers: Endgame",
        "rating": 8.5,
        "category": "Action",
        "languages": ["English", "Hindi"],
        "languages_display": "English, Hindi",
        "duration": 181,
        "description": "After the devastating events...",
        "show_count": 15,
        "created_at": "2024-01-01T00:00:00Z"
    }
]
```

### Advanced Movie Search

```http
GET /api/movies/search/?query=avengers&city=mumbai&category=Action&language=English&min_rating=7.0
```

**Query Parameters**:
- `query`: Search in name/description
- `city`: Filter by city ID
- `category`: Filter by category
- `language`: Filter by language
- `min_rating`: Minimum rating

**Response**:
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "movie-1",
            "name": "Avengers: Endgame",
            "rating": 8.5,
            ...
        }
    ]
}
```

### Get Movie Details

```http
GET /api/movies/movie-1/
```

**Response**:
```json
{
    "id": "movie-1",
    "name": "Avengers: Endgame",
    "rating": 8.5,
    "category": "Action",
    "languages": ["English", "Hindi"],
    "languages_display": "English, Hindi",
    "duration": 181,
    "description": "After the devastating events of Avengers: Infinity War...",
    "show_count": 15,
    "created_at": "2024-01-01T00:00:00Z"
}
```

### Get Shows for Movie

```http
GET /api/movies/movie-1/shows/
GET /api/movies/movie-1/shows/?city=mumbai
GET /api/movies/movie-1/shows/?city=mumbai&date=2024-12-15
```

**Response**:
```json
[
    {
        "id": "show-1",
        "movie": "movie-1",
        "movie_name": "Avengers: Endgame",
        "movie_rating": 8.5,
        "theater": "pvr-mumbai-1",
        "theater_name": "PVR Juhu",
        "screen": "screen-1",
        "screen_name": "Audi 1",
        "city_name": "Mumbai",
        "start_time": "2024-12-15T18:00:00Z",
        "end_time": "2024-12-15T21:01:00Z",
        "cutoff_time": "2024-12-15T17:00:00Z",
        "duration": 181,
        "language": "English",
        "is_booking_allowed": true,
        "available_seats_count": 85
    }
]
```

---

## Show APIs

### List Shows

```http
GET /api/shows/
GET /api/shows/?movie=movie-1
GET /api/shows/?theater=pvr-mumbai-1
GET /api/shows/?language=English
```

**Response**:
```json
[
    {
        "id": "show-1",
        "movie": "movie-1",
        "movie_name": "Avengers: Endgame",
        "movie_rating": 8.5,
        "theater": "pvr-mumbai-1",
        "theater_name": "PVR Juhu",
        "screen": "screen-1",
        "screen_name": "Audi 1",
        "city_name": "Mumbai",
        "start_time": "2024-12-15T18:00:00Z",
        "end_time": "2024-12-15T21:01:00Z",
        "cutoff_time": "2024-12-15T17:00:00Z",
        "duration": 181,
        "language": "English",
        "is_booking_allowed": true,
        "available_seats_count": 85
    }
]
```

### Get Show Details with Seat Layout

```http
GET /api/shows/show-1/
```

**Response**:
```json
{
    "id": "show-1",
    "movie": "movie-1",
    "movie_name": "Avengers: Endgame",
    "movie_rating": 8.5,
    "theater": "pvr-mumbai-1",
    "theater_name": "PVR Juhu",
    "screen": "screen-1",
    "screen_name": "Audi 1",
    "city_name": "Mumbai",
    "start_time": "2024-12-15T18:00:00Z",
    "end_time": "2024-12-15T21:01:00Z",
    "cutoff_time": "2024-12-15T17:00:00Z",
    "duration": 181,
    "language": "English",
    "is_booking_allowed": true,
    "available_seats_count": 85,
    "show_seats": [
        {
            "id": "showseat-1",
            "seat": {
                "id": "seat-a1",
                "number": "A1",
                "seat_type": "GOLD"
            },
            "seat_number": "A1",
            "seat_type": "GOLD",
            "status": "AVAILABLE",
            "price": "250.00",
            "locked_at": null
        },
        {
            "id": "showseat-2",
            "seat": {
                "id": "seat-a2",
                "number": "A2",
                "seat_type": "GOLD"
            },
            "seat_number": "A2",
            "seat_type": "GOLD",
            "status": "BOOKED",
            "price": "250.00",
            "locked_at": null
        }
    ]
}
```

### Get Available Seats

```http
GET /api/shows/show-1/available_seats/
```

**Response**:
```json
[
    {
        "id": "showseat-1",
        "seat_number": "A1",
        "seat_type": "GOLD",
        "status": "AVAILABLE",
        "price": "250.00"
    },
    {
        "id": "showseat-3",
        "seat_number": "A3",
        "seat_type": "PLATINUM",
        "status": "AVAILABLE",
        "price": "350.00"
    }
]
```

---

## Booking APIs

### Book Tickets

**🔐 Requires Authentication**

```http
POST /api/book/
Authorization: Bearer <token>
Content-Type: application/json

{
    "show_id": "show-1",
    "seat_ids": ["showseat-1", "showseat-3"],
    "payment_mode": "UPI",
    "coupon_code": "DISCOUNT50"
}
```

**Request Fields**:
- `show_id` (required): Show ID
- `seat_ids` (required): Array of ShowSeat IDs (1-10 seats)
- `payment_mode` (required): `UPI`, `CREDIT_CARD`, or `NETBANKING`
- `coupon_code` (optional): Discount coupon code

**Response** (201 Created):
```json
{
    "ticket": {
        "id": "TKT-ABC123XYZ",
        "user_name": "john_doe",
        "movie_name": "Avengers: Endgame",
        "theater_name": "PVR Juhu",
        "screen_name": "Audi 1",
        "show_time": "2024-12-15T18:00:00Z",
        "amount": "550.00",
        "status": "BOOKED",
        "booking_time": "2024-12-15T12:30:00Z",
        "seats": [
            {
                "seat_number": "A1",
                "seat_type": "GOLD",
                "price": "250.00"
            },
            {
                "seat_number": "A3",
                "seat_type": "PLATINUM",
                "price": "350.00"
            }
        ],
        "payment": {
            "id": "PAY-XYZ789ABC",
            "amount": "550.00",
            "mode": "UPI",
            "status": "PENDING",
            "transaction_id": "TXN-1234567890ABCDEF",
            "timestamp": "2024-12-15T12:30:00Z"
        },
        "can_cancel": true
    },
    "payment_id": "PAY-XYZ789ABC",
    "total_amount": "550.00",
    "discount": "50.00",
    "message": "Booking successful! Please complete payment."
}
```

**Error Response** (400 Bad Request):
```json
{
    "error": "Seats not available: A1, A3"
}
```

### Confirm Payment

**🔐 Requires Authentication**

```http
POST /api/tickets/TKT-ABC123XYZ/confirm-payment/
Authorization: Bearer <token>
Content-Type: application/json

{
    "payment_success": true
}
```

**Response**:
```json
{
    "id": "TKT-ABC123XYZ",
    "status": "CONFIRMED",
    ...
}
```

### List User Tickets

**🔐 Requires Authentication**

```http
GET /api/tickets/
Authorization: Bearer <token>
```

**Response**:
```json
[
    {
        "id": "TKT-ABC123XYZ",
        "movie_name": "Avengers: Endgame",
        "show_time": "2024-12-15T18:00:00Z",
        "amount": "550.00",
        "status": "CONFIRMED",
        "booking_time": "2024-12-15T12:30:00Z",
        "seat_count": 2
    }
]
```

### Get Ticket Details

**🔐 Requires Authentication**

```http
GET /api/tickets/TKT-ABC123XYZ/
Authorization: Bearer <token>
```

**Response**:
```json
{
    "id": "TKT-ABC123XYZ",
    "user_name": "john_doe",
    "movie_name": "Avengers: Endgame",
    "theater_name": "PVR Juhu",
    "screen_name": "Audi 1",
    "show_time": "2024-12-15T18:00:00Z",
    "amount": "550.00",
    "status": "CONFIRMED",
    "booking_time": "2024-12-15T12:30:00Z",
    "seats": [
        {
            "seat_number": "A1",
            "seat_type": "GOLD",
            "price": "250.00"
        },
        {
            "seat_number": "A3",
            "seat_type": "PLATINUM",
            "price": "350.00"
        }
    ],
    "payment": {
        "id": "PAY-XYZ789ABC",
        "amount": "550.00",
        "mode": "UPI",
        "status": "SUCCESS",
        "transaction_id": "TXN-1234567890ABCDEF",
        "timestamp": "2024-12-15T12:30:00Z"
    },
    "can_cancel": true
}
```

### Cancel Ticket

**🔐 Requires Authentication**

```http
POST /api/tickets/TKT-ABC123XYZ/cancel/
Authorization: Bearer <token>
```

**Response**:
```json
{
    "id": "TKT-ABC123XYZ",
    "status": "CANCELLED",
    "payment": {
        "status": "REFUNDED",
        ...
    },
    ...
}
```

**Error Response** (400 Bad Request):
```json
{
    "error": "Cannot cancel: cutoff time passed or already cancelled"
}
```

---

## Additional APIs

### Validate Coupon

**🔐 Requires Authentication**

```http
POST /api/validate-coupon/
Authorization: Bearer <token>
Content-Type: application/json

{
    "coupon_code": "DISCOUNT50",
    "booking_amount": "600.00"
}
```

**Response** (Success):
```json
{
    "valid": true,
    "discount_type": "FIXED",
    "discount_value": "50.00",
    "min_amount": "500.00"
}
```

**Response** (Invalid):
```json
{
    "valid": false,
    "error": "Coupon is expired or inactive"
}
```

### Health Check

```http
GET /api/health/
```

**Response**:
```json
{
    "status": "ok",
    "service": "bookmyshow",
    "booking_service": "BookingServicePessimistic"
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful GET request |
| 201 | Created | Successful POST (booking created) |
| 400 | Bad Request | Invalid data, validation error |
| 401 | Unauthorized | Missing/invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | Server error |

### Error Response Format

```json
{
    "error": "Error message here"
}
```

Or for validation errors:

```json
{
    "field_name": ["Error message for this field"],
    "another_field": ["Another error message"]
}
```

### Common Errors

**Authentication Required**:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

**Validation Error**:
```json
{
    "seat_ids": ["This field is required."],
    "payment_mode": ["\"CASH\" is not a valid choice."]
}
```

**Business Logic Error**:
```json
{
    "error": "Booking not allowed. Cutoff time has passed."
}
```

---

## Pagination

List endpoints return paginated results:

```http
GET /api/movies/?page=2&page_size=20
```

**Response**:
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/movies/?page=3",
    "previous": "http://localhost:8000/api/movies/?page=1",
    "results": [...]
}
```

---

## Rate Limiting

(Not implemented in this version, but here's how it would work)

- **Limit**: 100 requests per minute per user
- **Headers**:
  - `X-RateLimit-Limit: 100`
  - `X-RateLimit-Remaining: 95`
  - `X-RateLimit-Reset: 1639564800`

---

## Example Workflows

### User Booking Flow

1. **Register** → `POST /api/register/`
2. **Login** → `POST /api/auth/login/` → Get token
3. **Browse Movies** → `GET /api/movies/search/?city=mumbai`
4. **Select Movie** → `GET /api/movies/movie-1/shows/?city=mumbai`
5. **View Seats** → `GET /api/shows/show-1/`
6. **Book Tickets** → `POST /api/book/`
7. **Complete Payment** → `POST /api/tickets/TKT-123/confirm-payment/`
8. **View Booking** → `GET /api/tickets/TKT-123/`

### Admin Flow

1. Add City → `POST /admin/` (via Django Admin)
2. Add Theater → `POST /admin/`
3. Add Screens & Seats → `POST /admin/`
4. Add Movie → `POST /admin/`
5. Add Shows → `POST /admin/`

---

## Summary

### Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/cities/` | GET | List cities |
| `/api/theaters/` | GET | List theaters |
| `/api/movies/search/` | GET | Search movies |
| `/api/movies/{id}/shows/` | GET | Get shows for movie |
| `/api/shows/{id}/` | GET | Get show with seat layout |
| `/api/book/` | POST | Book tickets |
| `/api/tickets/` | GET | List user tickets |
| `/api/tickets/{id}/cancel/` | POST | Cancel ticket |

### Authentication

- Most endpoints require authentication
- Use `Authorization: Bearer <token>` header
- Get token from login endpoint

### Data Flow

1. Search movies by city
2. Select movie and date
3. View shows for movie
4. Select show and view seats
5. Book seats
6. Complete payment
7. View/cancel tickets

---

This API documentation covers all the essential endpoints for the BookMyShow application!
