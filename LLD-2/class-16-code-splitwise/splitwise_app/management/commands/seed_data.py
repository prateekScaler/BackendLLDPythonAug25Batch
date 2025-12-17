from django.core.management.base import BaseCommand
from splitwise_app.models import User, Group, Expense, UserExpense, UserExpenseType


class Command(BaseCommand):
    help = 'Seed database with sample Indian data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database with sample data...\n')

        # Clear existing data (makes this command idempotent)
        self.stdout.write('Clearing existing seed data...')
        UserExpense.objects.all().delete()
        Expense.objects.all().delete()
        Group.objects.all().delete()
        User.objects.all().delete()

        # Reset SQLite auto-increment counters (so IDs start from 1)
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='groups'")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='expenses'")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='user_expenses'")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='group_memberships'")

        self.stdout.write(self.style.WARNING('  ✓ Cleared existing data\n'))

        # Create users
        users_data = [
            ('rajesh_sharma', 'Rajesh Sharma', 'rajesh.sharma@email.com', '9876543210', 'pass123'),
            ('priya_patel', 'Priya Patel', 'priya.patel@email.com', '9876543211', 'pass123'),
            ('amit_kumar', 'Amit Kumar', 'amit.kumar@email.com', '9876543212', 'pass123'),
            ('sneha_reddy', 'Sneha Reddy', 'sneha.reddy@email.com', '9876543213', 'pass123'),
            ('vikram_singh', 'Vikram Singh', 'vikram.singh@email.com', '9876543214', 'pass123'),
        ]

        users = []
        for username, name, email, phone, password in users_data:
            user = User(
                username=username,
                name=name,
                email=email,
                phone_number=phone
            )
            user.set_password(password)
            user.save()
            users.append(user)
            self.stdout.write(f'  ✓ Created user: {name} (ID: {user.id})')

        # Create groups
        groups_data = [
            ('Goa Trip 2025', users[0]),
            ('Office Lunch Group', users[1]),
            ('Roommates - Mumbai', users[2]),
        ]

        groups = []
        for group_name, creator in groups_data:
            group = Group.objects.create(name=group_name, created_by=creator)
            group.add_member(creator, creator)
            groups.append(group)
            self.stdout.write(f'  ✓ Created group: {group_name} (ID: {group.id})')

        # Add members to groups
        # Goa Trip: Rajesh (creator), Priya, Amit, Sneha
        for user in [users[1], users[2], users[3]]:
            groups[0].add_member(user, users[0])

        # Office Lunch: Priya (creator), Vikram, Rajesh
        for user in [users[4], users[0]]:
            groups[1].add_member(user, users[1])

        # Roommates: Amit (creator), Sneha
        groups[2].add_member(users[3], users[2])

        self.stdout.write('  ✓ Added members to groups')

        # Create expenses
        expenses_data = [
            # Goa Trip expenses
            {
                'description': 'Hotel Booking - Goa',
                'amount': 12000,
                'created_by': users[0],
                'group': groups[0],
                'paid_by': {users[0]: 12000},
                'owed_by': {users[0]: 3000, users[1]: 3000, users[2]: 3000, users[3]: 3000}
            },
            {
                'description': 'Dinner at Beach Shack',
                'amount': 2400,
                'created_by': users[1],
                'group': groups[0],
                'paid_by': {users[1]: 2400},
                'owed_by': {users[0]: 600, users[1]: 600, users[2]: 600, users[3]: 600}
            },
            {
                'description': 'Cab to Airport',
                'amount': 800,
                'created_by': users[2],
                'group': groups[0],
                'paid_by': {users[2]: 800},
                'owed_by': {users[0]: 200, users[1]: 200, users[2]: 200, users[3]: 200}
            },
            # Office Lunch expenses
            {
                'description': 'Team Lunch - Barbeque Nation',
                'amount': 1800,
                'created_by': users[1],
                'group': groups[1],
                'paid_by': {users[1]: 1800},
                'owed_by': {users[1]: 600, users[4]: 600, users[0]: 600}
            },
            {
                'description': 'Coffee Break',
                'amount': 450,
                'created_by': users[4],
                'group': groups[1],
                'paid_by': {users[4]: 450},
                'owed_by': {users[1]: 150, users[4]: 150, users[0]: 150}
            },
            # Roommate expenses
            {
                'description': 'Monthly Electricity Bill',
                'amount': 1500,
                'created_by': users[2],
                'group': groups[2],
                'paid_by': {users[2]: 1500},
                'owed_by': {users[2]: 750, users[3]: 750}
            },
            {
                'description': 'Grocery Shopping - DMart',
                'amount': 2500,
                'created_by': users[3],
                'group': groups[2],
                'paid_by': {users[3]: 2500},
                'owed_by': {users[2]: 1250, users[3]: 1250}
            },
            # Personal expenses (no group)
            {
                'description': 'Movie Tickets',
                'amount': 600,
                'created_by': users[0],
                'group': None,
                'paid_by': {users[0]: 600},
                'owed_by': {users[0]: 300, users[1]: 300}
            },
            {
                'description': 'Uber Ride',
                'amount': 350,
                'created_by': users[2],
                'group': None,
                'paid_by': {users[2]: 350},
                'owed_by': {users[2]: 175, users[4]: 175}
            },
        ]

        for exp_data in expenses_data:
            expense = Expense.objects.create(
                description=exp_data['description'],
                total_amount=exp_data['amount'],
                created_by=exp_data['created_by'],
                group=exp_data['group']
            )

            # Create UserExpense for who paid
            for user, amount in exp_data['paid_by'].items():
                UserExpense.objects.create(
                    user=user,
                    expense=expense,
                    amount=amount,
                    type=UserExpenseType.PAID
                )

            # Create UserExpense for who owes
            for user, amount in exp_data['owed_by'].items():
                UserExpense.objects.create(
                    user=user,
                    expense=expense,
                    amount=amount,
                    type=UserExpenseType.OWED
                )

            group_info = f" in {expense.group.name}" if expense.group else " (personal)"
            self.stdout.write(f'  ✓ Created expense: {expense.description}{group_info}')

        self.stdout.write(self.style.SUCCESS('\n✓ Database seeded successfully!'))
        self.stdout.write('\n' + '='*60)
        self.stdout.write('SUMMARY')
        self.stdout.write('='*60)
        self.stdout.write(f'  Users created: {User.objects.count()}')
        self.stdout.write(f'  Groups created: {Group.objects.count()}')
        self.stdout.write(f'  Expenses created: {Expense.objects.count()}')
        self.stdout.write(f'  UserExpense records: {UserExpense.objects.count()}')
        self.stdout.write('='*60)
        self.stdout.write('\nSample users (all passwords: pass123):')
        for i, user in enumerate(users, 1):
            self.stdout.write(f'  {i}. {user.name} (ID: {user.id}, Username: {user.username})')
        self.stdout.write('\nYou can now run: python cli.py')
