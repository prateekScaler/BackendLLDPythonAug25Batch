# Hints: Snake & Ladder

## Hint 1: Actors

<details>
<summary>Click to reveal</summary>

**Actors:**
1. **Player** - Rolls dice, moves on board
2. **System/Game** - Manages turns, validates moves, declares winner

</details>

---

## Hint 2: Key Classes

<details>
<summary>Click to reveal</summary>

```
Game
Board
Player
Dice
BoardEntity (ABC) → Snake, Ladder
Cell (optional)
```

</details>

---

## Hint 3: Snake & Ladder - Same or Different?

<details>
<summary>Click to reveal</summary>

**Approach: Use Abstract Base Class**

Both Snake and Ladder:
- Have a start position
- Have an end position
- Move player from start to end

Only difference: Snake moves down (end < start), Ladder moves up (end > start)

```
BoardEntity (ABC)
├── start: int
├── end: int
└── getNextPosition(): int

Snake extends BoardEntity
Ladder extends BoardEntity
```

Or even simpler - single class with just `start` and `end`:
- If `end > start` → acts like ladder
- If `end < start` → acts like snake

</details>

---

## Hint 4: Board Design

<details>
<summary>Click to reveal</summary>

**Option 1: Simple Dictionary**
```python
class Board:
    def __init__(self):
        self.size = 100
        self.jumps = {}  # position -> new_position

    def add_snake(self, head, tail):
        self.jumps[head] = tail

    def add_ladder(self, bottom, top):
        self.jumps[bottom] = top

    def get_final_position(self, position):
        return self.jumps.get(position, position)
```

**Option 2: Cell-based**
```python
class Cell:
    def __init__(self, position):
        self.position = position
        self.jump_to = None  # Snake or Ladder destination
```

</details>

---

## Hint 5: Dice Design

<details>
<summary>Click to reveal</summary>

**Basic Dice:**
```python
class Dice:
    def __init__(self, faces=6):
        self.faces = faces

    def roll(self):
        return random.randint(1, self.faces)
```

**For Extensibility (Strategy Pattern):**
```python
class DiceStrategy(ABC):
    def roll(self) -> int: pass

class FairDice(DiceStrategy):
    def roll(self):
        return random.randint(1, 6)

class WeightedDice(DiceStrategy):
    def roll(self):
        # Higher probability for 6
        ...

class MultipleDice(DiceStrategy):
    def __init__(self, count=2):
        self.count = count

    def roll(self):
        return sum(random.randint(1,6) for _ in range(self.count))
```

</details>

---

## Hint 6: Game Flow

<details>
<summary>Click to reveal</summary>

```python
class Game:
    def __init__(self, players, board, dice):
        self.players = players
        self.board = board
        self.dice = dice
        self.current_player_index = 0
        self.winner = None

    def play(self):
        while not self.winner:
            player = self.players[self.current_player_index]
            self.play_turn(player)
            self.switch_turn()

    def play_turn(self, player):
        dice_value = self.dice.roll()
        new_position = player.position + dice_value

        if new_position > 100:
            return  # Stay in place

        if new_position == 100:
            player.position = 100
            self.winner = player
            return

        # Check for snake/ladder
        final_position = self.board.get_final_position(new_position)
        player.position = final_position

    def switch_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
```

</details>

---

## Hint 7: Class Diagram

<details>
<summary>Click to reveal</summary>

```
┌─────────────────────┐
│        Game         │
├─────────────────────┤
│ - board: Board      │
│ - players[]         │
│ - dice: Dice        │
│ - current_turn: int │
│ - winner: Player    │
│ - status: GameStatus│
├─────────────────────┤
│ + play()            │
│ + playTurn()        │
│ + switchTurn()      │
│ + isGameOver()      │
└─────────────────────┘
         │
    ┌────┴────┬─────────────┐
    ▼         ▼             ▼
┌────────┐ ┌────────┐ ┌──────────────┐
│ Board  │ │ Player │ │    Dice      │
├────────┤ ├────────┤ ├──────────────┤
│- size  │ │- id    │ │- faces: int  │
│- jumps │ │- name  │ ├──────────────┤
├────────┤ │-position│ │+ roll(): int │
│+getFinal│└────────┘ └──────────────┘
│Position│
└────────┘

jumps: Dict[int, int]
  97 → 14 (snake)
  4 → 56  (ladder)
```

</details>

---

## Hint 8: Replay Feature

<details>
<summary>Click to reveal</summary>

Store each move:
```python
class Move:
    player_id: str
    dice_value: int
    from_position: int
    to_position: int  # After snake/ladder
    timestamp: datetime

class Game:
    def __init__(self):
        self.move_history: List[Move] = []

    def play_turn(self, player):
        dice_value = self.dice.roll()
        from_pos = player.position
        # ... calculate new position ...
        self.move_history.append(Move(
            player.id, dice_value, from_pos, player.position
        ))
```

Replay by iterating through `move_history`.

</details>

---

## Hint 9: API Design

<details>
<summary>Click to reveal</summary>

```
POST   /games                    # Create new game
       Request: {player_names: ["A", "B"]}
       Response: {game_id, board, players}

GET    /games/{id}               # Get game state

POST   /games/{id}/roll          # Roll dice for current player
       Response: {dice_value, player, from, to, winner?}

GET    /games/{id}/moves         # Get move history
```

</details>

---

## Common Mistakes to Avoid

1. **Hardcoding board size** - Make it configurable
2. **Not handling > 100** - Player should stay if roll exceeds 100
3. **Snake/Ladder at same position** - Validate during setup
4. **No win check** - Remember to check after each move
5. **Forgetting chain jumps** - Snake tail on another snake head (edge case)
