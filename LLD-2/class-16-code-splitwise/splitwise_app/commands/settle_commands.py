from .base import Command
from splitwise_app.models import User, Group, UserExpense, UserExpenseType
from collections import defaultdict
from decimal import Decimal
import heapq


class SettleUserCommand(Command):
    """
    Command to calculate settle-up transactions for a user.
    Uses greedy algorithm with heaps to minimize number of transactions.
    """

    def __init__(self, user_id):
        self.user_id = user_id

    def validate(self):
        try:
            self.user = User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            raise ValueError(f"User with ID {self.user_id} not found")

    def execute(self):
        # Calculate balances between this user and all others
        balances = self._calculate_user_balances()

        if not balances or all(abs(b) < 0.01 for b in balances.values()):
            return f"\n{self.user.name} is already settled up! ✓"

        # Generate minimal transactions
        transactions = self._minimize_transactions(balances)

        # Format output
        output = [f"\n{'='*60}"]
        output.append(f"SETTLE-UP FOR: {self.user.name} (@{self.user.username})")
        output.append(f"{'='*60}\n")

        if not transactions:
            output.append("No transactions needed. You're settled up! ✓")
        else:
            output.append(f"Suggested transactions ({len(transactions)} total):\n")
            for i, txn in enumerate(transactions, 1):
                output.append(f"{i}. {txn}")

        output.append(f"\n{'='*60}")
        return '\n'.join(output)

    def _calculate_user_balances(self):
        """Calculate net balance between this user and each other user."""
        balances = defaultdict(Decimal)

        # Get all expenses involving this user
        paid = UserExpense.objects.filter(
            user=self.user,
            type=UserExpenseType.PAID
        ).select_related('expense')

        owed = UserExpense.objects.filter(
            user=self.user,
            type=UserExpenseType.OWED
        ).select_related('expense')

        # For each expense where this user paid
        for payment in paid:
            expense = payment.expense
            # Find who owes for this expense
            owes = UserExpense.objects.filter(
                expense=expense,
                type=UserExpenseType.OWED
            ).exclude(user=self.user).select_related('user')

            for owe in owes:
                # Other users owe this user
                balances[owe.user] += Decimal(str(owe.amount))

        # For each expense where this user owes
        for owing in owed:
            expense = owing.expense
            # Find who paid for this expense
            payments = UserExpense.objects.filter(
                expense=expense,
                type=UserExpenseType.PAID
            ).exclude(user=self.user).select_related('user')

            for payment in payments:
                # This user owes the payer
                balances[payment.user] -= Decimal(str(owing.amount))

        # Filter out zero/negligible balances
        return {user: amt for user, amt in balances.items() if abs(amt) > Decimal('0.01')}

    def _minimize_transactions(self, balances):
        """
        Minimize transactions using greedy algorithm with heaps.
        Positive balance = others owe this user
        Negative balance = this user owes others
        """
        transactions = []

        # Separate creditors (who this user owes) and debtors (who owe this user)
        creditors = []  # Max heap (use negative values)
        debtors = []    # Max heap (use negative values)

        for other_user, balance in balances.items():
            if balance > 0:
                # This user is owed by other_user
                heapq.heappush(debtors, (-float(balance), other_user))
            elif balance < 0:
                # This user owes other_user
                heapq.heappush(creditors, (float(balance), other_user))

        # Settle debts
        while creditors and debtors:
            # Get the largest debt this user owes
            debt_amount, creditor = heapq.heappop(creditors)
            debt_amount = abs(debt_amount)

            # Get the largest amount this user is owed
            credit_amount, debtor = heapq.heappop(debtors)
            credit_amount = abs(credit_amount)

            # Settle the minimum of the two
            settle_amount = min(debt_amount, credit_amount)

            transactions.append(
                f"{self.user.name} pays ₹{settle_amount:.2f} to {creditor.name}"
            )

            # If there's remaining debt/credit, push back to heap
            remaining_debt = debt_amount - settle_amount
            remaining_credit = credit_amount - settle_amount

            if remaining_debt > 0.01:
                heapq.heappush(creditors, (-remaining_debt, creditor))

            if remaining_credit > 0.01:
                heapq.heappush(debtors, (-remaining_credit, debtor))

        return transactions


