# Tic-Tac-Toe: Winning Strategy Optimization

This document explains how we can optimize the process of checking for a winner in a Tic-Tac-Toe game. We'll start with a naive approach and gradually improve it to a highly optimized O(1) solution.

## The Evolution of Winning Strategies

### 1. The Naive Approach: O(n^2)

After every move, we can check the entire board to see if there's a winner. For a board of size `n x n`, this involves:

- Iterating through all `n` rows to check for a row-win.
- Iterating through all `n` columns to check for a column-win.
- Checking both diagonals for a win.

The time complexity of this approach is **O(n^2)** because in the worst case, we have to scan the entire board.

```python
# Pseudocode for O(n^2) check
def check_winner_n2(board, n):
    # Check rows
    for row in range(n):
        if all_same(board[row]):
            return True

    # Check columns
    for col in range(n):
        if all_same([board[row][col] for row in range(n)]):
            return True

    # Check diagonals
    if all_same([board[i][i] for i in range(n)]) or \
       all_same([board[i][n-1-i] for i in range(n)]):
            return True

    return False
```

### 2. A Better Approach: O(n) - Focusing on the Current Player

We can make a simple but significant optimization. A player can only win on their own turn. Therefore, we only need to check if the player who just made a move has won. We don't need to check for the other player.

This doesn't change the worst-case time complexity, but it cuts the number of checks in half on average.

A more significant optimization comes from realizing that a win can only occur on the row, column, or diagonal that was just played on. So, after a move at `(row, col)`, we only need to check that specific row, column, and any relevant diagonals.

The time complexity of this approach is **O(n)** because we are only checking one row, one column, and at most two diagonals.

```python
# Pseudocode for O(n) check
def check_winner_n(board, n, row, col, player_symbol):
    # Check the row of the last move
    if all_same([board[row][c] for c in range(n)], player_symbol):
        return True

    # Check the column of the last move
    if all_same([board[r][col] for r in range(n)], player_symbol):
        return True

    # Check diagonals if the move was on a diagonal
    if row == col and all_same([board[i][i] for i in range(n)], player_symbol):
        return True
    if row + col == n - 1 and all_same([board[i][n-1-i] for i in range(n)], player_symbol):
        return True

    return False
```

### 3. The Optimal Approach: O(1) - Using Counters

The most efficient way to check for a winner is to avoid iterating over the board altogether. We can use counters to keep track of the state of the game.

We can maintain a count of symbols for each row, column, and diagonal.

- For each player, we'll have an array for row counts, an array for column counts, and variables for diagonal counts.
- When a player makes a move at `(row, col)`, we increment the corresponding counters for that player.
- If any of the counters for that player reaches `n`, that player has won.

This approach gives us a time complexity of **O(1)** for checking a winner, as it only involves a few arithmetic operations and comparisons.

```python
# Pseudocode for O(1) check

class TicTacToe:
    def __init__(self, n):
        self.n = n
        self.row_counts = {'X': [0]*n, 'O': [0]*n}
        self.col_counts = {'X': [0]*n, 'O': [0]*n}
        self.diag1_counts = {'X': 0, 'O': 0}
        self.diag2_counts = {'X': 0, 'O': 0}

    def make_move(self, row, col, player_symbol):
        self.row_counts[player_symbol][row] += 1
        self.col_counts[player_symbol][col] += 1
        if row == col:
            self.diag1_counts[player_symbol] += 1
        if row + col == self.n - 1:
            self.diag2_counts[player_symbol] += 1

        if self.row_counts[player_symbol][row] == self.n or \
           self.col_counts[player_symbol][col] == self.n or \
           self.diag1_counts[player_symbol] == self.n or \
           self.diag2_counts[player_symbol] == self.n:
            return f"Player {player_symbol} wins!"

        return "No winner yet"
```

## Conclusion

By using a simple counting mechanism, we can drastically reduce the time it takes to check for a winner in Tic-Tac-Toe, from O(n^2) to O(1). This makes the game more efficient, especially as the board size increases. The current implementation in this project uses the O(n) approach, which is a good balance between simplicity and performance for a standard 3x3 board. The O(1) approach is the most optimal and is recommended for larger boards or when performance is critical.
