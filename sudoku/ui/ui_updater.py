"""
UI update management module.
Handles all UI update operations in the game.
"""

import tkinter as tk
from typing import Dict, Optional, Tuple
from ..game.game_state import GameState
from .board import GameBoard
from .controls import ControlPanel

class UIUpdater:
    """Manages all UI update operations."""
    
    def __init__(
        self,
        board: GameBoard,
        controls: ControlPanel,
        game_state: GameState
    ):
        """
        Initialize UI updater.
        
        Args:
            board: Game board instance
            controls: Control panel instance
            game_state: Game state instance
        """
        self.board = board
        self.controls = controls
        self.game_state = game_state

    def update_board_display(self) -> None:
        """Update the entire board display."""
        for i in range(9):
            for j in range(9):
                value = self.game_state.current_board[i][j]
                state = 'original' if (i, j) in self.game_state.original_cells else 'normal'
                self.board.update_cell(i, j, value, state)

    def update_timer_display(self, seconds: int) -> None:
        """
        Update the timer display.

        Args:
            seconds (int): Elapsed time in seconds
        """
        try:
            minutes = seconds // 60
            seconds = seconds % 60
            time_string = f"{minutes:02d}:{seconds:02d}"
            
            if hasattr(self, 'controls') and self.controls:
                self.controls.update_timer(time_string)
        except tk.TclError:
            pass  # Ignore errors during shutdown

    def update_cell(
        self,
        row: int,
        col: int,
        value: int,
        highlight: str = 'normal'
    ) -> None:
        """
        Update a single cell.

        Args:
            row: Cell row
            col: Cell column
            value: Cell value
            highlight: Highlight state ('normal', 'selected', 'error')
        """
        self.board.update_cell(row, col, str(value))
        self.board.highlight_cell(row, col, highlight)

    def update_hint_count(self, count: int) -> None:
        """
        Update hint count display.

        Args:
            count: Number of hints remaining
        """
        self.controls.update_hint_count(count)

    def update_level_buttons(self) -> None:
        """Update level button states."""
        if hasattr(self.controls, 'update_level_buttons'):
            self.controls.update_level_buttons()

    def update_difficulty_buttons(self) -> None:
        """Update difficulty button states."""
        if hasattr(self.controls, 'update_difficulty_buttons'):
            self.controls.update_difficulty_buttons()

    def clear_cell_highlight(self, row: int, col: int) -> None:
        """
        Clear cell highlight.

        Args:
            row: Cell row
            col: Cell column
        """
        self.board.highlight_cell(row, col)

    def highlight_cell(self, row: int, col: int, state: str = 'selected') -> None:
        """
        Highlight a cell.

        Args:
            row: Cell row
            col: Cell column
            state: Highlight state ('normal', 'selected', 'error')
        """
        self.board.highlight_cell(row, col, state) 