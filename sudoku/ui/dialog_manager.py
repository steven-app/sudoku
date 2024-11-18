"""
Dialog management module.
Handles creation and management of all dialog windows in the game.
"""

import tkinter as tk
import tkinter.messagebox as messagebox
from typing import Callable, Optional
from .language_manager import LanguageManager

class DialogManager:
    """Manages all dialog windows in the game."""
    
    def __init__(self, window: tk.Tk, language_manager: LanguageManager):
        """
        Initialize dialog manager.
        
        Args:
            window: Main game window
            language_manager: Language manager instance
        """
        self.window = window
        self.lang = language_manager

    def show_game_complete_dialog(
        self, 
        difficulty: str, 
        level: int,
        on_next_level: Callable,
        on_exit: Optional[Callable] = None
    ) -> None:
        """
        Show game completion dialog.

        Args:
            difficulty: Current game difficulty
            level: Current game level
            on_next_level: Callback for next level button
            on_exit: Optional callback for exit button
        """
        dialog = tk.Toplevel(self.window)
        dialog.title(self.lang.get_text('game_title'))
        dialog.transient(self.window)
        dialog.grab_set()

        # Add congratulations message
        tk.Label(
            dialog,
            text=self.lang.get_text('messages', 'game_won'),
            pady=10,
            padx=20,
            font=('TkDefaultFont', 12, 'bold')
        ).pack()

        # Add level completion message
        level_text = self.lang.get_text(
            'messages', 
            'level_complete',
            difficulty=self.lang.get_text('difficulties', difficulty),
            level=level
        )
        
        tk.Label(
            dialog,
            text=level_text,
            pady=10,
            padx=20
        ).pack()

        # Add buttons frame
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)

        # Next level button
        tk.Button(
            button_frame,
            text=self.lang.get_text('buttons', 'next_level'),
            command=lambda: self._handle_next_level(dialog, on_next_level),
            width=10
        ).pack(side=tk.LEFT, padx=10)

        # Exit button
        tk.Button(
            button_frame,
            text=self.lang.get_text('buttons', 'exit'),
            command=lambda: self._handle_exit(dialog, on_exit),
            width=10
        ).pack(side=tk.RIGHT, padx=10)

        self.center_dialog(dialog)

    def show_confirm_dialog(self, message: str) -> bool:
        """
        Show confirmation dialog.

        Args:
            message: Message to display

        Returns:
            bool: True if confirmed, False otherwise
        """
        return messagebox.askyesno(
            self.lang.get_text('game_title'),
            message
        )

    def show_info_dialog(self, message: str) -> None:
        """
        Show information dialog.

        Args:
            message: Message to display
        """
        messagebox.showinfo(
            self.lang.get_text('game_title'),
            message
        )

    def _handle_next_level(self, dialog: tk.Toplevel, callback: Callable) -> None:
        """
        Handle next level button click.

        Args:
            dialog: Dialog window to close
            callback: Callback to execute
        """
        dialog.destroy()
        if callback:
            callback()

    def _handle_exit(self, dialog: tk.Toplevel, callback: Optional[Callable]) -> None:
        """
        Handle exit button click.

        Args:
            dialog: Dialog window to close
            callback: Optional callback to execute
        """
        dialog.destroy()
        if callback:
            callback()

    def center_dialog(self, dialog: tk.Toplevel) -> None:
        """
        Center dialog on screen.

        Args:
            dialog: Dialog window to center
        """
        dialog.update_idletasks()
        
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        
        dialog.geometry(f'{width}x{height}+{x}+{y}') 