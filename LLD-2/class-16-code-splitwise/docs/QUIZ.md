# Splitwise Django Implementation Quiz

Test your understanding of Django implementation details, Python internals, and database design decisions in this project.

---

## Question 1: Django DateTime Fields

You need to add timestamp fields to track when records are created and modified. Which implementation is correct?

**Option A:**
```python
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
```

**Option B:**
```python
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
```

**Option C:**
```python
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

---
<details>
<summary><strong>Answer</strong></summary>

**Correct: Option C**

**Explanation:**

**Key Differences:**

| Parameter | Behavior | Use Case |
|-----------|----------|----------|
| `auto_now_add=True` | Set ONLY on creation | created_at, registration_date |
| `auto_now=True` | Set EVERY time saved | updated_at, last_modified |
| `db_index=True` | Creates database index | Frequently queried fields |

**Why Index `created_at`?**
- Common query: "Show me recent expenses" → `ORDER BY created_at DESC`
- Date range filters: `created_at__gte`, `created_at__lte`
- Without index: Full table scan (slow)
- With index: Fast B-tree lookup

**Real-world impact:**
```python
# Without index: Scans all 1,000,000 records
Expense.objects.filter(created_at__gte=last_month)  # ~500ms

# With index: Uses index, scans only matching records
Expense.objects.filter(created_at__gte=last_month)  # ~5ms
```

</details>

---

## Question 2: Database Indexing Strategy

You have these models in your Splitwise app. Which fields should be indexed?

**Option A:**
```python
class User(models.Model):
    username = models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=15, db_index=True)

class UserExpense(models.Model):
    user = models.ForeignKey(User)
    expense = models.ForeignKey(Expense)
    amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    type = models.CharField(choices=[('PAID', 'Paid'), ('OWED', 'Owed')], db_index=True)

```

**Option B:**
```python
class User(models.Model):
    username = models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=15)

class UserExpense(models.Model):
    user = models.ForeignKey(User)
    expense = models.ForeignKey(Expense)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(choices=[('PAID', 'Paid'), ('OWED', 'Owed')])

    class Meta:
        indexes = [
            models.Index(fields=['user', 'type']),
            models.Index(fields=['expense', 'type']),
        ]
```

---
<details>
<summary><strong>Answer</strong></summary>

**Correct: Option B**

**Explanation:**

2. **Option A is wrong (over-indexed):**
   - Indexes on `phone_number` - rarely used for lookups
   - Index on `amount` - not useful (we don't search by exact amount)
   - Missing composite indexes on UserExpense
   - Index on `type` alone - single-column index on low-cardinality field
   - Problems with over-indexing:
     - Every index slows down INSERT/UPDATE operations
     - Indexes take disk space
     - Database has to maintain all indexes
     - Example: 5 indexes on UserExpense means 5 updates per INSERT

3. **Option B is correct:**
   - `username` indexed: Fast login queries
   - `email` indexed: Fast email lookups
   - `phone_number` NOT indexed: Rarely used for queries
   - Composite index on `(user, type)`: Fast balance calculations
   - Composite index on `(expense, type)`: Fast expense detail queries
   - `amount` NOT indexed: Not used for filtering
   - `type` NOT indexed alone: Always queried with user or expense

---

**Why These Specific Indexes?**

**Index Order Matters:**
```python
# Index on (user, type) helps these queries:
- WHERE user=1 AND type='PAID'  ✓
- WHERE user=1                   ✓ (can use first part of index)

