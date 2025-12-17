from django.db import models
from .base import BaseModel
from .user import User
from .group import Group


class Currency(models.TextChoices):
    """Currency enum - Only INR for this implementation."""
    INR = 'INR', 'Indian Rupee'


class UserExpenseType(models.TextChoices):
    """Type of user expense - either paid or owed."""
    PAID = 'PAID', 'Paid'
    OWED = 'OWED', 'Owed'


class Expense(BaseModel):
    """
    Expense model representing a shared expense between users.
    Can be part of a group or between individual users.
    """
    description = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.INR
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='expenses_created'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='expenses',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'expenses'
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.description} - ₹{self.total_amount}"

    def get_paid_by(self):
        """Get all users who paid for this expense."""
        return self.userexpense_set.filter(type=UserExpenseType.PAID)

    def get_paid_for(self):
        """Get all users who owe for this expense."""
        return self.userexpense_set.filter(type=UserExpenseType.OWED)

    def validate_expense(self):
        """
        Validate that total paid equals total owed.
        Should be called after all UserExpense entries are created.
        """
        total_paid = self.userexpense_set.filter(
            type=UserExpenseType.PAID
        ).aggregate(total=models.Sum('amount'))['total'] or 0

        total_owed = self.userexpense_set.filter(
            type=UserExpenseType.OWED
        ).aggregate(total=models.Sum('amount'))['total'] or 0

        if abs(float(total_paid) - float(total_owed)) > 0.01:  # Allow small floating point errors
            raise ValueError(
                f"Total paid (₹{total_paid}) must equal total owed (₹{total_owed})"
            )

        if abs(float(total_paid) - float(self.total_amount)) > 0.01:
            raise ValueError(
                f"Total paid (₹{total_paid}) must equal expense amount (₹{self.total_amount})"
            )


class UserExpense(BaseModel):
    """
    Junction model between User and Expense.
    Tracks who paid what and who owes what for each expense.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(
        max_length=10,
        choices=UserExpenseType.choices
    )

    class Meta:
        db_table = 'user_expenses'
        verbose_name = 'User Expense'
        verbose_name_plural = 'User Expenses'
        indexes = [
            models.Index(fields=['user', 'type']),
            models.Index(fields=['expense', 'type']),
        ]

    def __str__(self):
        return f"{self.user.name} {self.type} ₹{self.amount} for {self.expense.description}"
