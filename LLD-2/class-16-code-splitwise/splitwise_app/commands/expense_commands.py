from .base import Command
from splitwise_app.models import User, Group, Expense, UserExpense, UserExpenseType
from decimal import Decimal


class AddExpenseCommand(Command):
    """Command to add a new expense."""

    def __init__(self, description, amount, created_by_id, group_id, paid_by, owed_by):
        """
        Args:
            description: Expense description
            amount: Total amount
            created_by_id: User ID who created the expense
            group_id: Group ID (None for personal expenses)
            paid_by: Dict of {user_id: amount} for who paid
            owed_by: Dict of {user_id: amount} for who owes
        """
        self.description = description
        self.amount = Decimal(str(amount))
        self.created_by_id = created_by_id
        self.group_id = group_id
        self.paid_by = paid_by
        self.owed_by = owed_by

    def validate(self):
        if not self.description:
            raise ValueError("Description is required")

        if self.amount <= 0:
            raise ValueError("Amount must be positive")

        try:
            self.created_by = User.objects.get(id=self.created_by_id)
        except User.DoesNotExist:
            raise ValueError(f"User with ID {self.created_by_id} not found")

        if self.group_id:
            try:
                self.group = Group.objects.get(id=self.group_id)
                if not self.group.is_member(self.created_by):
                    raise ValueError("You must be a member of the group to add expenses")
            except Group.DoesNotExist:
                raise ValueError(f"Group with ID {self.group_id} not found")
        else:
            self.group = None

        # Validate paid_by users exist
        for user_id in self.paid_by.keys():
            if not User.objects.filter(id=user_id).exists():
                raise ValueError(f"User with ID {user_id} not found")

        # Validate owed_by users exist
        for user_id in self.owed_by.keys():
            if not User.objects.filter(id=user_id).exists():
                raise ValueError(f"User with ID {user_id} not found")

        # Validate amounts
        total_paid = sum(Decimal(str(amt)) for amt in self.paid_by.values())
        total_owed = sum(Decimal(str(amt)) for amt in self.owed_by.values())

        if abs(total_paid - self.amount) > Decimal('0.01'):
            raise ValueError(
                f"Total paid (₹{total_paid}) must equal expense amount (₹{self.amount})"
            )

        if abs(total_owed - self.amount) > Decimal('0.01'):
            raise ValueError(
                f"Total owed (₹{total_owed}) must equal expense amount (₹{self.amount})"
            )

    def execute(self):
        # Create expense
        expense = Expense.objects.create(
            description=self.description,
            total_amount=self.amount,
            created_by=self.created_by,
            group=self.group
        )

        # Create UserExpense entries for who paid
        for user_id, amount in self.paid_by.items():
            user = User.objects.get(id=user_id)
            UserExpense.objects.create(
                user=user,
                expense=expense,
                amount=Decimal(str(amount)),
                type=UserExpenseType.PAID
            )

        # Create UserExpense entries for who owes
        for user_id, amount in self.owed_by.items():
            user = User.objects.get(id=user_id)
            UserExpense.objects.create(
                user=user,
                expense=expense,
                amount=Decimal(str(amount)),
                type=UserExpenseType.OWED
            )

        # Validate the expense
        expense.validate_expense()

        group_info = f" in group '{self.group.name}'" if self.group else ""
        return f"✓ Expense '{expense.description}' (₹{expense.total_amount}) added successfully{group_info}! ID: {expense.id}"
