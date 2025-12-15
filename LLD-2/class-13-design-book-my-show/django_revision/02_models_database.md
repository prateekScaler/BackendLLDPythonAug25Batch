# Django Models & Database

## What are Models?

Models define your data structure. Each model maps to a single database table.

---

## Creating Models

### Basic Model Example
```python
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.name
```

---

## Field Types

### Common Field Types
```python
# Text fields
CharField(max_length=255)           # Short text
TextField()                         # Long text
EmailField()                        # Email validation
URLField()                          # URL validation
SlugField()                         # URL-friendly text

# Numeric fields
IntegerField()                      # Integer
FloatField()                        # Floating point
DecimalField(max_digits=10, decimal_places=2)  # Precise decimal

# Date/Time fields
DateField()                         # Date only
TimeField()                         # Time only
DateTimeField()                     # Date and time

# Boolean
BooleanField()                      # True/False

# File fields
FileField(upload_to='files/')      # Any file
ImageField(upload_to='images/')    # Images only

# Choice field
CHOICES = [('M', 'Male'), ('F', 'Female')]
gender = models.CharField(max_length=1, choices=CHOICES)
```

---

## Field Options

```python
# Common options
null=True              # Database allows NULL
blank=True             # Form validation allows empty
default=value          # Default value
unique=True            # Must be unique
db_index=True          # Create database index
editable=False         # Hide from forms
help_text="Help text"  # Form help text

# Auto fields
auto_now=True          # Update on every save
auto_now_add=True      # Set only on creation
```

---

## Relationships

### One-to-Many (ForeignKey)
```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # One author can have many books
```

**on_delete options:**
- `CASCADE`: Delete related objects
- `PROTECT`: Prevent deletion
- `SET_NULL`: Set to NULL (requires null=True)
- `SET_DEFAULT`: Set to default value
- `DO_NOTHING`: Do nothing (can cause integrity errors)

### Many-to-Many
```python
class Student(models.Model):
    name = models.CharField(max_length=100)

class Course(models.Model):
    title = models.CharField(max_length=100)
    students = models.ManyToManyField(Student)
    # Many students can enroll in many courses
```

### One-to-One
```python
class User(models.Model):
    username = models.CharField(max_length=100)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    # Each user has exactly one profile
```

---

## Migrations

### Create & Apply Migrations
```bash
# Generate migration files
python manage.py makemigrations

# View SQL that will be executed
python manage.py sqlmigrate myapp 0001

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

### Migration Best Practices
- Always review migrations before applying
- Never edit migration files manually (unless you know what you're doing)
- Keep migrations in version control
- Run migrations in production carefully

---

## QuerySet API

### Creating Objects
```python
# Method 1: Create and save
user = User(name='Jawahar', email='Jawahar@example.com')
user.save()

# Method 2: Create in one step
user = User.objects.create(name='Rithick', email='Rithick@example.com')

# Bulk create
User.objects.bulk_create([
    User(name='Praveen', email='praveen@scaler.com'),
    User(name='Sumit', email='Sumit@example.com'),
])
```

### Retrieving Objects
```python
# Get all objects
users = User.objects.all()

# Get single object (raises error if not found)
user = User.objects.get(id=1)

# Filter objects
active_users = User.objects.filter(is_active=True)
jas = User.objects.filter(name__icontains='ja')

# Exclude objects
not_jawahars = User.objects.exclude(name='Jawahar')

# Get first/last
first_user = User.objects.first()
last_user = User.objects.last()

# Check existence
exists = User.objects.filter(email='Jawahar@example.com').exists()

# Count
count = User.objects.count()
```

### Field Lookups
```python
# Exact match
User.objects.filter(name__exact='Praveen')
User.objects.filter(name='Praveen')  # Same as above

# Case-insensitive
User.objects.filter(name__iexact='Praveen')

# Contains
User.objects.filter(name__contains='oh')
User.objects.filter(name__icontains='OH')  # Case-insensitive

# Starts with / Ends with
User.objects.filter(name__startswith='J')
User.objects.filter(email__endswith='@gmail.com')

