"""
Window management module.
Handles main window creation and layout management.
"""

import tkinter as tk
from typing import Tuple
from .styles import GameStyles

class WindowManager:
    """Manages main game window and layout."""
    
    def __init__(self):
        """Initialize window manager."""
        self.styles = GameStyles()
        self.window = self._create_window()
        self.frames = self._create_frames()

    def _create_window(self) -> tk.Tk:
        """
        Create and configure main window.

        Returns:
            tk.Tk: Configured main window
        """
        window = tk.Toplevel()
        window.title("Sudoku")
        
        # Set window size and position
        window_width = self.styles.LAYOUT['window']['min_width']
        window_height = self.styles.LAYOUT['window']['min_height']
        
        # Calculate center position
        x = (window.winfo_screenwidth() - window_width) // 2
        y = (window.winfo_screenheight() - window_height) // 2
        
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        window.configure(bg=self.styles.COLORS['background'])
        
        # Configure grid
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=3)  # Game area
        window.grid_columnconfigure(1, weight=1)  # Control panel
        
        return window

    def _create_frames(self) -> dict:
        """
        Create main frame containers.

        Returns:
            dict: Dictionary containing all frame references
        """
        frames = {}

        # Game area frame
        frames['game_area'] = tk.Frame(
            self.window,
            bg=self.styles.COLORS['background']
        )
        frames['game_area'].grid(
            row=0,
            column=0,
            sticky='nsew',
            padx=(20, 10),
            pady=20
        )

        # Board frame
        frames['board'] = tk.Frame(
            frames['game_area'],
            bg=self.styles.COLORS['background']
        )
        frames['board'].pack(side='top', fill='both', expand=True)

        # Utility bar frame
        frames['utility'] = tk.Frame(
            frames['game_area'],
            bg=self.styles.COLORS['background'],
            height=60,
            width=self.styles.LAYOUT['window']['min_width'] - 400
        )
        frames['utility'].pack(side='bottom', fill='x')
        frames['utility'].pack_propagate(False)

        # Control panel frame
        frames['control'] = tk.Frame(
            self.window,
            bg=self.styles.COLORS['background']
        )
        frames['control'].grid(
            row=0,
            column=1,
            sticky='nsew',
            padx=(10, 20),
            pady=20
        )

        return frames

    def get_frame(self, name: str) -> tk.Frame:
        """
        Get frame by name.

        Args:
            name: Frame name

        Returns:
            tk.Frame: Requested frame
        """
        return self.frames.get(name)

    def center_window(self) -> None:
        """Center window on screen."""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'+{x}+{y}')

    def set_topmost(self, state: bool) -> None:
        """
        Set window topmost state.

        Args:
            state: True to set topmost, False to unset
        """
        self.window.attributes('-topmost', state) 