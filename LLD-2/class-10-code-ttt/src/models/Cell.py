from dataclasses import dataclass
from ..enums.Symbol import Symbol


@dataclass
class Cell:
    row: int
    column: int
    symbol: Symbol = None
