"""
Main game UI module.
Coordinates all UI components and handles the main game window.
"""

import tkinter as tk
from typing import Tuple, Optional, Dict, Callable, Any

from ..game.game_state import GameState
from ..core.game_logic import GameLogic
from ..core.generator import SudokuGenerator
from ..core.validator import SudokuValidator
from ..utils.timer import GameTimer
from .board import GameBoard
from .controls import ControlPanel
from .styles import GameStyles
from .utility_bar import UtilityBar
from .window_manager import WindowManager
from .language_manager import LanguageManager
from .dialog_manager import DialogManager
from .ui_updater import UIUpdater

class SudokuGame:
    """
    Main game class that coordinates all game components and UI elements.
    """

    def __init__(self):
        """Initialize the game and all its components."""
        # Initialize managers
        self.window_manager = WindowManager()
        self.language_manager = LanguageManager()
        self.dialog_manager = DialogManager(
            self.window_manager.window,
            self.language_manager
        )

        # Initialize game components
        self.game_state = GameState()
        self.game_logic = GameLogic()
        self.generator = SudokuGenerator()
        self.validator = SudokuValidator()
        
        # Create game board
        self.board = GameBoard(
            self.window_manager.get_frame('board'),
            self.game_state,
            self.cell_clicked
        )

        # Create utility bar
        self.create_utility_bar()

        # Create control panel
        self.create_controls()

        # Initialize UI updater
        self.ui_updater = UIUpdater(
            self.board,
            self.controls,
            self.game_state
        )

        # Initialize timer
        self.timer = GameTimer(self.ui_updater.update_timer_display)

        # Bind keyboard events
        self.window_manager.window.bind('<Key>', self.handle_keypress)

        # Start new game
        self.start_new_game()

    def create_utility_bar(self) -> None:
        """Create the utility bar."""
        callbacks = {
            'undo': self.undo_move,
            'hint': self.get_hint
        }
        self.utility_bar = UtilityBar(
            self.window_manager.get_frame('utility'),
            callbacks
        )

    def create_controls(self) -> None:
        """Create the control panel."""
        callbacks = {
            'difficulty': self.change_difficulty,
            'level': self.change_level,
            'number': self.number_clicked
        }
        self.controls = ControlPanel(
            self.window_manager.get_frame('control'),
            callbacks,
            self.game_state
        )

    def start_new_game(self) -> None:
        """Start a new game with current difficulty and level."""
        # Generate new puzzle
        difficulty = self.game_state.current_difficulty
        puzzle, solution = self.generator.generate_puzzle(difficulty)
        
        # Initialize game state (this will reset hints to 3)
        self.game_state.initialize_board(puzzle, solution)
        
        # Reset UI
        self.ui_updater.update_board_display()
        self.utility_bar.update_hint_count(self.game_state.hints_remaining)
        self.timer.reset()
        self.timer.start()

    def cell_clicked(self, row: int, col: int) -> None:
        """
        Handle cell click events.

        Args:
            row: Clicked cell row
            col: Clicked cell column
        """
        if self.game_state.is_cell_modifiable(row, col):
            if self.game_state.selected_cell:
                old_row, old_col = self.game_state.selected_cell
                self.ui_updater.clear_cell_highlight(old_row, old_col)
            
            self.game_state.selected_cell = (row, col)
            self.ui_updater.highlight_cell(row, col, 'selected')

    def number_clicked(self, number: int) -> None:
        """
        Handle number button clicks.

        Args:
            number: Clicked number (0-9)
        """
        if not self.game_state.selected_cell:
            return

        row, col = self.game_state.selected_cell
        
        if (row, col) in self.game_state.original_cells:
            return

        is_correct = self.game_state.solution[row][col] == number
        self.game_state.set_cell_value(row, col, number)
        
        self.ui_updater.update_cell(
            row,
            col,
            number,
            'normal' if is_correct else 'error'
        )

        if self.game_state.check_complete():
            self.handle_game_complete()

    def handle_game_complete(self) -> None:
        """Handle game completion."""
        self.timer.stop()
        self.dialog_manager.show_game_complete_dialog(
            self.game_state.current_difficulty,
            self.game_state.current_level,
            self.handle_next_level
        )

    def handle_next_level(self) -> None:
        """Handle transition to next level."""
        if self.game_state.current_level < 10:
            self.game_state.current_level += 1
        else:
            difficulties = ['easy', 'medium', 'hard', 'expert']
            current_idx = difficulties.index(self.game_state.current_difficulty)
            if current_idx < len(difficulties) - 1:
                self.game_state.current_difficulty = difficulties[current_idx + 1]
                self.game_state.current_level = 1
            else:
                self.dialog_manager.show_info_dialog(
                    self.language_manager.get_text('messages', 'all_complete')
                )
                self.window_manager.window.quit()
                return

        self.ui_updater.update_level_buttons()
        self.start_new_game()  # This will reset hints to 3 for the new level

    def change_difficulty(self, difficulty: str) -> None:
        """
        Change game difficulty.

        Args:
            difficulty: New difficulty level
        """
        self.game_state.current_difficulty = difficulty
        self.start_new_game()

    def change_level(self, level: int) -> None:
        """
        Change game level.

        Args:
            level: New level number
        """
        self.game_state.current_level = level
        self.ui_updater.update_level_buttons()
        self.start_new_game()

    def get_hint(self) -> None:
        """Provide a hint for the current selected cell."""
        if (not self.game_state.selected_cell or
            self.game_state.hints_remaining <= 0):
            return

        row, col = self.game_state.selected_cell
        
        if (row, col) in self.game_state.original_cells:
            return

        correct_value = self.game_state.solution[row][col]
        self.game_state.set_cell_value(row, col, correct_value)
        
        self.ui_updater.update_cell(row, col, correct_value)
        self.game_state.hints_remaining -= 1
        self.utility_bar.update_hint_count(self.game_state.hints_remaining)

    def handle_keypress(self, event: tk.Event) -> None:
        """
        Handle keyboard input.

        Args:
            event: Keyboard event
        """
        if not self.game_state.selected_cell:
            return

        if event.char in '123456789':
            self.number_clicked(int(event.char))
        elif event.keysym in ('BackSpace', 'Delete'):
            self.number_clicked(0)

    def run(self) -> None:
        """Start the game main loop."""
        self.window_manager.window.mainloop()

    def undo_move(self) -> None:
        """Undo the last move if possible."""
        if not self.game_state.move_history:
            return
        
        # Get last move
        last_move = self.game_state.move_history.pop()
        row, col, prev_value = last_move
        
        # Restore previous value
        self.game_state.set_cell_value(row, col, prev_value)
        
        # Update UI
        self.ui_updater.update_cell(
            row,
            col,
            prev_value,
            'normal'
        )
