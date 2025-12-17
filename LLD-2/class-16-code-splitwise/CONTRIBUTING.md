# Contributing to Splitwise

Thank you for your interest in extending this project! This guide will help you add new features following the existing patterns.

## 🎯 How to Add a New Command

Let's walk through adding a `DELETE_EXPENSE` command as an example.

### Step 1: Create the Command Class

Add to `splitwise_app/commands/expense_commands.py`:

```python
class DeleteExpenseCommand(Command):
    """Command to delete an expense."""

    def __init__(self, expense_id, user_id):
        self.expense_id = expense_id
        self.user_id = user_id

    def validate(self):
        # Check if expense exists
        try:
            self.expense = Expense.objects.get(id=self.expense_id)
        except Expense.DoesNotExist:
            raise ValueError(f"Expense with ID {self.expense_id} not found")

        # Check if user is the creator
        try:
            self.user = User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            raise ValueError(f"User with ID {self.user_id} not found")

        if self.expense.created_by != self.user:
            raise PermissionError("Only the expense creator can delete it")

    def execute(self):
        expense_desc = self.expense.description
        self.expense.delete()
        return f"✓ Expense '{expense_desc}' deleted successfully"
```

### Step 2: Add Parser Method

Add to `splitwise_app/commands/command_parser.py`:

```python
def _parse_delete_expense(self, tokens):
    """DELETE_EXPENSE <expense_id> <user_id>"""
    if len(tokens) < 2:
        raise ValueError("Usage: DELETE_EXPENSE <expense_id> <user_id>")
    return DeleteExpenseCommand(
        expense_id=int(tokens[0]),
        user_id=int(tokens[1])
    )
```

### Step 3: Register in Command Map

In `CommandParser.__init__()`, add:

```python
self.command_map = {
    # ... existing commands
    'DELETE_EXPENSE': self._parse_delete_expense,
}
```

### Step 4: Update Help Text

In `show_help()`, add:

```python
EXPENSE COMMANDS:
  ...
  DELETE_EXPENSE <expense_id> <user_id>
    Delete an expense (only creator can delete)
    Example: DELETE_EXPENSE 5 1
```

### Step 5: Test It

```bash
splitwise> DELETE_EXPENSE 1 1
✓ Expense 'Hotel Booking - Goa' deleted successfully
```

That's it! Your new command is integrated.

---

## 🔧 Common Extensions

### 1. Add Expense Categories

#### Step 1: Update Model

```python
# In splitwise_app/models/expense.py

class ExpenseCategory(models.TextChoices):
    FOOD = 'FOOD', 'Food & Dining'
    TRANSPORT = 'TRANSPORT', 'Transportation'
    ENTERTAINMENT = 'ENTERTAINMENT', 'Entertainment'
    UTILITIES = 'UTILITIES', 'Utilities'
    OTHER = 'OTHER', 'Other'

class Expense(BaseModel):
    # ... existing fields
    category = models.CharField(
        max_length=20,
        choices=ExpenseCategory.choices,
        default=ExpenseCategory.OTHER
    )
```

#### Step 2: Update Command

```python
class AddExpenseCommand(Command):
    def __init__(self, description, amount, created_by_id, group_id,
                 paid_by, owed_by, category='OTHER'):
        # ... existing code
        self.category = category
```

#### Step 3: Update Parser

```python
def _parse_add_expense(self, tokens):
    # Parse category if provided (last token)
    category = tokens[6] if len(tokens) > 6 else 'OTHER'
    # ... rest of parsing
```

---

### 2. Add Expense Search

```python
class SearchExpensesCommand(Command):
    """Search expenses by description."""

    def __init__(self, user_id, query):
        self.user_id = user_id
        self.query = query

    def validate(self):
        try:
            self.user = User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            raise ValueError(f"User with ID {self.user_id} not found")

    def execute(self):
        expenses = self.user.get_expenses().filter(
            description__icontains=self.query
        )

        output = [f"\nFound {expenses.count()} expenses matching '{self.query}':\n"]

        for expense in expenses:
            output.append(f"  [{expense.id}] {expense.description} - ₹{expense.total_amount}")

        return '\n'.join(output)
```

---

### 3. Add User Search

```python
class SearchUsersCommand(Command):
    """Search users by name or username."""

    def __init__(self, query):
        self.query = query

    def validate(self):
        if not self.query or len(self.query) < 2:
            raise ValueError("Search query must be at least 2 characters")

    def execute(self):
        from django.db.models import Q

        users = User.objects.filter(
            Q(name__icontains=self.query) |
            Q(username__icontains=self.query)
        )

        if not users.exists():
            return f"No users found matching '{self.query}'"

        output = [f"\nFound {users.count()} users:\n"]

        for user in users:
            output.append(f"  [{user.id}] {user.name} (@{user.username})")

        return '\n'.join(output)
```

---

### 4. Add Group Member List

```python
class ListGroupMembersCommand(Command):
    """List all members of a group."""

    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id

    def validate(self):
        try:
            self.group = Group.objects.get(id=self.group_id)
        except Group.DoesNotExist:
            raise ValueError(f"Group with ID {self.group_id} not found")

        try:
            self.user = User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            raise ValueError(f"User with ID {self.user_id} not found")

        if not self.group.is_member(self.user):
            raise PermissionError(f"You must be a member of '{self.group.name}'")

    def execute(self):
        memberships = GroupMembership.objects.filter(
            group=self.group
        ).select_related('user').order_by('joined_at')

        output = [f"\n{'='*60}"]
        output.append(f"MEMBERS OF: {self.group.name}")
        output.append(f"{'='*60}\n")

        for membership in memberships:
            is_creator = "👑 Creator" if membership.user == self.group.created_by else ""
            output.append(
                f"  {membership.user.name} (@{membership.user.username}) {is_creator}"
            )
            output.append(f"    Joined: {membership.joined_at.strftime('%Y-%m-%d')}")

        output.append(f"\nTotal members: {memberships.count()}")
        return '\n'.join(output)
```

