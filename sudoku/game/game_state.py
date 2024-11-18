"""
Game state management module.
Handles the current state of the Sudoku game.
"""

from typing import List, Set, Tuple, Optional

class GameState:
    """Manages the current state of the game."""
    
    def __init__(self):
        """Initialize game state."""
        self._current_board = [[0] * 9 for _ in range(9)]
        self._solution = [[0] * 9 for _ in range(9)]
        self.original_cells = set()
        self.selected_cell = None
        self.current_difficulty = 'easy'
        self.current_level = 1
        self.move_history = []
        self.hints_remaining = 3

    def initialize_board(self, puzzle: list, solution: list) -> None:
        """
        Initialize board with new puzzle.

        Args:
            puzzle: Initial puzzle state
            solution: Complete solution
        """
        self._current_board = [row[:] for row in puzzle]
        self._solution = [row[:] for row in solution]
        self.original_cells = {
            (i, j) for i in range(9) for j in range(9)
            if puzzle[i][j] != 0
        }
        self.selected_cell = None
        self.move_history = []
        self.hints_remaining = 3

    @property
    def current_board(self) -> list:
        """Get current board state."""
        return self._current_board

    @property
    def solution(self) -> list:
        """Get solution board state."""
        return self._solution

    def set_cell_value(self, row: int, col: int, value: int) -> None:
        """
        Set cell value and store in move history.
        
        Args:
            row: Cell row
            col: Cell column
            value: New value
        """
        prev_value = self._current_board[row][col]
        if value != prev_value:
            self.move_history.append((row, col, prev_value))
        self._current_board[row][col] = value

    def is_cell_modifiable(self, row: int, col: int) -> bool:
        """
        Check if cell can be modified.
        
        Args:
            row: Cell row
            col: Cell column
            
        Returns:
            bool: True if cell can be modified
        """
        return (row, col) not in self.original_cells

    def check_complete(self) -> bool:
        """
        Check if puzzle is complete and correct.
        
        Returns:
            bool: True if puzzle is complete and correct
        """
        return (
            all(all(cell != 0 for cell in row) for row in self._current_board) and
            self._current_board == self._solution
        )

    def get_cell_value(self, row: int, col: int) -> int:
        """
        Get the value of a cell.

        Args:
            row (int): Row index
            col (int): Column index

        Returns:
            int: Cell value
        """
        return self._current_board[row][col]

    def is_original_cell(self, row: int, col: int) -> bool:
        """
        Check if a cell is part of the original puzzle.

        Args:
            row (int): Row index
            col (int): Column index

        Returns:
            bool: True if cell is original, False otherwise
        """
        return (row, col) in self.original_cells

    def is_cell_valid(self, row: int, col: int) -> bool:
        """
        Check if a cell's current value is valid.

        Args:
            row (int): Row index
            col (int): Column index

        Returns:
            bool: True if cell value is valid, False otherwise
        """
        value = self._current_board[row][col]
        if value == 0:
            return True

        # Check row
        for j in range(9):
            if j != col and self._current_board[row][j] == value:
                return False

        # Check column
        for i in range(9):
            if i != row and self._current_board[i][col] == value:
                return False

        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if (i != row or j != col) and self._current_board[i][j] == value:
                    return False

        return True

    def is_complete(self) -> bool:
        """
        Check if the puzzle is complete and correct.

        Returns:
            bool: True if puzzle is complete and correct, False otherwise
        """
        # Check if all cells are filled
        if any(0 in row for row in self._current_board):
            return False

        # Check if all cells match the solution
        return all(
            self._current_board[i][j] == self._solution[i][j]
            for i in range(9)
            for j in range(9)
        )

    def is_cell_modifiable(self, row: int, col: int) -> bool:
        """
        Check if a cell can be modified.

        Args:
            row (int): Row index
            col (int): Column index

        Returns:
            bool: True if cell can be modified, False otherwise
        """
        return (row, col) not in self.original_cells

    def check_complete(self) -> bool:
        """
        Check if the puzzle is complete and correct.

        Returns:
            bool: True if the puzzle is complete and correct, False otherwise
        """
        # Check for empty cells
        if any(0 in row for row in self._current_board):
            return False

        # Check each row
        for row in self._current_board:
            if set(row) != set(range(1, 10)):
                return False

        # Check each column
        for col in range(9):
            column = [self._current_board[row][col] for row in range(9)]
            if set(column) != set(range(1, 10)):
                return False

        # Check each 3x3 box
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = []
                for i in range(3):
                    for j in range(3):
                        box.append(self._current_board[box_row + i][box_col + j])
                if set(box) != set(range(1, 10)):
                    return False

        return True 