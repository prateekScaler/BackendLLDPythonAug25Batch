

from abc import ABC, abstractmethod
from ..models.Board import Board
from ..enums.Symbol import Symbol


class WinningStrategy(ABC):
    @abstractmethod
    def has_won(self, board: Board, symbol: Symbol) -> bool:
        pass