"""
Sudoku validator module.
This module provides functionality to validate Sudoku board states and moves.
"""

from typing import List, Tuple, Set

class SudokuValidator:
    """
    Validates Sudoku board states and moves according to standard Sudoku rules.
    All validation methods are static as they don't require instance state.
    """

    @staticmethod
    def is_valid_move(board: List[List[int]], row: int, col: int, value: int) -> bool:
        """
        Check if placing a value at the specified position is valid.

        Args:
            board (List[List[int]]): Current board state
            row (int): Row index
            col (int): Column index
            value (int): Value to check (1-9)

        Returns:
            bool: True if the move is valid
        """
        return (SudokuValidator.is_valid_row(board, row, value, col) and
                SudokuValidator.is_valid_column(board, col, value, row) and
                SudokuValidator.is_valid_box(board, row, col, value))

    @staticmethod
    def is_valid_row(board: List[List[int]], row: int, value: int, 
                     exclude_col: int = -1) -> bool:
        """
        Check if a value is valid in the specified row.

        Args:
            board (List[List[int]]): Current board state
            row (int): Row index to check
            value (int): Value to check
            exclude_col (int): Column to exclude from check (optional)

        Returns:
            bool: True if the value is valid in the row
        """
        for col in range(9):
            if col != exclude_col and board[row][col] == value:
                return False
        return True

    @staticmethod
    def is_valid_column(board: List[List[int]], col: int, value: int, 
                        exclude_row: int = -1) -> bool:
        """
        Check if a value is valid in the specified column.

        Args:
            board (List[List[int]]): Current board state
            col (int): Column index to check
            value (int): Value to check
            exclude_row (int): Row to exclude from check (optional)

        Returns:
            bool: True if the value is valid in the column
        """
        for row in range(9):
            if row != exclude_row and board[row][col] == value:
                return False
        return True

    @staticmethod
    def is_valid_box(board: List[List[int]], row: int, col: int, 
                     value: int) -> bool:
        """
        Check if a value is valid in the 3x3 box containing the specified position.

        Args:
            board (List[List[int]]): Current board state
            row (int): Row index
            col (int): Column index
            value (int): Value to check

        Returns:
            bool: True if the value is valid in the 3x3 box
        """
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if (i != row or j != col) and board[i][j] == value:
                    return False
        return True

    @staticmethod
    def is_complete(board: List[List[int]]) -> bool:
        """
        Check if the board is completely and correctly filled.

        Args:
            board (List[List[int]]): Board to check

        Returns:
            bool: True if the board is complete and valid
        """
        # Check for empty cells
        if any(0 in row for row in board):
            return False

        # Check all rows, columns and boxes
        return (SudokuValidator._check_all_rows(board) and
                SudokuValidator._check_all_columns(board) and
                SudokuValidator._check_all_boxes(board))

    @staticmethod
    def _check_all_rows(board: List[List[int]]) -> bool:
        """
        Validate all rows in the board.

        Args:
            board (List[List[int]]): Board to check

        Returns:
            bool: True if all rows are valid
        """
        return all(SudokuValidator._is_valid_set(row) for row in board)

    @staticmethod
    def _check_all_columns(board: List[List[int]]) -> bool:
        """
        Validate all columns in the board.

        Args:
            board (List[List[int]]): Board to check

        Returns:
            bool: True if all columns are valid
        """
        return all(
            SudokuValidator._is_valid_set([board[row][col] for row in range(9)])
            for col in range(9)
        )

    @staticmethod
    def _check_all_boxes(board: List[List[int]]) -> bool:
        """
        Validate all 3x3 boxes in the board.

        Args:
            board (List[List[int]]): Board to check

        Returns:
            bool: True if all boxes are valid
        """
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = []
                for i in range(box_row, box_row + 3):
                    for j in range(box_col, box_col + 3):
                        box.append(board[i][j])
                if not SudokuValidator._is_valid_set(box):
                    return False
        return True

    @staticmethod
    def _is_valid_set(numbers: List[int]) -> bool:
        """
        Check if a set of numbers contains all digits 1-9 exactly once.

        Args:
            numbers (List[int]): List of numbers to check

        Returns:
            bool: True if the set is valid
        """
        return set(numbers) == set(range(1, 10))
