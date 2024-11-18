"""
Sudoku puzzle generator module.
This module handles the generation of valid Sudoku puzzles with varying difficulties.
"""

import random
import time
from typing import List, Tuple, Optional, Set

class SudokuGenerator:
    """
    Generates Sudoku puzzles with varying difficulties.
    Uses backtracking algorithm for puzzle generation and solution validation.
    """

    def __init__(self):
        """Initialize the generator with difficulty settings."""
        # Reset the board to empty state
        self.reset_board()
        # Counter for tracking number of solutions
        self.solutions_count = 0
        # Difficulty ratios (percentage of cells to remain filled)
        self.difficulty_ratios = {
            'easy': 0.6,      # 60% cells filled
            'medium': 0.5,    # 50% cells filled
            'hard': 0.4,      # 40% cells filled
            'expert': 0.3     # 30% cells filled
        }
        # 预计算每个位置的候选数字
        self.candidates = {(i, j): set(range(1, 10)) for i in range(9) for j in range(9)}
        self.attempts = 0
        self.start_time = 0

    def reset_board(self) -> None:
        """Reset the board to an empty state."""
        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def generate_puzzle(self, difficulty: str) -> Tuple[List[List[int]], List[List[int]]]:
        """
        Generate a new Sudoku puzzle with the specified difficulty.

        Args:
            difficulty (str): Difficulty level ('easy', 'medium', 'hard', 'expert')

        Returns:
            tuple: (puzzle, solution) where both are 9x9 lists of integers
        """
        print(f"\n=== Generating {difficulty.upper()} Puzzle ===")
        self.start_time = time.time()
        
        # Generate solution
        print("Generating complete solution...")
        solution = self.generate_solution()
        if not solution:
            print("Failed to generate solution!")
            raise RuntimeError("Failed to generate valid solution")
        
        solution_time = time.time() - self.start_time
        print(f"Solution generated in {solution_time:.2f} seconds")

        # Create puzzle
        print(f"\nCreating puzzle with {difficulty} difficulty...")
        fill_ratio = self.difficulty_ratios.get(difficulty, 0.5)
        print(f"Target fill ratio: {fill_ratio}")
        
        puzzle = self.generate_puzzle_from_solution(solution, fill_ratio)
        
        total_time = time.time() - self.start_time
        print(f"\nTotal generation time: {total_time:.2f} seconds")
        
        return puzzle, solution

    def generate_solution(self) -> List[List[int]]:
        """
        Generate a complete valid Sudoku solution.

        Returns:
            List[List[int]]: Complete Sudoku solution
        """
        print("\n=== Starting Solution Generation ===")
        self.start_time = time.time()
        self.attempts = 0
        self.reset_board()
        
        # Fill diagonal boxes first
        print("Filling diagonal boxes...")
        for i in range(0, 9, 3):
            self._fill_box(i, i)
            
        print("Starting recursive solve...")
        if self._solve_recursive(self.board):
            elapsed = time.time() - self.start_time
            print(f"Solution found in {elapsed:.2f} seconds after {self.attempts} attempts")
            return [row[:] for row in self.board]
        print("Failed to generate solution!")
        return None

    def _fill_box(self, start_row: int, start_col: int) -> None:
        """Fill a 3x3 box with random numbers."""
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for i in range(3):
            for j in range(3):
                self.board[start_row + i][start_col + j] = numbers[i * 3 + j]
        print(f"Filled box at ({start_row}, {start_col})")

    def _solve_recursive(self, board: List[List[int]], depth: int = 0, max_attempts: int = 1000000) -> bool:
        """
        Recursively solve the Sudoku board using optimized backtracking.
        
        Args:
            board: Current board state
            depth: Current recursion depth
            max_attempts: Maximum number of attempts before giving up
        
        Returns:
            bool: True if solution found, False otherwise
        """
        self.attempts += 1
        if self.attempts >= max_attempts:
            print(f"Exceeded maximum attempts ({max_attempts})!")
            return False
            
        if self.attempts % 10000 == 0:
            elapsed = time.time() - self.start_time
            print(f"Attempts: {self.attempts}, Time: {elapsed:.2f}s, Depth: {depth}")
            
        cell = self._find_best_empty_cell(board)
        if not cell:
            return True
            
        row, col = cell
        candidates = self._get_candidates(board, row, col)
        
        if not candidates:
            if self.attempts % 1000 == 0:
                print(f"No candidates at ({row}, {col}), depth {depth}")
            return False
            
        candidates_list = list(candidates)
        random.shuffle(candidates_list)
        
        for num in candidates_list:
            board[row][col] = num
            if self._solve_recursive(board, depth + 1):
                return True
            board[row][col] = 0
            
        return False

    def _find_best_empty_cell(self, board: List[List[int]]) -> Optional[Tuple[int, int]]:
        """
        Find the empty cell with fewest possible candidates.
        
        Returns:
            Optional[Tuple[int, int]]: Coordinates of best cell to fill next
        """
        min_candidates = 10
        best_cell = None
        
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    candidates = len(self._get_candidates(board, i, j))
                    if candidates < min_candidates:
                        min_candidates = candidates
                        best_cell = (i, j)
                        if candidates == 1:  # Return immediately if only one candidate
                            return best_cell
        
        return best_cell

    def _get_candidates(self, board: List[List[int]], row: int, col: int) -> Set[int]:
        """
        Get valid candidates for a cell.
        
        Args:
            board: Current board state
            row: Row index
            col: Column index
            
        Returns:
            Set[int]: Set of valid numbers for this cell
        """
        used = set()
        
        # Check row
        used.update(board[row])
        
        # Check column
        used.update(board[i][col] for i in range(9))
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                used.add(board[i][j])
        
        return set(range(1, 10)) - used

    def generate_puzzle_from_solution(self, solution: List[List[int]], fill_ratio: float) -> List[List[int]]:
        """Create puzzle by removing numbers while ensuring unique solution."""
        print("\n=== Creating Puzzle from Solution ===")
        start_time = time.time()
        puzzle = [row[:] for row in solution]
        cells_to_empty = int(81 * (1 - fill_ratio))
        
        print(f"Target cells to remove: {cells_to_empty}")
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        removed = 0
        attempts = 0
        max_attempts = len(cells)
        
        for i, j in cells:
            attempts += 1
            if removed >= cells_to_empty:
                break
                
            if attempts % 10 == 0:
                elapsed = time.time() - start_time
                print(f"Progress: {removed}/{cells_to_empty} cells removed, "
                      f"Attempts: {attempts}/{max_attempts}, Time: {elapsed:.2f}s")
            
            # Try removing current position
            temp = puzzle[i][j]
            puzzle[i][j] = 0
            
            # Check for unique solution
            if self._has_unique_solution(puzzle):
                removed += 1
                print(f"Removed cell ({i}, {j})")
                
                # Try symmetric position
                sym_i, sym_j = 8 - i, 8 - j
                if (sym_i, sym_j) != (i, j) and puzzle[sym_i][sym_j] != 0:
                    temp_sym = puzzle[sym_i][sym_j]
                    puzzle[sym_i][sym_j] = 0
                    if self._has_unique_solution(puzzle):
                        removed += 1
                        print(f"Removed symmetric cell ({sym_i}, {sym_j})")
                    else:
                        puzzle[sym_i][sym_j] = temp_sym
                        print(f"Restored symmetric cell ({sym_i}, {sym_j})")
            else:
                puzzle[i][j] = temp
                print(f"Restored cell ({i}, {j})")
                
        elapsed = time.time() - start_time
        print(f"\nPuzzle creation completed in {elapsed:.2f} seconds")
        print(f"Removed {removed} cells out of target {cells_to_empty}")
        
        return puzzle

    def _has_unique_solution(self, board: List[List[int]], max_solutions: int = 2) -> bool:
        """
        Check if the puzzle has exactly one solution.
        
        Args:
            board: Current board state
            max_solutions: Stop checking after finding this many solutions
            
        Returns:
            bool: True if exactly one solution exists
        """
        solutions = [0]
        start_time = time.time()
        
        def solve_count(brd: List[List[int]], depth: int = 0) -> None:
            if solutions[0] >= max_solutions:
                return
                
            if depth > 100:  # Prevent excessive recursion
                print("Maximum recursion depth exceeded!")
                return
                
            cell = self._find_best_empty_cell(brd)
            if not cell:
                solutions[0] += 1
                return
                
            row, col = cell
            for num in self._get_candidates(brd, row, col):
                if solutions[0] >= max_solutions:
                    return
                brd[row][col] = num
                solve_count(brd, depth + 1)
                brd[row][col] = 0
        
        board_copy = [row[:] for row in board]
        solve_count(board_copy)
        
        elapsed = time.time() - start_time
        if elapsed > 1.0:  # Log warning if check takes too long
            print(f"Solution uniqueness check took {elapsed:.2f} seconds!")
            
        return solutions[0] == 1

    def count_solutions(self, board: List[List[int]]) -> int:
        """
        Count the number of valid solutions for the given board.

        Args:
            board (List[List[int]]): Current board state

        Returns:
            int: Number of valid solutions
        """
        # Implementation to count solutions
        pass
