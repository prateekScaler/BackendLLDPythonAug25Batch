from abc import ABC, abstractmethod


class Command(ABC):
    """
    Abstract base class for all commands in the Command Design Pattern.
    Each concrete command encapsulates a specific operation with its parameters.
    """

    @abstractmethod
    def execute(self):
        """
        Execute the command operation.
        Returns: Result of the command execution
        """
        pass

    @abstractmethod
    def validate(self):
        """
        Validate command parameters before execution.
        Raises: ValueError if validation fails
        """
        pass

    def __str__(self):
        return self.__class__.__name__