# But NOT this query:
- WHERE type='PAID'              ❌ (can't use index starting from middle)
```

### 3. UserExpense(expense, type) - Composite Index
```python
# Expense detail query
paid_by = UserExpense.objects.filter(
    expense=expense,
    type=UserExpenseType.PAID
)

owed_by = UserExpense.objects.filter(
    expense=expense,
    type=UserExpenseType.OWED
)

# Composite index allows fast lookup of both
```

---

**Index Strategy Rules:**

1. **Index fields used in WHERE clauses**
   - Login: `WHERE username='...'` → Index username ✓

2. **Index foreign keys used in JOINs**
   - Django auto-indexes ForeignKey fields ✓

3. **Create composite indexes for common multi-column queries**
   - `WHERE user=X AND type=Y` → Index (user, type) ✓

4. **Don't over-index**
   - Each index slows down writes
   - Only index what's actually queried

5. **Index high-cardinality fields**
   - username (unique per user) ✓
   - Not type (only 2 values) ❌

---

**Performance Impact:**

```python
# Without proper indexes
def get_user_balance(user):
    # Scans all UserExpense records
    paid = UserExpense.objects.filter(user=user, type='PAID').aggregate(Sum('amount'))
    # Time: O(n) where n = total UserExpense records

# With composite index (user, type)
def get_user_balance(user):
    # Uses index to find only relevant records
    paid = UserExpense.objects.filter(user=user, type='PAID').aggregate(Sum('amount'))
    # Time: O(log n + k) where k = records matching the criteria
```

**Real numbers:**
- 1M UserExpense records
- User has 100 expenses
- Without index: Scans 1M records (~500ms)
- With composite index: Scans 100 records (~5ms)
- **100x faster!**

</details>

---

## Question 3: Floating Point Arithmetic in Financial Calculations

You're validating that total paid equals total owed in an expense. Which implementation is correct?

**Option A:**
```python
def validate_expense(self):
    total_paid = self.userexpense_set.filter(
        type=UserExpenseType.PAID
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_owed = self.userexpense_set.filter(
        type=UserExpenseType.OWED
    ).aggregate(total=Sum('amount'))['total'] or 0

    if total_paid != total_owed:
        raise ValueError("Total paid must equal total owed")
```

**Option B:**
```python
def validate_expense(self):
    total_paid = self.userexpense_set.filter(
        type=UserExpenseType.PAID
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_owed = self.userexpense_set.filter(
        type=UserExpenseType.OWED
    ).aggregate(total=Sum('amount'))['total'] or 0

    if abs(float(total_paid) - float(total_owed)) > 0.01:
        raise ValueError(
            f"Total paid (₹{total_paid}) must equal total owed (₹{total_owed})"
        )
```
---
**Option C:**
```python
from decimal import Decimal

def validate_expense(self):
    total_paid = self.userexpense_set.filter(
        type=UserExpenseType.PAID
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    total_owed = self.userexpense_set.filter(
        type=UserExpenseType.OWED
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    if total_paid != total_owed:
        raise ValueError("Total paid must equal total owed")
```

---
<details>
<summary><strong>Answer</strong></summary>

**Correct: Option B**

**Explanation:**

1. **Option A is wrong:**
   - Uses exact equality check: `!=`
   - Fails due to floating point precision issues
   - Example problem:
     ```python
     # Splitting ₹100 three ways
     amount = 100 / 3  # 33.333333...

     split1 = 33.33
     split2 = 33.33
     split3 = 33.34
     total = split1 + split2 + split3  # 100.00

     # But in computer memory:
     split1 = 33.330000000000002
     split2 = 33.330000000000002
     split3 = 33.340000000000003
     total = 100.000000000000007  # Not exactly 100!

     # Validation fails:
     if total != 100:  # True! 100.000000000000007 != 100
         raise ValueError()  # Raises error even though amounts are correct
     ```
---
2. **Option C is wrong (for this context):**
   - Uses Django's `Decimal` type
   - Exact equality works with Decimal
   - **BUT** the aggregate Sum() might still return float in some cases
   - Also, in Option B we convert to float for comparison anyway
   - While Decimal is better for storage, the epsilon comparison is more robust

3. **Option B is correct:**
   - Uses epsilon comparison: `abs(a - b) > 0.01`
   - Tolerates floating point errors up to 1 paisa (₹0.01)
   - Practical for financial calculations
   - Won't fail on rounding errors

---

**Understanding Floating Point Precision:**

### The Problem:
```python
# In Python:
>>> 0.1 + 0.2
0.30000000000000004

>>> 0.1 + 0.2 == 0.3
False  # Even though mathematically equal!
```

**Why?**
- Computers store numbers in binary (base-2)
- Some decimal numbers can't be represented exactly in binary
- 0.1 in binary is an infinite repeating fraction (like 1/3 in decimal = 0.333...)
- Computer truncates after limited precision
- Results in tiny errors that accumulate
---
### Real Splitwise Example:

```python
# Expense: ₹1000 split 3 ways
total = 1000
per_person = total / 3  # 333.333333...

# Database stores with precision
user1_owes = 333.33  # Rounded
user2_owes = 333.33  # Rounded
user3_owes = 333.34  # Adjusted to balance

# When validating:
total_owed = 333.33 + 333.33 + 333.34
# In memory: 1000.0000000000001 (tiny error)

# Option A fails:
if total_owed != 1000:  # True, validation fails ❌
    raise ValueError()

# Option B succeeds:
if abs(1000.0000000000001 - 1000) > 0.01:  # False, passes ✓
    # Error is 0.0000000000001, less than 0.01
    pass
```

---

**Why 0.01 Threshold?**

1. **Smallest Currency Unit**
   - In India: 1 paisa = ₹0.01
   - Can't have amounts smaller than 0.01
   - Errors larger than 0.01 are actual mistakes

2. **Rounding Errors**
   - Accumulated rounding across splits might cause small discrepancies
   - Example: ₹100 split 7 ways
     - Exact: 14.285714... each
     - Rounded: 14.29, 14.29, 14.29, 14.29, 14.29, 14.29, 14.28
     - Total: 100.01 (off by 1 paisa)
   - Epsilon allows this small error

3. **Practical Balance**
   ```python
   # Too strict (0.0001):
   # Fails on legitimate rounding: 333.33 + 333.33 + 333.34 = 1000.0000000001

   # Too loose (1.0):
   # Allows actual errors: User owes ₹1000 but entered ₹999

   # Just right (0.01):
   # Allows floating point errors, catches real mistakes
   ```

---

**Better Alternative: Use Decimal Throughout**

```python
from decimal import Decimal

class UserExpense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)

def validate_expense(self):
    # Returns Decimal, not float
    total_paid = self.userexpense_set.filter(
        type='PAID'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    total_owed = self.userexpense_set.filter(
        type='OWED'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # Exact comparison works with Decimal
    if total_paid != total_owed:
        raise ValueError()
```

**Why Decimal is Better:**
```python
# Float:
>>> 0.1 + 0.2
0.30000000000000004

# Decimal:
>>> Decimal('0.1') + Decimal('0.2')
Decimal('0.3')  # Exact!
```
---
**Django uses Decimal for DecimalField:**
- Stored as Decimal in database
- No floating point errors
- Perfect for money

---

**Summary:**

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| **Exact equality** | Simple | Fails on rounding | Never for floats |
| **Epsilon (0.01)** | Tolerates FP errors | Might hide small bugs | Financial comparisons |
| **Decimal type** | Exact, no errors | More verbose | All money operations |

**Best Practice for Money:**
1. Store as `DecimalField` ✓
2. Use `Decimal` type in Python ✓
3. If comparing floats, use epsilon ✓
4. Never use `float` for money ❌

</details>

---

## Question 4: Many-to-Many Through Model

You need users to belong to multiple groups and groups to have multiple users. Which design is best?

**Option A:**
```python
class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)
```

**Option B:**
```python
class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, through='GroupMembership')

class GroupMembership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
```

**Option C:**
```python
class Group(models.Model):
    name = models.CharField(max_length=100)
    member_ids = models.JSONField(default=list)  # Store list of user IDs
```

---
<details>
<summary><strong>Answer</strong></summary>

**Correct: Option B**

**Explanation:**

1. **Option A is incomplete:**
   - Basic ManyToMany works but lacks flexibility
   - Cannot track when users joined
   - Cannot add role information (admin, member)
   - Cannot track who added them
   - Django creates hidden junction table automatically, but you can't customize it
   - Example limitation:
     ```python
     group = Group.objects.get(name="Goa Trip")
     group.members.add(user)
     # Added to group, but when? Who added them? Unknown.
     ```
---
2. **Option C is wrong (anti-pattern):**
   - JSONField for relationships violates normalization
   - Cannot use foreign key constraints
   - Cannot use Django ORM for queries
   - No referential integrity
   - Problems:
     ```python
     # Adding a member
     group.member_ids.append(5)
     group.save()

     # Problems:
     # 1. What if user ID 5 doesn't exist? No validation ❌
     # 2. What if user 5 is deleted? JSON isn't updated ❌
     # 3. How to query "all groups user 5 is in"? ❌
     #    Group.objects.filter(member_ids__contains=5)  # Inefficient full scan
     # 4. Can't JOIN in database queries ❌
     ```

3. **Option B is correct:**
   - Explicit through model gives full control
   - Can add metadata: `joined_at`, `role`, `added_by`
   - Maintains database integrity with proper FKs
   - Can use Django ORM efficiently
   - Extensible for future requirements

---

**Why We Need Through Model:**

### Use Case 1: Track When Users Joined
```python
# With Through Model:
membership = GroupMembership.objects.get(group=goa_trip, user=rajesh)
print(f"Joined on: {membership.joined_at}")

# Without Through Model:
# No way to know when user was added ❌
```

### Use Case 2: Who Added the Member?
```python
class GroupMembership(models.Model):
    group = models.ForeignKey(Group)
    user = models.ForeignKey(User)
    joined_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, related_name='members_added')  # Track who invited

# Query: "Who added Priya to the group?"
membership = GroupMembership.objects.get(group=goa_trip, user=priya)
print(f"Added by: {membership.added_by.name}")
```
---
### Use Case 3: Member Roles
```python
class GroupMembership(models.Model):
    group = models.ForeignKey(Group)
    user = models.ForeignKey(User)
    role = models.CharField(choices=[
        ('ADMIN', 'Administrator'),
        ('MEMBER', 'Member'),
        ('VIEWER', 'Viewer')
    ])

# Business rule: Only admins can add expenses
if membership.role == 'ADMIN':
    # Allow expense creation
```
---
### Use Case 4: Soft Delete from Group
```python
class GroupMembership(models.Model):
    group = models.ForeignKey(Group)
    user = models.ForeignKey(User)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True)  # Track when they left
    is_active = models.BooleanField(default=True)

# User leaves group (don't delete history)
membership.is_active = False
membership.left_at = timezone.now()
membership.save()

# Query active members only
active_members = GroupMembership.objects.filter(group=group, is_active=True)
```

---

**How Through Model Works:**

### Django's Automatic Table (Option A):
```sql
-- Django creates this automatically
CREATE TABLE group_members (
    id INTEGER PRIMARY KEY,
    group_id INTEGER REFERENCES groups(id),
    user_id INTEGER REFERENCES users(id),
    UNIQUE(group_id, user_id)
);
```
- Cannot customize
- Cannot add fields
- Cannot track metadata

### Manual Through Model (Option B):
```sql
-- You define this explicitly
CREATE TABLE group_memberships (
    id INTEGER PRIMARY KEY,
    group_id INTEGER REFERENCES groups(id),
    user_id INTEGER REFERENCES users(id),
    joined_at TIMESTAMP,      -- Custom field ✓
    added_by_id INTEGER,      -- Custom field ✓
    role VARCHAR(20),         -- Custom field ✓
    is_active BOOLEAN,        -- Custom field ✓
    UNIQUE(group_id, user_id)
);
```
- Full control
- Add any fields you need
- Track all metadata

---

**Real Implementation in Our Project:**

```python
class Group(BaseModel):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, related_name='created_groups')
    members = models.ManyToManyField(User, through='GroupMembership', related_name='member_groups')

class GroupMembership(BaseModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'user')  # Can't join same group twice
```
---
**Benefits:**
```python
# Add member with metadata
membership = GroupMembership.objects.create(
    group=goa_trip,
    user=priya,
    # joined_at is set automatically
)

# Query all groups for a user
user_groups = Group.objects.filter(members=user)

# Query all members of a group
group_members = User.objects.filter(member_groups=group)

# Check when someone joined
membership = GroupMembership.objects.get(group=group, user=user)
print(f"Member since: {membership.joined_at}")
```

---

**When to Use Through Model:**

✅ **Use Through Model when:**
- Need to track metadata (when, who, why)
- Need to add role or status fields
- Need audit trail
- Relationship might have additional data

❌ **Don't need Through Model when:**
- Pure many-to-many with no metadata
- Simple tag systems
- No additional relationship data needed

**Example without Through Model:**
```python
class BlogPost(models.Model):
    tags = models.ManyToManyField(Tag)  # Just tags, no metadata
```

**Example with Through Model (our case):**
```python
class Group(models.Model):
    members = models.ManyToManyField(User, through='GroupMembership')  # Need joined_at
```

</details>

---

## Question 5: Django Admin Configuration

You have these models in your project. What does the `admin.py` file do?

```python
# models.py
class User(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    email = models.EmailField()

# admin.py
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'created_at')
    search_fields = ('username', 'name', 'email')
    readonly_fields = ('created_at', 'updated_at')
```

**Option A:** Defines the database schema and creates tables

**Option B:** Creates a web interface for managing model data in the browser

**Option C:** Configures API endpoints for the User model

---
<details>
<summary><strong>Answer</strong></summary>

**Correct: Option B**

**Explanation:**

1. **Option A is wrong:**
   - Database schema is defined in `models.py`, not `admin.py`
   - Migrations create tables (via `manage.py migrate`)
   - `admin.py` doesn't affect database structure at all

2. **Option C is wrong:**
   - API endpoints require REST framework or viewsets
   - `admin.py` is for Django's built-in admin interface
   - APIs would be in `views.py`, `serializers.py`, and `urls.py`

3. **Option B is correct:**
   - `admin.py` configures Django's built-in admin panel
   - Creates web UI at `/admin/` URL
   - Allows CRUD operations without writing code
   - Useful for testing, data management, and internal tools

---

**What Django Admin Does:**

### Without admin.py Registration:
- Model exists in database
- Can query via Django shell: `User.objects.all()`
- **NOT** visible in admin panel at http://localhost:8000/admin/

### With admin.py Registration:
```python
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
```
- Model appears in admin panel
- Default interface with all fields
- Can create, read, update, delete records
- **Still basic, no customization**

### With Configuration:
```python
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'created_at')
    search_fields = ('username', 'name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('created_at',)
```
- **Customized interface**
- Shows specific columns in list view
- Adds search functionality
- Protects audit fields from editing
- Adds filters

---

**Admin Configuration Options:**

### 1. `list_display` - Columns in List View
```python
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'created_at')
```
**Effect:**
```
Users List
┌────────────────┬─────────────────┬─────────────────────┬────────────────┐
│ Username       │ Name            │ Email               │ Created At     │
├────────────────┼─────────────────┼─────────────────────┼────────────────┤
│ rajesh_sharma  │ Rajesh Sharma   │ rajesh@email.com    │ 2025-01-15     │
│ priya_patel    │ Priya Patel     │ priya@email.com     │ 2025-01-15     │
└────────────────┴─────────────────┴─────────────────────┴────────────────┘
```
Without `list_display`: Only shows `User object (1)`, `User object (2)` ❌

### 2. `search_fields` - Add Search Box
```python
class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'name', 'email')
```
**Effect:**
- Adds search bar at top
- Searches across specified fields
- Example: Type "rajesh" → finds users matching in username, name, or email

### 3. `readonly_fields` - Protect Fields
```python
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
```
**Effect:**
- Fields visible but cannot be edited
- Useful for auto-generated fields (timestamps, IDs)
- Prevents accidental modification

### 4. `list_filter` - Add Sidebar Filters
```python
class ExpenseAdmin(admin.ModelAdmin):
    list_filter = ('currency', 'group', 'created_at')
