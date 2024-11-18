"""
Utility bar module for the Sudoku game.
Handles undo and hint buttons placed below the game board.
"""

import tkinter as tk
from typing import Dict, Callable
from .styles import GameStyles
from ..game.game_state import GameState

class UtilityBar:
    """Creates and manages the utility buttons bar interface."""

    def __init__(self, parent: tk.Frame, callbacks: Dict[str, Callable]):
        """
        Initialize the utility bar.

        Args:
            parent (tk.Frame): Parent frame to contain the utility bar
            callbacks (Dict[str, Callable]): Dictionary of callback functions
        """
        self.parent = parent
        self.callbacks = callbacks
        self.styles = GameStyles()
        self.create_utility_bar()

    def create_utility_bar(self) -> None:
        """Create the utility bar with undo and hint buttons."""
        # 创建居中的按钮容器
        button_container = tk.Frame(
            self.parent,
            bg=self.styles.COLORS['background']
        )
        button_container.place(relx=0.5, rely=0.5, anchor='center')

        # Undo按钮
        self.undo_btn = tk.Button(
            button_container,
            text="↶ Undo",
            command=self.callbacks['undo'],
            **self.styles.get_button_style()
        )
        self.undo_btn.pack(side='left', padx=20)

        # Hint按钮
        self.hint_btn = tk.Button(
            button_container,
            text="💡 Hint (3)",
            command=self.callbacks['hint'],
            **self.styles.get_button_style()
        )
        self.hint_btn.pack(side='left', padx=20)

    def update_hint_count(self, count: int) -> None:
        """
        Update the hint button text with remaining hints.

        Args:
            count (int): Number of remaining hints
        """
        if hasattr(self, 'hint_btn'):
            self.hint_btn.configure(
                text=f"💡 Hint ({count})",
                state='normal' if count > 0 else 'disabled'
            )