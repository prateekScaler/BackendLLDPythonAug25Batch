from dataclasses import dataclass
from .Board import Board
from .Player import Player
from .Cell import Cell
from ..enums.Level import Level
from ..strategies.bot_playing_strategies import BotPlayingStrategy


@dataclass
class BotPlayer(Player):
    difficulty_level: Level
    playing_strategy: BotPlayingStrategy

    def play(self, board: Board) -> Cell:
        return self.playing_strategy.get_move(board, self.symbol)
