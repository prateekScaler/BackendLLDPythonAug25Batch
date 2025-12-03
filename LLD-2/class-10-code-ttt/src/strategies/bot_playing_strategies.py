from ..strategies.BotPlayingStrategy import BotPlayingStrategy
from ..models.Board import Board
from ..models.Cell import Cell
from ..enums.Symbol import Symbol


class EasyBotPlayingStrategy(BotPlayingStrategy):
    def get_move(self, board: Board, symbol: Symbol) -> Cell:
        for row in board.cells:
            for cell in row:
                if cell.symbol is None:
                    return Cell(cell.row, cell.column, symbol)
        return None
