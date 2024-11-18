"""
Helper functions module for the Sudoku game.
Provides various utility functions used throughout the game.
"""

from typing import List, Tuple
import time

def format_time(seconds: int) -> str:
    """
    Format seconds into MM:SS string.

    Args:
        seconds (int): Number of seconds

    Returns:
        str: Formatted time string
    """
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def get_box_coordinates(row: int, col: int) -> Tuple[int, int]:
    """
    Get the top-left coordinates of the 3x3 box containing the given cell.

    Args:
        row (int): Row index
        col (int): Column index

    Returns:
        Tuple[int, int]: Box top-left coordinates
    """
    return (row // 3) * 3, (col // 3) * 3

def get_related_cells(row: int, col: int) -> List[Tuple[int, int]]:
    """
    Get all cells related to the given cell (same row, column, or box).

    Args:
        row (int): Row index
        col (int): Column index

    Returns:
        List[Tuple[int, int]]: List of related cell coordinates
    """
    related = set()
    
    # Add cells in same row
    for j in range(9):
        if j != col:
            related.add((row, j))
    
    # Add cells in same column
    for i in range(9):
        if i != row:
            related.add((i, col))
    
    # Add cells in same box
    box_row, box_col = get_box_coordinates(row, col)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if (i != row or j != col):
                related.add((i, j))
    
    return list(related)

def calculate_score(time_taken: int, difficulty: str, hints_used: int) -> int:
    """
    Calculate game score based on time taken, difficulty, and hints used.

    Args:
        time_taken (int): Time taken in seconds
        difficulty (str): Game difficulty
        hints_used (int): Number of hints used

    Returns:
        int: Calculated score
    """
    # Base score
    base_score = 1000
    
    # Difficulty multipliers
    difficulty_multipliers = {
        'easy': 1.0,
        'medium': 1.5,
        'hard': 2.0,
        'expert': 3.0
    }
    
    # Calculate penalties
    time_penalty = time_taken  # 1 point per second
    hint_penalty = hints_used * 100  # 100 points per hint
    
    # Calculate final score
    multiplier = difficulty_multipliers.get(difficulty, 1.0)
    final_score = (base_score - time_penalty - hint_penalty) * multiplier
    
    return max(0, int(final_score))

class PerformanceTimer:
    """Simple context manager for timing code execution."""
    
    def __init__(self, description: str = "Operation"):
        """
        Initialize timer.

        Args:
            description (str): Description of the operation being timed
        """
        self.description = description
        self.start_time = None

    def __enter__(self) -> 'PerformanceTimer':
        """Start timing."""
        self.start_time = time.time()
        return self

    def __exit__(self, *args) -> None:
        """End timing and print result."""
        duration = time.time() - self.start_time
        print(f"{self.description} took {duration:.3f} seconds")
