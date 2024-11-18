"""
Control panel module for the Sudoku game.
Handles the creation and management of game controls including difficulty selection,
level selection, number pad, and utility buttons.
"""

import tkinter as tk
from typing import Callable, Dict, Any
from .styles import GameStyles
from ..game.game_state import GameState
import json

class ControlPanel:
    """Creates and manages the control panel interface."""

    def __init__(self, parent: tk.Frame, callbacks: Dict[str, Callable], game_state: GameState):
        """
        Initialize the control panel.

        Args:
            parent (tk.Frame): Parent frame to contain the controls
            callbacks (Dict[str, Callable]): Dictionary of callback functions
            game_state (GameState): Game state manager
        """
        self.parent = parent
        self.callbacks = callbacks
        self.game_state = game_state
        self.styles = GameStyles()
        self.timer_label = None
        
        # Load language configuration
        self.current_language = 'zh_CN'  # Default to Chinese
        self.load_language_config()
        
        self.create_control_panel()

    def load_language_config(self) -> None:
        """Load language configuration from JSON file."""
        try:
            with open('sudoku/config/languages.json', 'r', encoding='utf-8') as f:
                self.languages = json.load(f)
        except FileNotFoundError:
            print("Warning: Language configuration file not found")
            self.languages = {}

    def get_text(self, *keys: str, **kwargs: Any) -> str:
        """
        Get localized text with nested keys.

        Args:
            *keys: Sequence of nested dictionary keys
            **kwargs: Format parameters

        Returns:
            str: Localized text
        """
        try:
            text = self.languages[self.current_language]
            for key in keys:
                text = text[key]
            if kwargs:
                return text.format(**kwargs)
            return text
        except (KeyError, AttributeError):
            return keys[-1]

    def update_timer(self, time_str: str) -> None:
        """
        Update the timer display.

        Args:
            time_str (str): Formatted time string (MM:SS)
        """
        if self.timer_label and self.timer_label.winfo_exists():
            try:
                self.timer_label.configure(text=time_str)
            except tk.TclError:
                pass  # Ignore errors if widget is being destroyed

    def create_timer_display(self) -> None:
        """Create the timer display section."""
        timer_frame = tk.Frame(
            self.parent,
            bg=self.styles.COLORS['background']
        )
        timer_frame.pack(fill='x', padx=5, pady=5)

        # Create timer label
        self.timer_label = tk.Label(
            timer_frame,
            text="00:00",
            font=self.styles.get_fonts()['title'],
            bg=self.styles.COLORS['background'],
            fg=self.styles.COLORS['text']['primary']
        )
        self.timer_label.pack(anchor='e', padx=5)

    def create_control_panel(self) -> None:
        """Create all control panel elements."""
        # Create timer display
        self.create_timer_display()
        
        # Create difficulty selector
        self.create_difficulty_section()
        
        # Create level selector
        self.create_level_section()
        
        # Create number pad
        self.create_numpad_section()

    def create_difficulty_section(self) -> None:
        """Create the difficulty selection section."""
        # Create section container
        difficulty_section = tk.LabelFrame(
            self.parent,
            text="Difficulty",
            **self.styles.get_label_frame_style()
        )
        difficulty_section.pack(fill='x', padx=5, pady=5)

        # Create difficulty buttons grid
        button_grid = tk.Frame(difficulty_section, bg=self.styles.COLORS['background'])
        button_grid.pack(padx=5, pady=5)

        # Create difficulty buttons
        difficulties = ['easy', 'medium', 'hard', 'expert']
        labels = ['Easy', 'Medium', 'Hard', 'Expert']
        
        # 存储按钮引用
        self.difficulty_buttons = {}
        
        for i, (diff, label) in enumerate(zip(difficulties, labels)):
            btn = tk.Button(
                button_grid,
                text=label,
                command=lambda d=diff: self.on_difficulty_click(d),
                **self.styles.get_button_style(diff == self.game_state.current_difficulty)
            )
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.difficulty_buttons[diff] = btn

    def create_level_section(self) -> None:
        """Create the level selection section."""
        # Create section container
        level_section = tk.LabelFrame(
            self.parent,
            text=self.get_text('level'),
            **self.styles.get_label_frame_style()
        )
        level_section.pack(fill='x', padx=5, pady=5)

        # Create level buttons grid
        level_grid = tk.Frame(level_section, bg=self.styles.COLORS['background'])
        level_grid.pack(padx=5, pady=5)

        # Chinese number mapping
        chinese_numbers = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
        
        # Store button references
        self.level_buttons = {}
        
        for level in range(1, 11):
            btn = tk.Button(
                level_grid,
                text=chinese_numbers[level-1],
                command=lambda l=level: self.callbacks['level'](l),
                **self.styles.get_button_style(level == self.game_state.current_level)
            )
            row = (level - 1) // 2
            col = (level - 1) % 2
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.level_buttons[level] = btn

    def on_difficulty_click(self, difficulty: str) -> None:
        """Handle difficulty button click."""
        # 更新所有按钮样式
        for diff, btn in self.difficulty_buttons.items():
            btn.configure(**self.styles.get_button_style(diff == difficulty))
        # 调用原始回调
        self.callbacks['difficulty'](difficulty)

    def on_level_click(self, level: int) -> None:
        """Handle level button click."""
        # 更新所有按钮样式
        for lvl, btn in self.level_buttons.items():
            btn.configure(**self.styles.get_button_style(lvl == level))
        # 调用原始回调
        self.callbacks['level'](level)

    def create_numpad_section(self) -> None:
        """Create the number pad section."""
        # Create number pad container
        numpad_section = tk.LabelFrame(
            self.parent,
            text="Number Pad",
            **self.styles.get_label_frame_style()
        )
        numpad_section.pack(fill='x', padx=5, pady=5)
        
        # Create number pad grid container
        numpad_grid = tk.Frame(numpad_section, bg=self.styles.COLORS['background'])
        numpad_grid.pack(padx=5, pady=5)
        
        # Create number buttons (1-9)
        for i in range(1, 10):
            row = (i - 1) // 3
            col = (i - 1) % 3
            
            # Create fixed-size frame
            btn_frame = tk.Frame(
                numpad_grid,
                **self.styles.get_numpad_frame_style()
            )
            btn_frame.grid(
                row=row,
                column=col,
                **self.styles.get_numpad_layout()
            )
            btn_frame.grid_propagate(False)  # Keep frame size fixed
            
            # Create button within frame
            btn = tk.Button(
                btn_frame,
                text=str(i),
                command=lambda n=i: self.callbacks['number'](n),
                **self.styles.get_numpad_button_style()
            )
            btn.place(
                relx=0.5,
                rely=0.5,
                anchor='center',
                relwidth=1,
                relheight=1
            )

    def update_level_buttons(self) -> None:
        """Update the level buttons to reflect current level."""
        if hasattr(self, 'level_buttons'):
            for level, btn in self.level_buttons.items():
                is_current = level == self.game_state.current_level
                style = self.styles.get_button_style(is_current)
                btn.configure(**style)

