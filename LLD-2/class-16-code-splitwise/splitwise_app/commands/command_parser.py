from .user_commands import (
    RegisterUserCommand,
    UpdateUserCommand,
    ShowBalanceCommand,
    ShowUserExpensesCommand,
)
from .group_commands import (
    CreateGroupCommand,
    AddMemberCommand,
    RemoveMemberCommand,
    ShowGroupExpensesCommand,
)
from .expense_commands import (
    AddExpenseCommand,
)
from .settle_commands import (
    SettleUserCommand,
    SettleGroupCommand,
)


class CommandParser:
    """
    Parser that converts user input strings into Command objects.
    Tokenizes and parses CLI input to create appropriate command instances.
    """

    def __init__(self):
        self.command_map = {
            'REGISTER': self._parse_register,
            'UPDATE_USER': self._parse_update_user,
            'CREATE_GROUP': self._parse_create_group,
            'ADD_MEMBER': self._parse_add_member,
            'REMOVE_MEMBER': self._parse_remove_member,
            'ADD_EXPENSE': self._parse_add_expense,
            'SHOW_BALANCE': self._parse_show_balance,
            'SHOW_USER_EXPENSES': self._parse_show_user_expenses,
            'SHOW_GROUP_EXPENSES': self._parse_show_group_expenses,
            'SETTLE_USER': self._parse_settle_user,
            'SETTLE_GROUP': self._parse_settle_group,
            'HELP': self._parse_help,
            'EXIT': self._parse_exit,
        }

    def parse(self, input_string):
        """
        Parse input string and return appropriate Command object.

        Args:
            input_string: Raw CLI input from user

        Returns:
            Command object or None for EXIT

        Raises:
            ValueError: If command is invalid or malformed
        """
        tokens = self._tokenize(input_string)

        if not tokens:
            raise ValueError("Empty command")

        command_name = tokens[0].upper()

        if command_name not in self.command_map:
            raise ValueError(f"Unknown command: {command_name}")

        return self.command_map[command_name](tokens[1:])

    def _tokenize(self, input_string):
        """
        Tokenize input string by splitting on whitespace.
        Handles quoted strings as single tokens.
        """
        tokens = []
        current_token = []
        in_quotes = False

        for char in input_string:
            if char == '"':
                in_quotes = not in_quotes
            elif char.isspace() and not in_quotes:
                if current_token:
                    tokens.append(''.join(current_token))
                    current_token = []
            else:
                current_token.append(char)

        if current_token:
            tokens.append(''.join(current_token))

        return tokens

    def _parse_register(self, tokens):
        """REGISTER <username> <name> <email> <phone> <password>"""
        if len(tokens) < 5:
            raise ValueError("Usage: REGISTER <username> <name> <email> <phone> <password>")
        return RegisterUserCommand(
            username=tokens[0],
            name=tokens[1],
            email=tokens[2],
            phone_number=tokens[3],
            password=tokens[4]
        )

    def _parse_update_user(self, tokens):
        """UPDATE_USER <user_id> <field> <value>"""
        if len(tokens) < 3:
            raise ValueError("Usage: UPDATE_USER <user_id> <field> <value>")
        return UpdateUserCommand(
            user_id=int(tokens[0]),
            field=tokens[1],
            value=tokens[2]
        )

    def _parse_create_group(self, tokens):
        """CREATE_GROUP <group_name> <creator_user_id>"""
        if len(tokens) < 2:
            raise ValueError("Usage: CREATE_GROUP <group_name> <creator_user_id>")
        return CreateGroupCommand(
            name=tokens[0],
            creator_id=int(tokens[1])
        )

    def _parse_add_member(self, tokens):
        """ADD_MEMBER <group_id> <user_id> <added_by_user_id>"""
        if len(tokens) < 3:
            raise ValueError("Usage: ADD_MEMBER <group_id> <user_id> <added_by_user_id>")
        return AddMemberCommand(
            group_id=int(tokens[0]),
            user_id=int(tokens[1]),
            added_by_id=int(tokens[2])
        )

    def _parse_remove_member(self, tokens):
        """REMOVE_MEMBER <group_id> <user_id> <removed_by_user_id>"""
        if len(tokens) < 3:
            raise ValueError("Usage: REMOVE_MEMBER <group_id> <user_id> <removed_by_user_id>")
        return RemoveMemberCommand(
            group_id=int(tokens[0]),
            user_id=int(tokens[1]),
            removed_by_id=int(tokens[2])
        )

    def _parse_add_expense(self, tokens):
        """
        ADD_EXPENSE <description> <amount> <created_by_id> <group_id_or_0> <paid_by_ids:amounts> <owed_by_ids:amounts>
        Example: ADD_EXPENSE "Dinner" 1500 1 0 1:1500 1:750,2:750
        """
        if len(tokens) < 6:
            raise ValueError(
                "Usage: ADD_EXPENSE <description> <amount> <created_by_id> "
                "<group_id_or_0> <paid_by_ids:amounts> <owed_by_ids:amounts>"
            )

        # Parse paid_by and owed_by
        paid_by = self._parse_user_amounts(tokens[4])
        owed_by = self._parse_user_amounts(tokens[5])

        return AddExpenseCommand(
            description=tokens[0],
            amount=float(tokens[1]),
            created_by_id=int(tokens[2]),
            group_id=int(tokens[3]) if tokens[3] != '0' else None,
            paid_by=paid_by,
            owed_by=owed_by
        )

    def _parse_user_amounts(self, token):
        """Parse user_id:amount pairs. Format: 1:500,2:500"""
        result = {}
        pairs = token.split(',')
        for pair in pairs:
            user_id, amount = pair.split(':')
            result[int(user_id)] = float(amount)
        return result

    def _parse_show_balance(self, tokens):
        """SHOW_BALANCE <user_id>"""
        if len(tokens) < 1:
            raise ValueError("Usage: SHOW_BALANCE <user_id>")
        return ShowBalanceCommand(user_id=int(tokens[0]))

    def _parse_show_user_expenses(self, tokens):
        """SHOW_USER_EXPENSES <user_id>"""
        if len(tokens) < 1:
            raise ValueError("Usage: SHOW_USER_EXPENSES <user_id>")
        return ShowUserExpensesCommand(user_id=int(tokens[0]))

    def _parse_show_group_expenses(self, tokens):
        """SHOW_GROUP_EXPENSES <group_id> <user_id>"""
        if len(tokens) < 2:
            raise ValueError("Usage: SHOW_GROUP_EXPENSES <group_id> <user_id>")
        return ShowGroupExpensesCommand(
            group_id=int(tokens[0]),
            user_id=int(tokens[1])
        )

    def _parse_settle_user(self, tokens):
        """SETTLE_USER <user_id>"""
        if len(tokens) < 1:
            raise ValueError("Usage: SETTLE_USER <user_id>")
        return SettleUserCommand(user_id=int(tokens[0]))

    def _parse_settle_group(self, tokens):
        """SETTLE_GROUP <group_id> <user_id>"""
        if len(tokens) < 2:
            raise ValueError("Usage: SETTLE_GROUP <group_id> <user_id>")
        return SettleGroupCommand(
            group_id=int(tokens[0]),
            user_id=int(tokens[1])
        )

    def _parse_help(self, tokens):
        """HELP - Show all available commands"""
        return None  # Will be handled specially in CLI

    def _parse_exit(self, tokens):
        """EXIT - Exit the application"""
        return None

    def show_help(self):
        """Display help message with all available commands."""
        help_text = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                         SPLITWISE CLI COMMANDS                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

