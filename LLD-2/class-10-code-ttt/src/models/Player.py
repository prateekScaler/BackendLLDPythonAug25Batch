from abc import abstractmethod, ABC
from dataclasses import dataclass
from .Board import Board
from .Cell import Cell
from ..enums.Symbol import Symbol


@dataclass
class Player(ABC):
    """Abstract base class for a player in the game."""
    symbol: Symbol

    @abstractmethod
    def play(self, board: Board) -> Cell:
        pass
