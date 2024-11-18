"""
Main entry point for the Sudoku game.
This module initializes and starts the game.
"""

import tkinter as tk
from sudoku.ui.game_ui import SudokuGame

def main():
    """
    Initialize and start the Sudoku game.
    This function creates the main game instance and starts the game loop.
    """
    print("Starting game...")
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    game = SudokuGame()
    print("Game instance created")
    
    try:
        print("Starting main loop...")
        game.run()
    except Exception as e:
        print(f"Error during game execution: {e}")
    
    print("Game ended")

if __name__ == "__main__":
    main()