class SettleGroupCommand(Command):
    """
    Command to calculate settle-up transactions for a group.
    Minimizes total number of transactions needed to settle all group members.
    """

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
            raise PermissionError(f"You must be a member of '{self.group.name}' to view settle-up")

    def execute(self):
        # Calculate net balance for each member
        balances = self._calculate_group_balances()

        if not balances or all(abs(b) < 0.01 for b in balances.values()):
            return f"\nGroup '{self.group.name}' is already settled up! ✓"

        # Generate minimal transactions
        transactions = self._minimize_group_transactions(balances)

        # Format output
        output = [f"\n{'='*60}"]
        output.append(f"SETTLE-UP FOR GROUP: {self.group.name}")
        output.append(f"{'='*60}\n")

        output.append("Current Balances:")
        for user, balance in sorted(balances.items(), key=lambda x: -x[1]):
            if balance > 0:
                output.append(f"  {user.name}: +₹{balance:.2f} (to receive)")
            elif balance < 0:
                output.append(f"  {user.name}: -₹{abs(balance):.2f} (to pay)")
            else:
                output.append(f"  {user.name}: ₹0.00 (settled)")

        output.append(f"\n{'-'*60}")

        if not transactions:
            output.append("\nNo transactions needed. Group is settled up! ✓")
        else:
            output.append(f"\nSuggested transactions ({len(transactions)} total):\n")
            for i, txn in enumerate(transactions, 1):
                output.append(f"{i}. {txn}")

        output.append(f"\n{'='*60}")
        return '\n'.join(output)

    def _calculate_group_balances(self):
        """Calculate net balance for each group member based on group expenses."""
        balances = defaultdict(Decimal)

        # Get all expenses in this group
        expenses = self.group.expenses.all()

        for expense in expenses:
            # Get who paid
            payments = UserExpense.objects.filter(
                expense=expense,
                type=UserExpenseType.PAID
            ).select_related('user')

            # Get who owes
            owes = UserExpense.objects.filter(
                expense=expense,
                type=UserExpenseType.OWED
            ).select_related('user')

            # Update balances
            for payment in payments:
                balances[payment.user] += Decimal(str(payment.amount))

            for owe in owes:
                balances[owe.user] -= Decimal(str(owe.amount))

        # Filter out zero/negligible balances
        return {user: amt for user, amt in balances.items() if abs(amt) > Decimal('0.01')}

    def _minimize_group_transactions(self, balances):
        """
        Minimize transactions for the entire group using greedy algorithm.
        This uses a two-heap approach to match largest debts with largest credits.
        """
        transactions = []

        # Create max heaps for creditors (to receive) and debtors (to pay)
        creditors = []  # People who should receive money (positive balance)
        debtors = []    # People who should pay money (negative balance)

        for user, balance in balances.items():
            if balance > 0:
                # This person should receive money
                heapq.heappush(creditors, (-float(balance), user))
            elif balance < 0:
                # This person should pay money
                heapq.heappush(debtors, (float(balance), user))

        # Match debtors with creditors
        while creditors and debtors:
            # Get largest creditor (person owed the most)
            credit_amount, creditor = heapq.heappop(creditors)
            credit_amount = abs(credit_amount)

            # Get largest debtor (person who owes the most)
            debt_amount, debtor = heapq.heappop(debtors)
            debt_amount = abs(debt_amount)

            # Settle the minimum of the two
            settle_amount = min(credit_amount, debt_amount)

            transactions.append(
                f"{debtor.name} pays ₹{settle_amount:.2f} to {creditor.name}"
            )

            # If there's remaining balance, push back to heap
            remaining_credit = credit_amount - settle_amount
            remaining_debt = debt_amount - settle_amount

            if remaining_credit > 0.01:
                heapq.heappush(creditors, (-remaining_credit, creditor))

            if remaining_debt > 0.01:
                heapq.heappush(debtors, (-remaining_debt, debtor))

        return transactions
