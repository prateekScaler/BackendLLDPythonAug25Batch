from .base import Command
from splitwise_app.models import User


class RegisterUserCommand(Command):
    """Command to register a new user."""

    def __init__(self, username, name, email, phone_number, password):
        self.username = username
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.password = password

    def validate(self):
        if not self.username or len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not self.name:
            raise ValueError("Name is required")
        if not self.email or '@' not in self.email:
            raise ValueError("Valid email is required")
        if not self.phone_number or len(self.phone_number) < 10:
            raise ValueError("Valid phone number is required")
        if not self.password or len(self.password) < 4:
            raise ValueError("Password must be at least 4 characters")

        # Check if username or email already exists
        if User.objects.filter(username=self.username).exists():
            raise ValueError(f"Username '{self.username}' already exists")
        if User.objects.filter(email=self.email).exists():
            raise ValueError(f"Email '{self.email}' already exists")

    def execute(self):
        user = User(
            username=self.username,
            name=self.name,
            email=self.email,
            phone_number=self.phone_number
        )
        user.set_password(self.password)
        user.save()

        return f"✓ User registered successfully! ID: {user.id}, Username: {user.username}"


class UpdateUserCommand(Command):
    """Command to update user profile."""

    ALLOWED_FIELDS = ['name', 'email', 'phone_number']

    def __init__(self, user_id, field, value):
        self.user_id = user_id
        self.field = field
        self.value = value

    def validate(self):
        if self.field not in self.ALLOWED_FIELDS:
            raise ValueError(
                f"Invalid field '{self.field}'. Allowed fields: {', '.join(self.ALLOWED_FIELDS)}"
            )

        if not self.value:
            raise ValueError(f"Value for '{self.field}' cannot be empty")

        try:
            self.user = User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            raise ValueError(f"User with ID {self.user_id} not found")

        # Validate email format
        if self.field == 'email' and '@' not in self.value:
            raise ValueError("Invalid email format")

        # Check for duplicate email
        if self.field == 'email' and User.objects.filter(email=self.value).exclude(id=self.user_id).exists():
            raise ValueError(f"Email '{self.value}' is already in use")

    def execute(self):
        setattr(self.user, self.field, self.value)
        self.user.save()

        return f"✓ User {self.user.username}'s {self.field} updated to '{self.value}'"


class ShowBalanceCommand(Command):
    """Command to show user's total balance."""

    def __init__(self, user_id):
        self.user_id = user_id

    def validate(self):
        try:
            self.user = User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            raise ValueError(f"User with ID {self.user_id} not found")

    def execute(self):
        from splitwise_app.models import UserExpense, UserExpenseType
        from collections import defaultdict

        # Get all transactions for this user
        paid = UserExpense.objects.filter(
            user=self.user,
            type=UserExpenseType.PAID
        ).select_related('expense')

        owed = UserExpense.objects.filter(
            user=self.user,
            type=UserExpenseType.OWED
        ).select_related('expense')

        # Calculate balance with other users
        balances = defaultdict(float)

        for payment in paid:
            expense = payment.expense
            # Find who owes for this expense
            owes = UserExpense.objects.filter(
                expense=expense,
                type=UserExpenseType.OWED
            ).exclude(user=self.user)

            for owe in owes:
                # This user paid, so others owe them
                balances[owe.user.name] += float(owe.amount)

        for owing in owed:
            expense = owing.expense
            # Find who paid for this expense
            payments = UserExpense.objects.filter(
                expense=expense,
                type=UserExpenseType.PAID
            ).exclude(user=self.user)

            for payment in payments:
                # This user owes to the payer
                balances[payment.user.name] -= float(owing.amount)

        # Calculate total
        total_balance = sum(balances.values())

        # Format output
        output = [f"\n{'='*60}"]
        output.append(f"BALANCE FOR: {self.user.name} (@{self.user.username})")
        output.append(f"{'='*60}\n")

        if not balances:
            output.append("No transactions yet. You're all settled up! ✓")
        else:
            for person, balance in sorted(balances.items(), key=lambda x: -x[1]):
                if abs(balance) < 0.01:  # Skip negligible amounts
                    continue

                if balance > 0:
                    output.append(f"  {person} owes you: ₹{balance:.2f}")
                else:
                    output.append(f"  You owe {person}: ₹{abs(balance):.2f}")

        output.append(f"\n{'='*60}")
        if total_balance > 0:
            output.append(f"TOTAL: You are owed ₹{total_balance:.2f}")
        elif total_balance < 0:
            output.append(f"TOTAL: You owe ₹{abs(total_balance):.2f}")
        else:
            output.append("TOTAL: You're all settled up! ✓")
        output.append(f"{'='*60}")

        return '\n'.join(output)


class ShowUserExpensesCommand(Command):
    """Command to show all expenses involving a user."""

    def __init__(self, user_id):
        self.user_id = user_id

    def validate(self):
        try:
            self.user = User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            raise ValueError(f"User with ID {self.user_id} not found")

    def execute(self):
        expenses = self.user.get_expenses()

        output = [f"\n{'='*60}"]
        output.append(f"EXPENSES FOR: {self.user.name} (@{self.user.username})")
        output.append(f"{'='*60}\n")

        if not expenses.exists():
            output.append("No expenses found.")
        else:
            for expense in expenses:
                output.append(f"\n[{expense.created_at.strftime('%Y-%m-%d %H:%M')}]")
                output.append(f"  Description: {expense.description}")
                output.append(f"  Total Amount: ₹{expense.total_amount}")
                if expense.group:
                    output.append(f"  Group: {expense.group.name}")

                # Show who paid
                paid_by = expense.get_paid_by()
                output.append("  Paid by:")
                for ue in paid_by:
                    output.append(f"    - {ue.user.name}: ₹{ue.amount}")

                # Show who owes
                owed_by = expense.get_paid_for()
                output.append("  Owed by:")
                for ue in owed_by:
                    output.append(f"    - {ue.user.name}: ₹{ue.amount}")
                output.append("-" * 60)

        return '\n'.join(output)
