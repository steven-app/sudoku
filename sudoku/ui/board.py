"""
Sudoku game board UI module.
Handles the creation and management of the game board interface.
"""

import tkinter as tk
from typing import Dict, Tuple, Callable

from .styles import GameStyles
from ..game.game_state import GameState

class GameBoard:
    """
    Creates and manages the Sudoku game board interface.
    Handles cell creation, selection, and updates.
    """

    def __init__(self, parent: tk.Frame, game_state: GameState, 
                 on_cell_click: Callable[[int, int], None]):
        """
        Initialize the game board.

        Args:
            parent (tk.Frame): Parent frame to contain the board
            game_state (GameState): Game state manager
            on_cell_click (callable): Callback for cell click events
        """
        self.parent = parent
        self.game_state = game_state
        self.on_cell_click = on_cell_click
        self.cells: Dict[Tuple[int, int], tk.Label] = {}
        self.styles = GameStyles()
        
        # 创建画布
        board_size = 9 * self.styles.LAYOUT['cell']['size']
        self.canvas = tk.Canvas(
            self.parent,
            width=board_size,
            height=board_size,
            bg=self.styles.COLORS['board']['background'],
            highlightthickness=0
        )
        self.canvas.pack(expand=True)
        
        # 存储单元格引用
        self.cells = {}
        
        # 创建棋盘
        self.create_board()
        
        # 绑定点击事件
        self.canvas.bind('<Button-1>', self.on_canvas_click)

    def on_canvas_click(self, event):
        """Handle canvas click events."""
        # 计算点击的单元格位置
        cell_size = self.styles.LAYOUT['cell']['size']
        row = event.y // cell_size
        col = event.x // cell_size
        
        if 0 <= row < 9 and 0 <= col < 9:
            self.on_cell_click(row, col)

    def create_board(self) -> None:
        """Create the complete board."""
        cell_size = self.styles.LAYOUT['cell']['size']
        board_size = 9 * cell_size
        
        # 创建所有单元格
        for i in range(9):
            for j in range(9):
                self.create_cell(i, j)
        
        # 绘制粗边界线（3x3宫格的边界）
        for i in range(4):
            # 垂直线
            x = i * 3 * cell_size
            self.canvas.create_line(
                x, 0, x, board_size,
                fill=self.styles.COLORS['board']['block_line'],
                width=2
            )
            
            # 水平线
            y = i * 3 * cell_size
            self.canvas.create_line(
                0, y, board_size, y,
                fill=self.styles.COLORS['board']['block_line'],
                width=2
            )
        
        # 添加最外层边框
        self.canvas.create_rectangle(
            0, 0, board_size, board_size,
            outline=self.styles.COLORS['board']['block_line'],
            width=2
        )

    def create_cell(self, row: int, col: int) -> None:
        """Create a single cell on the board."""
        cell_size = self.styles.LAYOUT['cell']['size']
        x1 = col * cell_size
        y1 = row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size
        
        # 获取3x3宫格的颜色
        color_index = (row // 3) * 3 + (col // 3)
        bg_color = self.styles.COLORS['box_colors'][color_index]
        
        # 创建单元格背景
        cell_id = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=bg_color,
            outline=self.styles.COLORS['board']['grid_line'],
            width=1,
            tags=f'cell_{row}_{col}'
        )
        
        # 创建单元格文本
        text_id = self.canvas.create_text(
            (x1 + x2) / 2,
            (y1 + y2) / 2,
            text='',
            font=self.styles.get_fonts()['cell'],
            fill=self.styles.COLORS['text']['primary'],
            tags=f'text_{row}_{col}'
        )
        
        # 存储单元格引用
        self.cells[(row, col)] = {
            'rect': cell_id,
            'text': text_id
        }

    def update_cell(self, row: int, col: int, value: str, state: str = 'normal') -> None:
        """Update the content and style of a cell."""
        if (row, col) not in self.cells:
            return
            
        cell = self.cells[(row, col)]
        
        # 更新文本
        self.canvas.itemconfig(cell['text'], text=str(value) if value else '')
        
        # 更新样式
        color_index = (row // 3) * 3 + (col // 3)
        if state == 'selected':
            bg_color = self.styles.COLORS['board']['selected']
        elif state == 'error':
            bg_color = self.styles.COLORS['board']['error']
        else:
            bg_color = self.styles.COLORS['box_colors'][color_index]
            
        self.canvas.itemconfig(cell['rect'], fill=bg_color)

    def highlight_cell(self, row: int, col: int, state: str = 'normal') -> None:
        """Highlight a cell on the board with specified state.
        
        Args:
            row: Row index of the cell
            col: Column index of the cell
            state: Cell state ('normal', 'selected', 'error')
        """
        if (row, col) not in self.cells:
            return
        
        cell = self.cells[(row, col)]
        
        # 根据状态设置背景色
        if state == 'selected':
            bg_color = self.styles.COLORS['board']['selected']
        elif state == 'error':
            bg_color = self.styles.COLORS['board']['error']
        else:
            color_index = (row // 3) * 3 + (col // 3)
            bg_color = self.styles.COLORS['box_colors'][color_index]
        
        # 设置背景色
        self.canvas.itemconfig(
            cell['rect'],
            fill=bg_color
        )
        
        # 设置文本颜色
        text_color = (
            self.styles.COLORS['text']['secondary'] 
            if (row, col) in self.game_state.original_cells 
            else self.styles.COLORS['text']['primary']
        )
        self.canvas.itemconfig(
            cell['text'],
            fill=text_color
        )

    def select_cell(self, row: int, col: int) -> None:
        """Select a cell and highlight it."""
        if (row, col) not in self.cells:
            return
        
        cell = self.cells[(row, col)]
        
        # 设置选中状态的背景色
        self.canvas.itemconfig(
            cell['rect'],
            fill=self.styles.COLORS['board']['selected']
        )

    def clear_highlights(self) -> None:
        """Clear all cell highlights."""
        for (row, col), cell in self.cells.items():
            if (row, col) not in self.game_state.original_cells:
                self.highlight_cell(row, col)
