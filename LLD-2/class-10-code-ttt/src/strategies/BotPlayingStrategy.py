from abc import ABC, abstractmethod
from ..models.Board import Board
from ..models.Cell import Cell
from ..enums.Symbol import Symbol


class BotPlayingStrategy(ABC):
    @abstractmethod
    def get_move(self, board: Board, symbol: Symbol) -> Cell:
        pass
