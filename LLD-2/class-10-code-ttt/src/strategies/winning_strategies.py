from ..strategies.WinningStrategy import WinningStrategy
from ..models.Board import Board
from ..enums.Symbol import Symbol


class RowWinningStrategy(WinningStrategy):
    def has_won(self, board: Board, symbol: Symbol) -> bool:
        for row in board.cells:
            if all(cell.symbol == symbol for cell in row):
                return True
        return False


class ColWinningStrategy(WinningStrategy):
    def has_won(self, board: Board, symbol: Symbol) -> bool:
        for col_idx in range(board.size):
            if all(board.cells[row_idx][col_idx].symbol == symbol for row_idx in range(board.size)):
                return True
        return False


class DiagonalWinningStrategy(WinningStrategy):
    def has_won(self, board: Board, symbol: Symbol) -> bool:
        # Main diagonal
        if all(board.cells[i][i].symbol == symbol for i in range(board.size)):
            return True

        # Anti-diagonal
        if all(board.cells[i][board.size - 1 - i].symbol == symbol for i in range(board.size)):
            return True

        return False
