# Category Guide: Board & Strategy Games

## Overview

Game-based LLD problems test your ability to model **rules, turns, and win conditions** in an object-oriented way. These are popular because they have clear boundaries and test inheritance, polymorphism, and state management.

---

## Common Entities

| Entity | Purpose | Example |
|--------|---------|---------|
| Game | Orchestrates gameplay | ChessGame, SnakeLadderGame |
| Board | Holds the playing surface | 8x8 grid, 100 cells |
| Player | Represents participants | HumanPlayer, ComputerPlayer |
| Piece/Token | Movable game elements | King, Queen, Pawn, Token |
| Move | Represents an action | from (2,3) to (4,5) |
| Dice/RandomGenerator | Introduces randomness | 1-6 dice roll |

---

## Key Design Patterns

### 1. Strategy Pattern - For Different Piece Movements
```
                    ┌─────────────────┐
                    │  MovementStrategy│ (ABC)
                    │  + canMove()    │
                    │  + getValidMoves()│
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ LinearMovement│   │DiagonalMovement│  │  LShapeMovement│
│   (Rook)      │   │   (Bishop)    │   │   (Knight)    │
└───────────────┘   └───────────────┘   └───────────────┘
```

### 2. Template Method - For Game Loop
```
class Game:
    def play(self):           # Template method
        self.initialize()
        while not self.is_game_over():
            player = self.get_current_player()
            move = player.get_move()
            if self.is_valid_move(move):
                self.execute_move(move)
                self.switch_turn()
        self.declare_winner()
```

### 3. Factory Pattern - For Piece Creation
```
class PieceFactory:
    def create_piece(type, color):
        if type == "KING": return King(color)
        if type == "QUEEN": return Queen(color)
        ...
```

---

## Class Design Tips

### Piece Hierarchy (Chess-like games)
```
         ┌────────────┐
         │   Piece    │ (ABC)
         │ - color    │
         │ - position │
         │ + canMove()│
         └─────┬──────┘
               │
    ┌──────────┼──────────┬──────────┐
    ▼          ▼          ▼          ▼
  King      Queen       Rook      Pawn
```

**Why ABC for Piece?**
- Each piece has different movement rules
- `canMove()` must be implemented by each subclass
- Common attributes (color, position) in base class

### Board Representation

**Option 1: 2D Array (Simple)**
```
board = [[Cell() for _ in range(8)] for _ in range(8)]
piece = board[row][col].piece
```

**Option 2: Dictionary (Sparse)**
```
pieces = {(0,0): Rook(), (0,1): Knight(), ...}
```

**When to use which?**
- Dense boards (Chess, Sudoku) → 2D Array
- Sparse boards (Battleship) → Dictionary

---

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| God class Game | Game class does everything | Extract Board, MoveValidator, TurnManager |
| Hardcoded rules | Move validation in Piece class | Use Strategy pattern for movements |
| No move history | Can't implement undo | Store List[Move] in Game |
| Missing validation | Invalid moves accepted | Separate MoveValidator class |
| Tight coupling | Board knows about specific pieces | Use Piece interface |

---

## Coding Hacks for Demo

### 1. Enum for Directions
```python
class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    DIAGONAL_UP_LEFT = (-1, -1)
    # ... etc
```

### 2. Quick Move Validation
```python
def is_within_bounds(row, col, size=8):
    return 0 <= row < size and 0 <= col < size
```

### 3. Delta-based Movement
```python
# Knight moves as deltas
KNIGHT_DELTAS = [(-2,-1), (-2,1), (-1,-2), (-1,2),
                 (1,-2), (1,2), (2,-1), (2,1)]

def get_knight_moves(pos):
    return [(pos[0]+dr, pos[1]+dc) for dr, dc in KNIGHT_DELTAS
            if is_within_bounds(pos[0]+dr, pos[1]+dc)]
```

### 4. Simple Game Loop
```python
def play(self):
    while self.status == GameStatus.IN_PROGRESS:
        move = self.current_player.get_move(self.board)
        if self.board.is_valid_move(move, self.current_player):
            self.board.execute_move(move)
            self.check_game_over()
            self.switch_turn()
```

---

## API Design

### Core Endpoints
```
POST   /games                    # Create new game
GET    /games/{id}               # Get game state
POST   /games/{id}/moves         # Make a move
GET    /games/{id}/moves         # Get move history
POST   /games/{id}/resign        # Player resigns
```

### Move Request
```json
POST /games/{id}/moves
{
    "player_id": "player-1",
    "from": {"row": 1, "col": 0},
    "to": {"row": 3, "col": 0}
}
```

### Game State Response
```json
{
    "id": "game-123",
    "status": "IN_PROGRESS",
    "current_turn": "WHITE",
    "board": [...],
    "captured_pieces": {"WHITE": [], "BLACK": ["PAWN"]},
    "move_count": 5
}
```

---

## Interview Questions to Expect

1. "How would you add an **undo** feature?"
   → Store moves in a stack, implement reverse of each move

2. "How would you add a **timer** for each player?"
   → Add `remaining_time` to Player, decrement on their turn

3. "How would you support **multiplayer online**?"
   → Game state in DB, WebSocket for real-time updates

4. "How would you add **AI opponent**?"
   → Create `ComputerPlayer` implementing Player interface, use Strategy for difficulty levels

---

## Checklist Before Interview

- [ ] Can explain Piece hierarchy with ABC
- [ ] Can draw Board + Cell relationship
- [ ] Know Game loop structure
- [ ] Can handle turn switching
- [ ] Know how to validate moves
- [ ] Can explain win/draw conditions
- [ ] Have Strategy pattern example ready