---

## 🧪 Adding Tests

### Example: Test User Registration

Create `splitwise_app/tests.py`:

```python
from django.test import TestCase
from splitwise_app.models import User
from splitwise_app.commands.user_commands import RegisterUserCommand


class UserCommandTests(TestCase):
    def test_register_user_success(self):
        """Test successful user registration."""
        command = RegisterUserCommand(
            username='test_user',
            name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            password='testpass'
        )

        command.validate()
        result = command.execute()

        self.assertIn('User registered successfully', result)
        self.assertTrue(User.objects.filter(username='test_user').exists())

    def test_register_duplicate_username(self):
        """Test registration with duplicate username fails."""
        # Create first user
        User.objects.create(
            username='duplicate',
            name='First User',
            email='first@example.com',
            phone_number='1111111111'
        )

        # Try to create second user with same username
        command = RegisterUserCommand(
            username='duplicate',
            name='Second User',
            email='second@example.com',
            phone_number='2222222222',
            password='password'
        )

        with self.assertRaises(ValueError):
            command.validate()

    def test_register_short_password(self):
        """Test registration with short password fails."""
        command = RegisterUserCommand(
            username='test',
            name='Test',
            email='test@example.com',
            phone_number='1234567890',
            password='123'  # Too short
        )

        with self.assertRaises(ValueError):
            command.validate()
```

Run tests:
```bash
python manage.py test
```

---

## 🎨 Code Style Guide

### 1. Command Naming
- Use descriptive names: `RegisterUserCommand`, not `RegUser`
- End with "Command": `DeleteExpenseCommand`

### 2. Validation
- Always validate in `validate()` method
- Raise `ValueError` for invalid data
- Raise `PermissionError` for permission issues

### 3. Error Messages
- Be specific: "User with ID 5 not found" not "Invalid user"
- User-friendly: "You must be a member" not "Access denied"

### 4. Success Messages
- Use ✓ checkmark for success
- Include relevant details: "Expense 'Dinner' (₹1500) added successfully"
- Include ID for reference: "ID: 5"

### 5. Output Formatting
```python
# Use consistent formatting
output = [f"\n{'='*60}"]
output.append(f"TITLE")
output.append(f"{'='*60}\n")
# ... content
return '\n'.join(output)
```

---

## 📋 Feature Ideas

### Easy
- [ ] View all groups a user is in
- [ ] List all users in the system
- [ ] Show total expenses in a group
- [ ] Export expenses to CSV

### Medium
- [ ] Edit expense description/amount
- [ ] Add expense attachments (receipt images)
- [ ] Add comments to expenses
- [ ] Expense categories with filtering

### Hard
- [ ] Multi-currency support with conversion
- [ ] Recurring expenses (monthly rent)
- [ ] Expense templates
- [ ] Payment integration (simulate)
- [ ] Notifications system

---

## 🐛 Debugging Tips

### 1. Check Database State
```bash
python manage.py shell

>>> from splitwise_app.models import User, Expense
>>> User.objects.all()
>>> Expense.objects.filter(created_by__username='rajesh')
```

### 2. Test Command Directly
```python
from splitwise_app.commands.user_commands import ShowBalanceCommand

command = ShowBalanceCommand(user_id=1)
command.validate()
result = command.execute()
print(result)
```

### 3. View SQL Queries
```python
from django.db import connection

# Run your command
# Then check queries
print(connection.queries)
```

---

## 📚 Learning Resources

### Django
- [Django Documentation](https://docs.djangoproject.com/)
- [Django ORM Tutorial](https://docs.djangoproject.com/en/stable/topics/db/queries/)

### Design Patterns
- [Refactoring Guru - Command Pattern](https://refactoring.guru/design-patterns/command)
- [Source Making - Design Patterns](https://sourcemaking.com/design_patterns)

### Algorithms
- [GeeksforGeeks - Greedy Algorithms](https://www.geeksforgeeks.org/greedy-algorithms/)
- [Python Heapq Documentation](https://docs.python.org/3/library/heapq.html)

---

## 🤝 Contribution Guidelines

### Before You Start
1. Read the existing code
2. Understand the Command pattern
3. Check if feature already exists
4. Plan your changes

### Making Changes
1. Follow existing code style
2. Add proper validation
3. Write clear error messages
4. Update documentation
5. Test thoroughly

### Submitting
1. Test your changes
2. Update help text
3. Add examples to docs
4. Document any new dependencies

---

## 💡 Tips for Success

1. **Start Small**: Add simple commands first
2. **Follow Patterns**: Look at existing commands
3. **Test Early**: Test as you code
4. **Document**: Add docstrings and comments
5. **Ask Questions**: Review existing code if unsure

---

## 🎯 Challenge Projects

### Project 1: Add REST API
Convert the CLI to a REST API using Django REST Framework.
- Create serializers for models
- Create viewsets for endpoints
- Add authentication with JWT
- Document with Swagger

### Project 2: Add Web Frontend
Create a web UI for the application.
- Use Django templates or React
- Add user authentication
- Create dashboards
- Add charts for expenses

### Project 3: Mobile App
Create a mobile app using the API.
- React Native or Flutter
- Offline support
- Push notifications
- Receipt scanning

---

Happy Contributing! 🚀

If you have questions or need help, refer to the documentation or create an issue.
