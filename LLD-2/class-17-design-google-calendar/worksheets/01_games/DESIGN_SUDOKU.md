# Design Sudoku

- [Design Sudoku](#design-sudoku)
  - [Overview](#overview)
  - [Expectations](#expectations)
  - [Requirements Gathering](#requirements-gathering)
  - [Requirements](#requirements)
  - [Use Case Diagrams](#use-case-diagrams)
  - [Class Diagram](#class-diagram)
  - [Key Design Decisions](#key-design-decisions)
  - [API Design](#api-design)

---

## Overview

Sudoku is a logic-based puzzle game played on a 9x9 grid. The grid is divided into 9 smaller 3x3 boxes. The objective is to fill the grid so that each row, column, and 3x3 box contains digits 1-9 without repetition.

```
┌───────┬───────┬───────┐
│ 5 3 . │ . 7 . │ . . . │
│ 6 . . │ 1 9 5 │ . . . │
│ . 9 8 │ . . . │ . 6 . │
├───────┼───────┼───────┤
│ 8 . . │ . 6 . │ . . 3 │
│ 4 . . │ 8 . 3 │ . . 1 │
│ 7 . . │ . 2 . │ . . 6 │
├───────┼───────┼───────┤
│ . 6 . │ . . . │ 2 8 . │
│ . . . │ 4 1 9 │ . . 5 │
│ . . . │ . 8 . │ . 7 9 │
└───────┴───────┴───────┘
```

**Rules:**
- 9x9 grid divided into 9 boxes of 3x3
- Some cells are pre-filled (given)
- Fill remaining cells with digits 1-9
- Each row must contain 1-9 (no repeats)
- Each column must contain 1-9 (no repeats)
- Each 3x3 box must contain 1-9 (no repeats)

---

## Expectations

* Code should be functionally correct.
* Code should be modular and readable. Clean and professional level code.
* Code should be extensible and scalable. Means it should be able to accommodate new requirements with minimal changes.
* Code should have good OOP design principles.

---

## Requirements Gathering

What are some questions you would ask to gather requirements?

```
1.
2.
3.
4.
5.
```

<details>
<summary><strong>Sample clarifying questions</strong></summary>

1. Do we need to generate puzzles or just solve/validate?
2. Should we support different difficulty levels?
3. Can users get hints?
4. Should we track time taken?
5. Can users undo moves?
6. Should we highlight invalid entries?
7. Do we support partial board validation?

</details>

---

## Requirements

What will be 6-8 requirements of the system, according to you?

```
1.
2.
3.
4.
5.
6.
```

<details>
<summary><strong>Click to see the actual requirements</strong></summary>

1. Display a 9x9 Sudoku board with pre-filled numbers.
2. User can input a number (1-9) into an empty cell.
3. System validates if the move is valid (no conflict).
4. System detects when puzzle is complete and correct.
5. User can clear a cell they filled (not given cells).
6. System can provide hints (optional).
7. Track and display time taken.
8. Support undo functionality.

</details>

---

## Use Case Diagrams

### Actors

What would be the actors in this system?

```
1.
```

### Use Cases

#### Actor 1

Name of the actor - ` `

Use cases:
```
1.
2.
3.
4.
5.
```

---

## Class Diagram

What will be the major classes and their attributes?

**Think about:**
- What represents the board?
- What represents a cell?
- How to validate moves?
- How to check win condition?

List down your classes:

```
Class 1:

Class 2:

Class 3:

Class 4:
```

**Design Question: Should Cell know its position?**
```
Your thoughts:

```

Draw the class diagram:

```




```

---

## Key Design Decisions

**1. How to validate a move efficiently?**
```
Hint: Track which numbers are used in each row/column/box

Your approach:

```

**2. How to implement hint feature?**
```
Your approach:

```

**3. How would you implement undo?**
```
Your approach:

```

---

## API Design

If this were a web-based Sudoku, what APIs would you need?

```
1.
2.
3.
4.
```

---

## Hints

<details>
<summary><strong>Hint 1: Cell Design</strong></summary>

```python
class Cell:
    value: Optional[int]  # 1-9 or None
    is_given: bool        # Pre-filled or user-filled
    row: int
    col: int
    box_index: int        # 0-8

    def set_value(self, val):
        if self.is_given:
            raise CannotModifyGivenCell()
        self.value = val
```

</details>

<details>
<summary><strong>Hint 2: Efficient Validation</strong></summary>

```python
class Board:
    def __init__(self):
        self.cells = [[Cell() for _ in range(9)] for _ in range(9)]
        # Track used numbers
        self.rows = [set() for _ in range(9)]    # rows[i] = numbers in row i
        self.cols = [set() for _ in range(9)]    # cols[j] = numbers in col j
        self.boxes = [set() for _ in range(9)]   # boxes[k] = numbers in box k

    def is_valid_move(self, row, col, num):
        box_idx = (row // 3) * 3 + (col // 3)
        return (num not in self.rows[row] and
                num not in self.cols[col] and
                num not in self.boxes[box_idx])

    def place_number(self, row, col, num):
        if not self.is_valid_move(row, col, num):
            raise InvalidMoveError()
        self.cells[row][col].value = num
        box_idx = (row // 3) * 3 + (col // 3)
        self.rows[row].add(num)
        self.cols[col].add(num)
        self.boxes[box_idx].add(num)
```

</details>

<details>
<summary><strong>Hint 3: Win Condition</strong></summary>

```python
def is_complete(self):
    for row in self.cells:
        for cell in row:
            if cell.value is None:
                return False
    return True  # All cells filled (validation ensures correctness)
```

</details>

<details>
<summary><strong>Hint 4: Undo with Command Pattern</strong></summary>

```python
class Move:
    row: int
    col: int
    old_value: Optional[int]
    new_value: Optional[int]

class Game:
    move_history: List[Move]

    def place_number(self, row, col, num):
        old_val = self.board.cells[row][col].value
        self.board.place_number(row, col, num)
        self.move_history.append(Move(row, col, old_val, num))

    def undo(self):
        if not self.move_history:
            return
        move = self.move_history.pop()
        self.board.cells[move.row][move.col].value = move.old_value
        # Also update row/col/box sets
```

</details>
