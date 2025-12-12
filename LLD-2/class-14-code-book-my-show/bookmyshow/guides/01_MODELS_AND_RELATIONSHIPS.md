# Django Models and Relationships Guide for LLD Interviews

## Table of Contents
1. [Django ORM Basics](#django-orm-basics)
2. [Relationship Types](#relationship-types)
3. [BookMyShow Model Design](#bookmyshow-model-design)
4. [Interview Gotchas](#interview-gotchas)
5. [Best Practices](#best-practices)

---

## Django ORM Basics

### What is ORM?
**Object-Relational Mapping** - Maps Python classes to database tables.

```python
# Python Class (Model)
class Movie(models.Model):
    name = models.CharField(max_length=200)
    rating = models.FloatField()

# Translates to SQL:
# CREATE TABLE movie (
#     id BIGINT PRIMARY KEY,
#     name VARCHAR(200),
#     rating FLOAT
# );
```

### Why ORM?
- Database agnostic (works with PostgreSQL, MySQL, SQLite, etc.)
- Prevents SQL injection
- Easier to maintain
- Type-safe

---

## Relationship Types

### 1. One-to-Many (ForeignKey)

**Concept**: One parent can have multiple children.

**Example**: City → Theater (One city has many theaters)

```python
class City(models.Model):
    name = models.CharField(max_length=100)

class Theater(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,     # Interview Question: What happens on delete?
        related_name='theaters'        # Interview Question: What is related_name?
    )
```
> **Note on `related_name`:**  
> `related_name` defines the **reverse relationship name** that Django creates on the parent model.  
>  
> In this example, setting `related_name='theaters'` allows accessing all theaters of a city using:
> ```python
> city.theaters.all()
> ```
>  
> If `related_name` is not specified, Django automatically creates a default reverse relation using the pattern:
> ```python
> city.theater_set.all()
> ```
>  
> Using `related_name` improves readability, avoids generic naming, and prevents conflicts when multiple foreign keys point to the same model.

**Database Representation**:
```
City Table:          Theater Table:
+----+----------+    +----+----------+---------+
| id | name     |    | id | name     | city_id |
+----+----------+    +----+----------+---------+
| 1  | Mumbai   |    | 1  | PVR      | 1       |
| 2  | Delhi    |    | 2  | INOX     | 1       |
+----+----------+    | 3  | Cinepol  | 2       |
                     +----+----------+---------+
```

**Usage**:
```python
# Forward access (child → parent)
theater = Theater.objects.get(id=1)
print(theater.city.name)  # "Mumbai"

# Reverse access (parent → children)
city = City.objects.get(id=1)
print(city.theaters.all())  # QuerySet of theaters in Mumbai
# Note: 'theaters' comes from related_name
```

**Interview Questions**:

**Q: What does `on_delete=models.CASCADE` mean?**
- **CASCADE**: Delete theaters when city is deleted
- **PROTECT**: Prevent city deletion if it has theaters
- **SET_NULL**: Set city_id to NULL (requires `null=True`)
- **SET_DEFAULT**: Set to default value

**Q: What if we don't specify `related_name`?**
- Default is `theater_set` (modelname_set)
- Example: `city.theater_set.all()`

### 2. One-to-One (OneToOneField)

**Concept**: Each record relates to exactly one record in another table.

**Example**: Ticket → Payment (One ticket has one payment)

```python
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Payment(models.Model):
    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
```
> **Why not use `ForeignKey(unique=True)` for 1:1 relationships?**  
>  
> While `ForeignKey(unique=True)` enforces a one-to-one constraint at the database level, Django still **treats it as a one-to-many relationship in the ORM**.  
>  
> This leads to:
> - Reverse access returning a **QuerySet** instead of a single object  
>   (`ticket.payment_set.all()` instead of `ticket.payment`)  
> - Extra `.first()` or `.get()` calls in application code  
> - Weaker expression of domain intent (it *looks* like 1:N, not 1:1)  
>  
> `OneToOneField` solves this by explicitly modeling a true 1:1 relationship, giving:
> - Clean reverse access (`ticket.payment`)  
> - Correct ORM semantics  
> - Clearer, self-documenting models  
>  
> **Use `OneToOneField` when one model is conceptually an extension of another.**

**Database Representation**:
```
Ticket Table:              Payment Table:
+----+------+--------+     +----+-----------+--------+-----------+
| id | user | amount |     | id | ticket_id | status | txn_id    |
+----+------+--------+     +----+-----------+--------+-----------+
| 1  | 10   | 500    |     | 1  | 1         | SUCCESS| TXN-123   |
| 2  | 11   | 300    |     | 2  | 2         | PENDING| TXN-456   |
+----+------+--------+     +----+-----------+--------+-----------+
```

**Usage**:
```python
ticket = Ticket.objects.get(id=1)
print(ticket.payment.status)  # "SUCCESS"

payment = Payment.objects.get(id=1)
print(payment.ticket.amount)  # 500
```

**Interview Question**:

**Q: OneToOne vs ForeignKey with unique=True?**
- Functionally similar
- OneToOne enforces uniqueness at DB level
- OneToOne returns object, ForeignKey with unique returns QuerySet
- Use OneToOne for semantic clarity (1:1 relationship)

### 3. Many-to-Many (ManyToManyField)

**Basic Many-to-Many**:

```python
class Movie(models.Model):
    name = models.CharField(max_length=200)
    actors = models.ManyToManyField('Actor')

class Actor(models.Model):
    name = models.CharField(max_length=100)
```

**Database Representation** (Django creates intermediary table):
```
Movie Table:           Movie_Actor Table:      Actor Table:
+----+-----------+     +----+----------+--------+    +----+-----------+
| id | name      |     | id | movie_id | actor_id|   | id | name      |
+----+-----------+     +----+----------+---------+   +----+-----------+
| 1  | Avengers  |     | 1  | 1        | 1       |   | 1  | RDJ       |
| 2  | Iron Man  |     | 2  | 1        | 2       |   | 2  | Chris     |
+----+-----------+     | 3  | 2        | 1       |   +----+-----------+
                       +----+----------+---------+
```

**Many-to-Many with Extra Fields (Through Model)**:

**Example**: Show ↔ Seat (Many shows have many seats, but each combination has extra data like price, status)

```python
class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    start_time = models.DateTimeField()

class Seat(models.Model):
    number = models.CharField(max_length=10)
    seat_type = models.CharField(max_length=20)

class ShowSeat(models.Model):  # Through model / Intermediary model
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Extra field!
    status = models.CharField(max_length=20)  # Extra field!

    class Meta:
        unique_together = ['show', 'seat']  # Composite unique constraint
```

**Usage**:
```python
# Get all ShowSeats for a show
show = Show.objects.get(id=1)
show_seats = show.showseat_set.all()

# Get available seats for a show
available_seats = ShowSeat.objects.filter(
    show=show,
    status='AVAILABLE'
)

# Book a seat
show_seat = ShowSeat.objects.get(show_id=1, seat_id=5)
show_seat.status = 'BOOKED'
show_seat.save()
```

**Interview Question**:

**Q: When to use Through model vs regular ManyToMany?**
- Use **Through model** when you need extra fields (price, status, timestamps)
- Use **ManyToMany** for simple associations (Movie ↔ Actor)

---

## BookMyShow Model Design

### Entity Relationship Overview

```
City (1) ──→ (N) Theater (1) ──→ (N) Screen (1) ──→ (N) Seat
                   ↓                      ↓
                  (N)                    (N)
                   ↓                      ↓
                 Show ←──────────────────┘
                   ↓ (1)
                  (N)
                   ↓
               ShowSeat ←── (N) TicketSeat ──→ (1) Ticket (1) ──→ (1) Payment
                                                     ↓
                                                    (N)
                                                     ↓
                                                   User
```

### Key Relationships

1. **City → Theater** (1:N)
   - One city has many theaters
   - ForeignKey in Theater

2. **Theater → Screen** (1:N)
   - One theater has many screens
   - ForeignKey in Screen

3. **Screen → Seat** (1:N)
   - One screen has many seats
   - ForeignKey in Seat

4. **Movie → Show** (1:N)
   - One movie has many shows
   - ForeignKey in Show

5. **Screen → Show** (1:N)
   - One screen has many shows
   - ForeignKey in Show

6. **Show ↔ Seat** (M:N with extra fields)
   - **Through model: ShowSeat**
   - Extra fields: price, status, locked_at

7. **Ticket ↔ ShowSeat** (M:N)
   - **Through model: TicketSeat**
   - One ticket can have multiple seats

8. **Ticket → Payment** (1:1)
   - One ticket has one payment
   - OneToOneField in Payment

### Design Decisions

**Q: Why separate Seat and ShowSeat?**
- **Seat**: Template/master data (permanent seat configuration)
- **ShowSeat**: Instance data (seat for specific show with dynamic price/status)
- Allows same seat to have different prices/availability for different shows

**Q: Why TicketSeat as Through model?**
- One ticket can book multiple seats
- Need to track which seats belong to which ticket
- Could have extra fields like individual seat cancellation

---

## Interview Gotchas

### 1. N+1 Query Problem

**Bad** (N+1 queries):
```python
# 1 query to get theaters
theaters = Theater.objects.all()

# N queries (one per theater to get city)
for theater in theaters:
    print(theater.city.name)  # Triggers query for each theater!
```

**Good** (2 queries):
```python
# Use select_related for ForeignKey
theaters = Theater.objects.select_related('city').all()

for theater in theaters:
    print(theater.city.name)  # No extra query!

```

**Interview Question**: *When to use `select_related` vs `prefetch_related`?*
- **select_related**: ForeignKey, OneToOne (SQL JOIN)
- **prefetch_related**: ManyToMany, reverse ForeignKey (separate queries)

> **Note on `select_related` vs `prefetch_related`:**  
>  
> `select_related` and `prefetch_related` are Django ORM optimizations used to avoid the N+1 query problem, but they work differently.
>  
> **select_related**
> - Uses a SQL JOIN
> - Fetches related objects in the same query
> - Best for `ForeignKey` and `OneToOneField`
> - Returns a single related object
>  
> Example:
> ```python
> Theater.objects.select_related('city').all()
> ```
>  
> **prefetch_related**
> - Executes separate queries
> - Joins data in Python memory
> - Best for `ManyToMany` and reverse `ForeignKey`
> - Avoids row duplication caused by JOINs
>  
> Example:
> ```python
> City.objects.prefetch_related('theaters').all()
> ```
>  
> **Reverse ForeignKey** refers to accessing child objects from the parent side of a relationship, such as `city.theaters.all()`, where the `ForeignKey` is defined on the child model.

### 2. Database Indexes

```python
class Movie(models.Model):
    name = models.CharField(max_length=200, db_index=True)  # Index on name
    rating = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=['rating']),  # Single column index
            models.Index(fields=['category', 'rating']),  # Composite index
        ]
```

**When to add indexes?**
- Frequently queried fields (WHERE, ORDER BY, JOIN)
- Foreign keys (auto-indexed by Django)
- Fields used in filtering/searching

**Downsides**:
- Slower writes (INSERT, UPDATE, DELETE)
- More storage space

### 3. Migrations

**Interview Question**: *How does Django track schema changes?*
- Migration files (Python code)
- `django_migrations` table tracks applied migrations

**Commands**:
```bash
python manage.py makemigrations  # Create migration files
python manage.py migrate         # Apply migrations
python manage.py showmigrations  # Show status
```

### 4. Meta Options

```python
class ShowSeat(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)

    class Meta:
        # Table name (default: app_modelname)
        db_table = 'show_seats'

        # Default ordering
        ordering = ['show', 'seat']

        # Composite unique constraint
        unique_together = ['show', 'seat']

        # Modern way (Django 2.2+)
        constraints = [
            models.UniqueConstraint(
                fields=['show', 'seat'],
                name='unique_show_seat'
            ),
            models.CheckConstraint(
                check=Q(price__gte=0),
                name='price_positive'
            )
        ]

        # Permissions
        permissions = [
            ('can_book_premium', 'Can book premium seats'),
        ]

        # Plural name
        verbose_name_plural = 'Show Seats'
```

---

## Best Practices

### 1. Use Appropriate Field Types

```python
# Good
price = models.DecimalField(max_digits=10, decimal_places=2)  # For money

# Bad
price = models.FloatField()  # Floating point errors!
```

### 2. Use Choices for Fixed Values

```python
class SeatType(models.TextChoices):
    GOLD = 'GOLD', 'Gold'
    DIAMOND = 'DIAMOND', 'Diamond'
    PLATINUM = 'PLATINUM', 'Platinum'

class Seat(models.Model):
    seat_type = models.CharField(
        max_length=20,
        choices=SeatType.choices,
        default=SeatType.GOLD
    )
```

### 3. Add Timestamps

```python
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Won't create table

class Movie(BaseModel):  # Inherits timestamps
    name = models.CharField(max_length=200)
```

### 4. Use validators

```python
from django.core.validators import MinValueValidator, MaxValueValidator

class Movie(models.Model):
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
```

### 5. Property Methods

```python
class Show(models.Model):
    start_time = models.DateTimeField()
    duration = models.IntegerField()

    @property
    def end_time(self):
        """Computed property"""
        return self.start_time + timedelta(minutes=self.duration)
```

---

## Common Interview Questions

**Q1: Explain `on_delete` options.**
- CASCADE, PROTECT, SET_NULL, SET_DEFAULT, DO_NOTHING

**Q2: What's the difference between `null=True` and `blank=True`?**
- `null=True`: Database level (allows NULL)
- `blank=True`: Validation level (form can be empty)

**Q3: How to query with OR conditions?**
```python
from django.db.models import Q
Movie.objects.filter(Q(rating__gte=8) | Q(category='Action'))
```

**Q4: How to avoid N+1 queries?**
- Use `select_related()` for ForeignKey/OneToOne
- Use `prefetch_related()` for ManyToMany/reverse FK

**Q5: How to create a custom manager?**
```python
class AvailableShowManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            start_time__gte=timezone.now()
        )

class Show(models.Model):
    objects = models.Manager()  # Default
    available = AvailableShowManager()  # Custom
```

Usage: `Show.available.all()` → Only upcoming shows

---

## Summary

### Key Takeaways for Interviews

1. **Understand relationships**: 1:N (ForeignKey), 1:1 (OneToOne), M:N (ManyToMany)
2. **Use Through models** for M:N with extra fields
3. **Optimize queries**: select_related, prefetch_related, indexes
4. **Use Meta options**: ordering, unique_together, constraints
5. **Follow best practices**: validators, choices, timestamps
6. **Know gotchas**: N+1 queries, null vs blank, on_delete options

### Practice Questions

1. Design a model for a social media app (Users, Posts, Comments, Likes)
2. Implement a shopping cart system (Products, Cart, CartItems)
3. Design a flight booking system (Flights, Seats, Bookings)

Remember: **Models are just Python classes that map to database tables!**
