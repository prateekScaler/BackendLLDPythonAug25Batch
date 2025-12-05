# Code Structuring & Design Issues - Tic-Tac-Toe

Comprehensive guide for improving the Tic-Tac-Toe design for LLD interviews.

---

## CRITICAL ISSUES (Must Fix for Interviews)

### 1. Missing Game Model

**Problem:** `GameController` directly holds game state (board, players, current_player_index). Controller is both orchestrating AND storing state, violating SRP.

**Solution:** Create a `Game` model class:
```python
@dataclass
class Game:
    board: Board
    players: List[Player]
    moves: List[Move]  # Move history
    winning_strategies: List[WinningStrategy]
    current_player_index: int = 0
    status: GameStatus = GameStatus.IN_PROGRESS
    winner: Player = None
```

**Impact:** Enables proper separation of concerns, makes state serializable, enables save/load functionality.

---

### 2. Missing Service Layer & Fat Controller

**Problem:** `GameController.start_game()` contains business logic (checking winners, managing turns, I/O). Controller should orchestrate, not implement logic.

**Current:** `main.py` → `GameController` (business logic + I/O + orchestration)

**Solution:** Add `GameService` for business logic:
```python
class GameService:
    def make_move(self, game: Game, row: int, col: int) -> Move
    def check_winner(self, game: Game) -> Optional[Player]
    def is_draw(self, game: Game) -> bool
    def get_next_player(self, game: Game) -> Player
    def undo_move(self, game: Game) -> bool  # Bonus feature
```

**Refactored Flow:**
```
main.py → GameController (orchestration) → GameService (logic) → Models
                ↓
          DisplayService (UI)
```

---

### 3. Builder Pattern for Game Construction

**Problem:** Direct construction in `main.py` with no validation. No way to ensure valid game state before starting.

**Solution:** `GameBuilder` + `GameValidator` + optional `GameDirector`

```python
class GameBuilder:
    def set_board_size(self, size: int) -> 'GameBuilder'
    def add_player(self, player: Player) -> 'GameBuilder'
    def add_winning_strategies(self, strategies: List[WinningStrategy]) -> 'GameBuilder'
    def build(self) -> Game:  # Validates before returning
        self.validator.validate(self.game)
        return self.game

# Optional: Director for common configurations
class GameDirector:
    def create_human_vs_bot(self, user: User, difficulty: Level) -> Game
    def create_two_player(self, user1: User, user2: User) -> Game
```

**Validation Rules:**
- Board size: 3-10
- Exactly 2 players (for standard Tic-Tac-Toe)
- Unique symbols per player
- At most 1 bot player
- Bot must have playing strategy
- At least one winning strategy

---

### 4. Models with Mixed Responsibilities

**Problem:** `Player.play()` contains I/O logic (input() in HumanPlayer:17-21). Models should be pure data/domain logic.

**Solution:** Extract I/O to separate handlers:
```python
# Pure model - no I/O
@dataclass
class Player(ABC):
    symbol: Symbol
    # No play() method!

# Separate input handling
class InputHandler:
    def get_move(self, game: Game) -> Tuple[int, int]

class ConsoleInputHandler(InputHandler):
    def get_move(self, game: Game) -> Tuple[int, int]:
        # Handle input/validation here
```

**GameService orchestrates:**
```python
if isinstance(player, HumanPlayer):
    row, col = input_handler.get_move(game)
else:
    row, col = player.strategy.get_move(game.board, player.symbol)
```

---

## IMPORTANT ISSUES (High Interview Value)

### 5. Missing GameStatus Enum & Move Model

**Problem:** No explicit game state tracking. Move history not captured - can't implement undo/replay.

**Solution:**
```python
class GameStatus(Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    WIN = "WIN"
    DRAW = "DRAW"
    ABANDONED = "ABANDONED"

@dataclass
class Move:
    player: Player
    cell: Cell
    timestamp: datetime
    move_number: int
```

**Benefits:** Enables undo (pop from moves stack), replay, game persistence, analytics.

---

### 6. Board Has Display Logic (SRP Violation)

**Problem:** `Board.print()` at line 27-31 mixes domain logic with presentation.

**Solution:** Separate display responsibility:
```python
class BoardDisplay(ABC):
    @abstractmethod
    def display(self, board: Board) -> None

class ConsoleDisplay(BoardDisplay):
    def display(self, board: Board) -> None:
        # Print logic here
```

