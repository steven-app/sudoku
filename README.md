# Sudoku Game

A feature-rich Sudoku puzzle game built with Python and Tkinter, offering multiple difficulty levels and a clean, modern interface.

## Screenshot

<img width="998" alt="image" src="https://github.com/user-attachments/assets/5263acc1-39e6-44f2-a2ea-2fc916fe78d8">


## Features

- **4 difficulty levels** (Easy, Medium, Hard, Expert)
- **10 levels per difficulty**
- **Multi-language support** (English, Chinese)
- **Hint system** (3 hints per level)
- **Undo functionality**
- **Timer**
- **Modern UI** with color-coded 3x3 boxes
- **Keyboard input support**

## Requirements

- Python 3.6+
- Tkinter (usually comes with Python)

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/steven-app/sudoku.git
   ```

2. Navigate to the game directory:

   ```bash
   cd sudoku/sudoku_game/src
   ```

3. Run the game:

   ```bash
   python main.py
   ```

## How to Play

1. Select a difficulty level (Easy, Medium, Hard, or Expert).
2. Choose a level (1-10).
3. Click a cell and enter numbers using:
   - On-screen number pad
   - Keyboard numbers (1-9)
   - Delete/Backspace to clear a cell
4. Use hints (💡) when stuck (3 hints per level).
5. Use the undo button to correct mistakes.
6. Complete all levels to unlock harder difficulties.

## Game Features

### Difficulty Levels

- **Easy**: 30 empty cells
- **Medium**: 40 empty cells
- **Hard**: 50 empty cells
- **Expert**: 60 empty cells, no hints allowed

### UI Features

- Color-coded 3x3 boxes for better visibility
- Selected cell highlighting
- Error highlighting
- Original numbers in a different color
- Progress tracking across levels

### Controls

- **Mouse**: Click cells and buttons
- **Keyboard**: Numbers 1-9, Delete/Backspace
- **Utility buttons**: Undo, Hint

## Technical Details

### Built using:

- **Python 3.x**
- **Tkinter** for GUI
- **JSON** for language configuration
- Object-oriented design with modular architecture

### Key Components:

- Game state management
- Puzzle generation and validation
- Multi-language support
- Custom styling system
- Event handling system

### Project Structure

```
sudoku_game/
├── src/
│   ├── main.py
│   └── sudoku/
│       ├── config/
│       │   ├── languages.json
│       │   └── settings.py
│       ├── core/
│       │   ├── generator.py
│       │   └── validator.py
│       ├── game/
│       │   └── game_state.py
│       └── ui/
│           ├── board.py
│           ├── controls.py
│           ├── game_ui.py
│           ├── styles.py
│           └── utility_bar.py
```