USER COMMANDS:
  REGISTER <username> <name> <email> <phone> <password>
    Register a new user
    Example: REGISTER rajesh_123 Rajesh rajesh@email.com 9876543210 pass123

  UPDATE_USER <user_id> <field> <value>
    Update user profile (name, email, phone_number)
    Example: UPDATE_USER 1 phone_number 9876543211

  SHOW_BALANCE <user_id>
    Show total balance for a user
    Example: SHOW_BALANCE 1

  SHOW_USER_EXPENSES <user_id>
    Show all expenses for a user
    Example: SHOW_USER_EXPENSES 1

GROUP COMMANDS:
  CREATE_GROUP <group_name> <creator_user_id>
    Create a new group
    Example: CREATE_GROUP "Goa Trip" 1

  ADD_MEMBER <group_id> <user_id> <added_by_user_id>
    Add member to group (only creator can add)
    Example: ADD_MEMBER 1 2 1

  REMOVE_MEMBER <group_id> <user_id> <removed_by_user_id>
    Remove member from group (only creator can remove)
    Example: REMOVE_MEMBER 1 2 1

  SHOW_GROUP_EXPENSES <group_id> <user_id>
    Show expenses in a group (user must be member)
    Example: SHOW_GROUP_EXPENSES 1 1

EXPENSE COMMANDS:
  ADD_EXPENSE <description> <amount> <created_by_id> <group_id_or_0> <paid_by> <owed_by>
    Add an expense
    Format for paid_by/owed_by: user_id:amount,user_id:amount
    Example: ADD_EXPENSE "Dinner" 1500 1 0 1:1500 1:750,2:750

SETTLE COMMANDS:
  SETTLE_USER <user_id>
    Show transactions to settle up a user
    Example: SETTLE_USER 1

  SETTLE_GROUP <group_id> <user_id>
    Show transactions to settle up a group
    Example: SETTLE_GROUP 1 1

OTHER:
  HELP     - Show this help message
  EXIT     - Exit the application

"""
        return help_text