**Why:** Enables different displays (GUI, web, ASCII art) without changing Board model.

---

### 7. Inefficient Winning Strategy

**Problem:** Strategies scan entire board O(n²) after EVERY move (game_controller.py:35-38).

**Solution:** Optimize with state tracking:
```python
class OptimizedRowWinningStrategy(WinningStrategy):
    def __init__(self):
        self.row_counts: Dict[int, Dict[Symbol, int]] = {}

    def update(self, move: Move) -> None:
        # O(1) update counts

    def has_won(self, board: Board, symbol: Symbol) -> bool:
        # O(1) check using counts
```

**Interview Gold:** Shows understanding of time complexity optimization. Mention during discussion.

---

### 8. Missing Factory Pattern for Strategies

**Problem:** Strategies instantiated directly in main.py:9-12, 20, 22. Tight coupling.

**Solution:**
```python
class StrategyFactory:
    @staticmethod
    def create_winning_strategies(board_size: int) -> List[WinningStrategy]:
        return [
            RowWinningStrategy(),
            ColWinningStrategy(),
            DiagonalWinningStrategy()
        ]

    @staticmethod
    def create_bot_strategy(level: Level) -> BotPlayingStrategy:
        strategies = {
            Level.EASY: EasyBotPlayingStrategy(),
            Level.MEDIUM: MediumBotPlayingStrategy(),
            Level.HARD: HardBotPlayingStrategy()
        }
        return strategies[level]
```

---

## GOOD-TO-HAVE IMPROVEMENTS

### 9. No Configuration Management

**Problem:** Magic numbers scattered (board size 3 in main.py:17, etc.).

**Solution:**
```python
class GameConfig:
    MIN_BOARD_SIZE: int = 3
    MAX_BOARD_SIZE: int = 10
    DEFAULT_BOARD_SIZE: int = 3
    MIN_PLAYERS: int = 2
    MAX_PLAYERS: int = 2
    MAX_BOTS: int = 1
```

---

### 10. Cell Mutability Issues

**Problem:** `Cell.symbol` is mutable (Cell.py:9). Can be accidentally modified.

**Solution:** Make Cell immutable or use property setter with validation:
```python
@dataclass(frozen=True)
class Cell:
    row: int
    column: int
    symbol: Optional[Symbol] = None
```

Or create new Cell on move instead of mutating.

---

### 11. Limited Exception Handling

**Problem:** Only `InvalidMoveError` exists. No hierarchy for different error types.

**Solution:**
```python
class GameException(Exception): pass
class InvalidMoveError(GameException): pass
class GameNotStartedError(GameException): pass
class GameAlreadyOverError(GameException): pass
class InvalidPlayerError(GameException): pass
class InvalidBoardSizeError(GameException): pass
```

---

### 12. Missing Undo/Replay (Common Interview Extension)

**Problem:** No move history, can't implement undo.

**Solution:** With Move model + history:
```python
class GameService:
    def undo_move(self, game: Game) -> bool:
        if not game.moves:
            return False
        last_move = game.moves.pop()
        game.board.cells[last_move.cell.row][last_move.cell.column].symbol = None
        game.current_player_index = (game.current_player_index - 1) % len(game.players)
        return True

    def replay_game(self, game: Game) -> None:
        # Replay all moves for demonstration
```

**Interview Tip:** Mention this as an extension even if not implementing.

---

## ARCHITECTURE IMPROVEMENTS

### 13. Dependency Injection

**Problem:** Tight coupling, hard to test. Direct instantiation everywhere.

**Solution:** Inject dependencies:
```python
class GameController:
    def __init__(
        self,
        game_service: GameService,
        display_service: DisplayService,
        input_handler: InputHandler
    ):
        self.game_service = game_service
        self.display = display_service
        self.input_handler = input_handler
```

---

### 14. Empty Services/Repositories Folders

**Problem:** Folders exist but unused - shows incomplete architecture understanding.

**Solution:** Either use them or remove them. If using:
- `services/game_service.py` - Business logic
- `repositories/` - If adding persistence (save/load games)

---

## SOLID PRINCIPLES SUMMARY