# Greater than / Less than
User.objects.filter(age__gt=18)   # Greater than
User.objects.filter(age__gte=18)  # Greater than or equal
User.objects.filter(age__lt=65)   # Less than
User.objects.filter(age__lte=65)  # Less than or equal

# In list
User.objects.filter(id__in=[1, 2, 3])

# Range
User.objects.filter(age__range=(18, 65))

# NULL checks
User.objects.filter(age__isnull=True)

# Date queries
from datetime import date
User.objects.filter(created_at__date=date.today())
User.objects.filter(created_at__year=2024)
User.objects.filter(created_at__month=12)
```

### Updating Objects
```python
# Update single object
user = User.objects.get(id=1)
user.name = 'Jane'
user.save()

# Update multiple objects
User.objects.filter(is_active=False).update(is_active=True)

# Update or create
user, created = User.objects.update_or_create(
    email='Debina@example.com',
    defaults={'name': 'Debina', 'age': 30}
)
```

### Deleting Objects
```python
# Delete single object
user = User.objects.get(id=1)
user.delete()

# Delete multiple objects
User.objects.filter(is_active=False).delete()

# Delete all (be careful!)
User.objects.all().delete()
```

### Ordering & Limiting
```python
# Order by
User.objects.order_by('name')           # Ascending
User.objects.order_by('-created_at')    # Descending
User.objects.order_by('name', '-age')   # Multiple fields

# Limit results (like SQL LIMIT)
User.objects.all()[:5]                  # First 5
User.objects.all()[5:10]                # 6th to 10th

# Reverse order
User.objects.order_by('-name').reverse()
```

### Aggregation
```python
from django.db.models import Count, Avg, Sum, Max, Min

# Count
user_count = User.objects.count()

# Aggregate
User.objects.aggregate(Avg('age'))
User.objects.aggregate(Max('age'), Min('age'))

# Annotate (add calculated field to each object)
from django.db.models import Count
authors = Author.objects.annotate(book_count=Count('book'))
for author in authors:
    print(f"{author.name} has {author.book_count} books")
```

### QuerySet Chaining
```python
# QuerySets are lazy - query executes when evaluated
users = User.objects.filter(is_active=True)  # No DB hit yet
users = users.filter(age__gte=18)            # Still no DB hit
users = users.order_by('name')               # Still no DB hit
for user in users:                            # NOW query executes
    print(user.name)
```

---

## Performance Optimization

### select_related (for ForeignKey & OneToOne)
```python
# Without select_related (N+1 queries problem)
books = Book.objects.all()
for book in books:
    print(book.author.name)  # Hits DB for each book!

# With select_related (1 query with JOIN)
books = Book.objects.select_related('author').all()
for book in books:
    print(book.author.name)  # No extra DB hit
```

### prefetch_related (for ManyToMany & reverse ForeignKey)
```python
# Without prefetch_related
authors = Author.objects.all()
for author in authors:
    for book in author.book_set.all():  # Hits DB for each author!
        print(book.title)

# With prefetch_related
authors = Author.objects.prefetch_related('book_set').all()
for author in authors:
    for book in author.book_set.all():  # No extra DB hit
        print(book.title)
```

### only() and defer()
```python
# Load only specific fields
User.objects.only('name', 'email')

# Defer loading specific fields
User.objects.defer('bio')  # Load everything except bio
```

---

## Model Methods

```python
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def get_final_price(self):
        """Calculate price after discount"""
        return self.price - (self.price * self.discount / 100)

    @property
    def is_discounted(self):
        """Check if product has discount"""
        return self.discount > 0

    def __str__(self):
        return self.name
```

---

## Database Configuration

### SQLite (Default)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### PostgreSQL
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### MySQL
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

## Resources

- [Django Model Field Reference](https://docs.djangoproject.com/en/stable/ref/models/fields/)
- [QuerySet API Reference](https://docs.djangoproject.com/en/stable/ref/models/querysets/)
- [Database Optimization](https://docs.djangoproject.com/en/stable/topics/db/optimization/)
- [Making Queries](https://docs.djangoproject.com/en/stable/topics/db/queries/)
