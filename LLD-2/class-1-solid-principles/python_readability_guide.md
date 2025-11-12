# Python Readability Best Practices

## Naming Conventions (PEP 8)

| Type | Convention | Example |
|------|------------|---------|
| **Variables** | `snake_case` | `user_name`, `total_count` |
| **Functions** | `snake_case` | `calculate_total()`, `get_user()` |
| **Classes** | `PascalCase` | `UserAccount`, `OrderProcessor` |
| **Constants** | `UPPER_SNAKE_CASE` | `MAX_SIZE`, `API_KEY` |
| **Private** | `_leading_underscore` | `_internal_method()`, `_helper` |
| **Module** | `snake_case` | `user_service.py` |

## Function/Method Guidelines

**Use descriptive verbs:**
- ❌ `data()` → ✅ `fetch_data()`, `process_data()`
- ❌ `user()` → ✅ `get_user()`, `create_user()`

**Boolean functions start with `is_`, `has_`, `can_`:**
- `is_valid()`, `has_permission()`, `can_access()`

**Keep functions short:** 1 function = 1 task

## Class Guidelines

**Nouns for classes:** `User`, `Invoice`, `EmailService`

**Use meaningful names:**
- ❌ `DataProcessor` → ✅ `OrderValidator`
- ❌ `Manager` → ✅ `UserRepository`

## Variable Guidelines

**Descriptive over short:**
- ❌ `d`, `temp`, `x` → ✅ `duration`, `user_email`, `total_price`

**Plurals for collections:**
- `users = []`, `order_items = []`

## Code Layout

**Spacing:**
```python
# 2 blank lines before classes/functions
class User:
    pass


def calculate():
    pass

# 1 blank line between methods
class Order:
    def create(self):
        pass
    
    def delete(self):
        pass
```

**Line length:** Max 79-99 characters

**Indentation:** 4 spaces (never tabs)

## Comments

**When to comment:**
- ✅ WHY, not WHAT
- ✅ Complex logic
- ❌ Obvious code

```python
# ❌ BAD
x = x + 1  # Increment x

# ✅ GOOD
x = x + 1  # Adjust for zero-based indexing
```

## Docstrings

```python
def calculate_discount(price, percentage):
    """Calculate discount amount.
    
    Args:
        price: Original price
        percentage: Discount percentage (0-100)
    
    Returns:
        Discount amount
    """
    return price * (percentage / 100)
```

## Quick Tips

1. **Names reveal intent** - code should read like English
2. **Avoid abbreviations** - `calculate_total()` not `calc_tot()`
3. **No magic numbers** - use named constants
4. **Consistent style** - follow PEP 8
5. **One statement per line** - no `x=1;y=2`

## Resources

- **PEP 8:** https://pep8.org
- **Check style:** `pylint`, `flake8`, `black`