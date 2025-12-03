from ..models.Board import Board
from ..models.Player import Player
from ..strategies.WinningStrategy import WinningStrategy


class GameController:
    def __init__(self, board: Board, players: list[Player], winning_strategies: list[WinningStrategy]):
        self.board = board
        self.players = players
        self.winning_strategies = winning_strategies
        self.current_player_index = 0

    def start_game(self):
        while True:
            print(f"\n{'=' * 20}")
            print(f"Turn: {self.players[self.current_player_index].symbol.value}'s move")
            print("=" * 20)
            self.board.print()
            player = self.players[self.current_player_index]
            cell = player.play(self.board)
            self.board.update(cell)

            if self.check_winner(player.symbol):
                self.board.print()
                print(f"Player {player.symbol.value} wins!")
                break

            if len(self.board.get_available_cells()) == 0:
                self.board.print()
                print("Game over!")
                break

            self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def check_winner(self, symbol):
        for strategy in self.winning_strategies:
            if strategy.has_won(self.board, symbol):
                return True
        return False
