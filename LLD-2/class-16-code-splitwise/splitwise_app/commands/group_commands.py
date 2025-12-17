from .base import Command
from splitwise_app.models import User, Group


class CreateGroupCommand(Command):
    """Command to create a new group."""

    def __init__(self, name, creator_id):
        self.name = name
        self.creator_id = creator_id

    def validate(self):
        if not self.name:
            raise ValueError("Group name is required")

        try:
            self.creator = User.objects.get(id=self.creator_id)
        except User.DoesNotExist:
            raise ValueError(f"User with ID {self.creator_id} not found")

    def execute(self):
        group = Group.objects.create(
            name=self.name,
            created_by=self.creator
        )
        # Add creator as member
        group.add_member(self.creator, self.creator)

        return f"✓ Group '{group.name}' created successfully! ID: {group.id}"


class AddMemberCommand(Command):
    """Command to add a member to a group."""

    def __init__(self, group_id, user_id, added_by_id):
        self.group_id = group_id
        self.user_id = user_id
        self.added_by_id = added_by_id

    def validate(self):
        try:
            self.group = Group.objects.get(id=self.group_id)
        except Group.DoesNotExist:
            raise ValueError(f"Group with ID {self.group_id} not found")

        try:
            self.user = User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            raise ValueError(f"User with ID {self.user_id} not found")

        try:
            self.added_by = User.objects.get(id=self.added_by_id)
        except User.DoesNotExist:
            raise ValueError(f"User with ID {self.added_by_id} not found")

        if self.added_by != self.group.created_by:
            raise PermissionError("Only the group creator can add members")

        if self.group.is_member(self.user):
            raise ValueError(f"{self.user.name} is already a member of this group")

    def execute(self):
        self.group.add_member(self.user, self.added_by)
        return f"✓ {self.user.name} added to group '{self.group.name}'"


class RemoveMemberCommand(Command):
    """Command to remove a member from a group."""

    def __init__(self, group_id, user_id, removed_by_id):
        self.group_id = group_id
        self.user_id = user_id
        self.removed_by_id = removed_by_id

    def validate(self):
        try:
            self.group = Group.objects.get(id=self.group_id)
        except Group.DoesNotExist:
            raise ValueError(f"Group with ID {self.group_id} not found")

        try:
            self.user = User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            raise ValueError(f"User with ID {self.user_id} not found")

        try:
            self.removed_by = User.objects.get(id=self.removed_by_id)
        except User.DoesNotExist:
            raise ValueError(f"User with ID {self.removed_by_id} not found")

        if self.removed_by != self.group.created_by:
            raise PermissionError("Only the group creator can remove members")

        if not self.group.is_member(self.user):
            raise ValueError(f"{self.user.name} is not a member of this group")

        if self.user == self.group.created_by:
            raise ValueError("Cannot remove the group creator")

    def execute(self):
        self.group.remove_member(self.user, self.removed_by)
        return f"✓ {self.user.name} removed from group '{self.group.name}'"


class ShowGroupExpensesCommand(Command):
    """Command to show all expenses in a group."""

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
            raise PermissionError(f"You must be a member of '{self.group.name}' to view its expenses")

    def execute(self):
        expenses = self.group.get_expenses()

        output = [f"\n{'='*60}"]
        output.append(f"EXPENSES FOR GROUP: {self.group.name}")
        output.append(f"{'='*60}\n")

        if not expenses.exists():
            output.append("No expenses in this group yet.")
        else:
            for expense in expenses:
                output.append(f"\n[{expense.created_at.strftime('%Y-%m-%d %H:%M')}]")
                output.append(f"  Description: {expense.description}")
                output.append(f"  Total Amount: ₹{expense.total_amount}")
                output.append(f"  Created by: {expense.created_by.name}")

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
