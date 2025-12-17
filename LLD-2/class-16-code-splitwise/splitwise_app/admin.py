from django.contrib import admin
from .models import User, Group, Expense, UserExpense
from .models.group import GroupMembership


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'phone_number', 'created_at')
    search_fields = ('username', 'name', 'email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'joined_at')
    search_fields = ('group__name', 'user__name')


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
