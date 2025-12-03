from src.controllers.game_controller import GameController
from src.models.Board import Board
from src.models.BotPlayer import BotPlayer
from src.models.HumanPlayer import HumanPlayer
from src.models.User import User
from src.enums.Symbol import Symbol
from src.enums.Level import Level
from src.strategies.bot_playing_strategies import EasyBotPlayingStrategy
from src.strategies.winning_strategies import (
    RowWinningStrategy,
    ColWinningStrategy,
    DiagonalWinningStrategy,
)


def main():
    board = Board(3)
    user = User("Sumit Kumar", "sumit.kumar@scaler.com")
    human_player = HumanPlayer(user, Symbol.X)
    bot_player = BotPlayer(Symbol.O, Level.EASY, EasyBotPlayingStrategy())
    players = [human_player, bot_player]
    winning_strategies = [RowWinningStrategy(), ColWinningStrategy(), DiagonalWinningStrategy()]
    game_controller = GameController(board, players, winning_strategies)
    game_controller.start_game()


if __name__ == "__main__":
    main()
