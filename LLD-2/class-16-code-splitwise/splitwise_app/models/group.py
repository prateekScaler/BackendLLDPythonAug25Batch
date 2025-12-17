from django.db import models
from .base import BaseModel
from .user import User


class Group(BaseModel):
    """
    Group model for organizing expenses among multiple users.
    """
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_groups'
    )
    members = models.ManyToManyField(
        User,
        related_name='member_groups',
        through='GroupMembership'
    )

    class Meta:
        db_table = 'groups'
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return self.name

    def add_member(self, user, added_by):
        """Add a member to the group. Only creator can add members."""
        if added_by != self.created_by:
            raise PermissionError("Only the group creator can add members")

        if not self.members.filter(id=user.id).exists():
            GroupMembership.objects.create(group=self, user=user)

    def remove_member(self, user, removed_by):
        """Remove a member from the group. Only creator can remove members."""
        if removed_by != self.created_by:
            raise PermissionError("Only the group creator can remove members")

        if user == self.created_by:
            raise ValueError("Cannot remove the group creator")

        GroupMembership.objects.filter(group=self, user=user).delete()

    def is_member(self, user):
        """Check if a user is a member of this group."""
        return self.members.filter(id=user.id).exists()

    def get_expenses(self):
        """Get all expenses in this group."""
        return self.expenses.all().order_by('-created_at')


class GroupMembership(BaseModel):
    """
    Through model for Group-User many-to-many relationship.
    Tracks when users joined groups.
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'group_memberships'
        unique_together = ('group', 'user')
        verbose_name = 'Group Membership'
        verbose_name_plural = 'Group Memberships'

    def __str__(self):
        return f"{self.user.name} in {self.group.name}"
