
from dataclasses import dataclass
from .Player import Player
from .Board import Board
from .Cell import Cell
from .User import User
from ..exceptions.invalid_move_error import InvalidMoveError

@dataclass
class HumanPlayer(Player):
    user: User

    def __init__(self, user: User, symbol):
        super().__init__(symbol)   # initialize Player with correct symbol
        self.user = user           # assign user correctly

    def play(self, board: Board) -> Cell:
        while True:
            try:
                row = int(input("Enter row: "))
                col = int(input("Enter col: "))
                if not (0 <= row < board.size and 0 <= col < board.size):
                    raise InvalidMoveError("Coordinates are out of bounds.")
                if board.cells[row][col].symbol is not None:
                    raise InvalidMoveError("Cell already occupied.")
                return Cell(row, col, self.symbol)
            except ValueError:
                print("Invalid input. Please enter numbers only.")
            except InvalidMoveError as e:
                print(e.message)