| Principle | Current Violation | Solution |
|-----------|-------------------|----------|
| **SRP** | GameController (logic+I/O+orchestration), Board.print(), Player.play() | GameService, DisplayService, InputHandler |
| **OCP** | Adding new player types requires changes in multiple places | Strategy pattern (already good), Factory pattern |
| **LSP** | Player subclasses change behavior significantly | Acceptable for this domain |
| **ISP** | No violations - interfaces are focused | ✓ Good |
| **DIP** | Depends on concrete classes | Inject abstractions, use factories |

---

## PRIORITY FOR LLD INTERVIEWS

### ⭐ MUST MENTION/IMPLEMENT (10-15 min discussion)
1. **Game Model** - Separate state from controller
2. **GameService** - Business logic layer
3. **GameBuilder** - Complex object construction
4. **Move Model + GameStatus** - State tracking

### ⭐ GOOD TO MENTION (5 min discussion)
5. **DisplayService** - Separate presentation
6. **InputHandler** - Separate I/O
7. **Strategy Optimization** - Time complexity improvement
8. **Factory Pattern** - Strategy creation

### ⭐ BONUS (If time permits or asked)
9. **Undo/Replay** - Move history usage
10. **Exception Hierarchy** - Proper error handling
11. **DI Container** - Testability

---

## UPDATED CLASS DIAGRAM

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                              │
│  - Creates GameBuilder/Director                              │
│  - Initializes GameController with DI                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
        ┌───────────────────────┐
        │   GameController      │
        │  (Orchestration only) │
        └──────┬────────────────┘
               │
      ┌────────┴────────┐
      ▼                 ▼
┌──────────────┐  ┌──────────────┐
│ GameService  │  │DisplayService│
│ (Logic)      │  │ (UI)         │
└──┬───────────┘  └──────────────┘
   │
   │ operates on
   ▼
┌────────────────────────────────┐
│          Game (Model)          │
│ ├─ board: Board                │
│ ├─ players: List[Player]       │
│ ├─ moves: List[Move]           │
│ ├─ status: GameStatus          │
│ ├─ winning_strategies: List    │
│ └─ current_player_index: int   │
└────┬───────────────────────────┘
     │
     ├──► Board ──► Cell
     │
     ├──► Player (ABC)
     │      ├─ HumanPlayer
     │      └─ BotPlayer
     │
     ├──► Move
     │      ├─ player: Player
     │      ├─ cell: Cell
     │      └─ timestamp
     │
     └──► WinningStrategy (ABC)
            ├─ RowWinningStrategy
            ├─ ColWinningStrategy
            └─ DiagonalWinningStrategy

┌─────────────────────────┐
│   GameBuilder           │
│  (Creational Pattern)   │
├─────────────────────────┤
│ + set_board_size()      │
│ + add_player()          │
│ + add_strategies()      │
│ + build() -> Game       │
└────────┬────────────────┘
         │ uses
         ▼
    ┌──────────────┐
    │GameValidator │
    └──────────────┘

Optional:
┌──────────────────┐       ┌───────────────────┐
│  GameDirector    │       │ StrategyFactory   │
│ (Preset configs) │       │ (Create strategies│
└──────────────────┘       └───────────────────┘

Supporting:
┌─────────────────┐  ┌──────────────────┐  ┌────────────┐
│ InputHandler    │  │ BotPlayingStrategy│  │ GameStatus │
│ (I/O logic)     │  │ (Bot moves)       │  │ (Enum)     │
└─────────────────┘  └──────────────────┘  └────────────┘
```

---

## KEY INTERVIEW TALKING POINTS

1. **"I see the controller has mixed responsibilities..."** → Suggest GameService separation
2. **"How would you add undo functionality?"** → Move model + history stack
3. **"This checks the entire board each time..."** → Optimize with hashmaps
4. **"How do you ensure valid game creation?"** → Builder pattern with validation
5. **"What if we want a web UI?"** → DisplayService abstraction
6. **"How would you test this?"** → DI enables mocking
7. **"Can we support NxN boards?"** → Already supported, mention config validation
8. **"What about replay or save/load?"** → Move history + serialization

**Remember:** Don't over-engineer. Focus on demonstrating understanding of:
- SOLID principles
- Design patterns (Strategy, Builder, Factory)
- Clean architecture (layers: Controller → Service → Model)
- Time/space complexity awareness

---
