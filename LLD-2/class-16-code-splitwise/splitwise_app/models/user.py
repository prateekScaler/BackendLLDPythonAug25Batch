from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from .base import BaseModel


class User(BaseModel):
    """
    User model for Splitwise application.
    Stores user profile information and credentials.
    """
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=15)
    hashed_password = models.CharField(max_length=128)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.name} (@{self.username})"

    def set_password(self, raw_password):
        """Hash and set the user's password."""
        self.hashed_password = make_password(raw_password)

    def check_password(self, raw_password):
        """Verify if the provided password matches the hashed password."""
        return check_password(raw_password, self.hashed_password)

    def get_balance(self):
        """
        Calculate the user's total balance across all expenses.
        Positive = user is owed money
        Negative = user owes money
        """
        from .expense import UserExpense, UserExpenseType

        paid = UserExpense.objects.filter(
            user=self,
            type=UserExpenseType.PAID
        ).aggregate(total=models.Sum('amount'))['total'] or 0

        owed = UserExpense.objects.filter(
            user=self,
            type=UserExpenseType.OWED
        ).aggregate(total=models.Sum('amount'))['total'] or 0

        return paid - owed

    def get_expenses(self):
        """Get all expenses the user is involved in."""
        from .expense import Expense
        return Expense.objects.filter(
            models.Q(userexpense__user=self)
        ).distinct().order_by('-created_at')

    def get_groups(self):
        """Get all groups the user is a member of."""
        return self.member_groups.all()
