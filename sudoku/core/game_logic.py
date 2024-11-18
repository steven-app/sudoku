"""
Core game logic for Sudoku.
Handles game rules validation and puzzle checking.
"""

from typing import List, Tuple, Optional

class GameLogic:
    """Handles core Sudoku game rules and validation."""
    
    @staticmethod
    def is_valid_move(board: List[List[int]], row: int, col: int, value: int) -> bool:
        """
        Check if placing a value at the given position is valid.
        
        Args:
            board: Current game board
            row: Row index
            col: Column index
            value: Value to check
            
        Returns:
            bool: True if the move is valid, False otherwise
        """
        # Check row
        for j in range(9):
            if j != col and board[row][j] == value:
                return False
                
        # Check column
        for i in range(9):
            if i != row and board[i][col] == value:
                return False
                
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if (i != row or j != col) and board[i][j] == value:
                    return False
                    
        return True

    @staticmethod
    def find_empty_cell(board: List[List[int]]) -> Optional[Tuple[int, int]]:
        """
        Find an empty cell in the board.
        
        Args:
            board: Current game board
            
        Returns:
            Optional[Tuple[int, int]]: Coordinates of empty cell or None if board is full
        """
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    @staticmethod
    def check_solution(board: List[List[int]], solution: List[List[int]]) -> bool:
        """
        Check if the current board matches the solution.
        
        Args:
            board: Current game board
            solution: Solution board
            
        Returns:
            bool: True if boards match, False otherwise
        """
        for i in range(9):
            for j in range(9):
                if board[i][j] != solution[i][j]:
                    return False
        return True

    @staticmethod
    def get_conflicts(board: List[List[int]], row: int, col: int, value: int) -> List[Tuple[int, int]]:
        """
        Get list of cells that conflict with the given value at position.
        
        Args:
            board: Current game board
            row: Row index
            col: Column index
            value: Value to check
            
        Returns:
            List[Tuple[int, int]]: List of conflicting cell coordinates
        """
        conflicts = []
        
        # Check row
        for j in range(9):
            if j != col and board[row][j] == value:
                conflicts.append((row, j))
                
        # Check column
        for i in range(9):
            if i != row and board[i][col] == value:
                conflicts.append((i, col))
                
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if (i != row or j != col) and board[i][j] == value:
                    conflicts.append((i, j))
                    
        return conflicts
