class CommandInvoker:
    """
    The Invoker class in Command Design Pattern.
    Responsible for executing commands and maintaining command history.
    """

    def __init__(self):
        self.history = []

    def execute_command(self, command):
        """
        Execute a command after validation.

        Args:
            command: Command object to execute

        Returns:
            Result of command execution

        Raises:
            ValueError: If command validation fails
            Exception: If command execution fails
        """
        try:
            # Validate before execution
            command.validate()

            # Execute the command
            result = command.execute()

            # Store in history
            self.history.append({
                'command': str(command),
                'success': True,
                'result': result
            })

            return result

        except Exception as e:
            # Store failed command in history
            self.history.append({
                'command': str(command),
                'success': False,
                'error': str(e)
            })
            raise

    def get_history(self):
        """Get command execution history."""
        return self.history

    def clear_history(self):
        """Clear command execution history."""
        self.history = []