```
**Effect:**
```
Expenses
┌─────────────────────────────────┐
│ Filters                         │
├─────────────────────────────────┤
│ Currency                        │
│  ☐ INR                          │
│  ☐ USD                          │
│                                 │
│ Group                           │
│  ☐ Goa Trip                     │
│  ☐ Office Lunch                 │
│                                 │
│ Created Date                    │
│  ☐ Today                        │
│  ☐ Past 7 days                  │
└─────────────────────────────────┘
```

### 5. `ordering` - Default Sort Order
```python
class ExpenseAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)  # Newest first
```

---

**Real Example from Our Project:**

```python
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'phone_number', 'created_at')
    search_fields = ('username', 'name', 'email')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'total_amount', 'currency', 'created_by', 'group', 'created_at')
    search_fields = ('description',)
    list_filter = ('currency', 'group')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(UserExpense)
class UserExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'expense', 'amount', 'type', 'created_at')
    search_fields = ('user__name', 'expense__description')
    list_filter = ('type',)
    readonly_fields = ('created_at', 'updated_at')
```

**Access Admin Panel:**
1. Create superuser: `python manage.py createsuperuser`
2. Run server: `python manage.py runserver`
3. Visit: http://localhost:8000/admin/
4. Login with superuser credentials
5. See all registered models with custom interfaces

---

**Benefits of Django Admin:**

1. **No Code Required**
   - Automatic CRUD interface
   - No need to write views, forms, templates

2. **Quick Data Management**
   - Add test data
   - Fix data issues
   - Verify database state

3. **Internal Tool**
   - Staff can manage data
   - Non-technical users can add content

4. **Development Aid**
   - Quickly inspect data
   - Test model relationships
   - Debug issues

---

**When to Use Admin:**

✅ **Good for:**
- Internal data management
- Staff/admin interfaces
- Testing during development
- Content management for non-technical users

❌ **Not for:**
- Public-facing features
- Customer interfaces
- Complex workflows
- High-performance needs

**For public features, build proper views/APIs instead.**

---

**Summary:**

| File | Purpose | Creates |
|------|---------|---------|
| `models.py` | Define data structure | Database tables |
| `admin.py` | Configure admin panel | Web interface for data management |
| `views.py` | Handle requests | Public-facing pages/APIs |
| `urls.py` | Define URL routes | URL-to-view mapping |

**`admin.py` = Built-in data management interface, not for public use**

</details>

---

## Summary

These questions cover:
1. ✅ Django ORM (auto_now, auto_now_add, indexes)
2. ✅ Database design (indexing strategy, when/why)
3. ✅ Python internals (floating point arithmetic, Decimal vs float)
4. ✅ Design patterns (through models, many-to-many relationships)
5. ✅ Django admin (configuration, purpose, benefits)

**Key Takeaways:**
- Use `auto_now_add` for creation timestamps (set once)
- Use `auto_now` for update timestamps (set on every save)
- Index high-cardinality fields and frequently queried columns
- Use epsilon comparison for floating point money calculations
- Through models provide flexibility and metadata for relationships
- Django admin provides automatic data management interface

Good luck! 🎯
