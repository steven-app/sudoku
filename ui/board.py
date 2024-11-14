import tkinter as tk
from utils.constants import COLORS, FONT_CONFIGS
import sys

class SudokuBoard:
    def __init__(self, game_frame, font_config):
        self.game_frame = game_frame
        self.font_config = font_config
        self.cells = {}
        self.create_board()

    def create_board(self):
        """创建9x9的棋盘"""
        # 创建居中的棋盘容器
        board_container = tk.Frame(self.game_frame, bg='#FFFFFF')
        board_container.place(relx=0.5, rely=0.5, anchor='center')
        
        # 创建9x9的棋盘
        for i in range(9):
            for j in range(9):
                cell_frame = tk.Frame(
                    board_container,
                    borderwidth=1,
                    relief="solid",
                    width=50,
                    height=50
                )
                cell_frame.pack_propagate(False)
                cell_frame.grid(row=i, column=j, padx=1, pady=1)
                
                color_index = (i // 3) * 3 + (j // 3)
                cell_frame.configure(bg=COLORS['GRID_COLORS'][color_index])
                
                cell = tk.Label(
                    cell_frame,
                    text="",
                    font=self.font_config['cell'],
                    bg=cell_frame.cget("bg"),
                    width=2,
                    height=1
                )
                cell.pack(expand=True)
                
                self.cells[(i, j)] = cell

    def update_cell(self, row, col, value, is_original=False):
        """更新单元格的值"""
        cell = self.cells[(row, col)]
        if value != 0:
            cell.configure(
                text=str(value),
                fg='#666666' if is_original else '#2c3e50'
            )
        else:
            cell.configure(text="")

    def highlight_cell(self, row, col, highlight_type=None):
        """高亮显示单元格"""
        cell_frame = self.cells[(row, col)].master
        cell = self.cells[(row, col)]
        
        if highlight_type == 'selected':
            cell_frame.configure(bg=COLORS['SELECTED'])
            cell.configure(bg=COLORS['SELECTED'])
        elif highlight_type == 'error':
            cell_frame.configure(bg=COLORS['ERROR'])
            cell.configure(bg=COLORS['ERROR'])
        else:
            # 恢复原始颜色
            original_color = COLORS['GRID_COLORS'][self.get_box_index(row, col)]
            cell_frame.configure(bg=original_color)
            cell.configure(bg=original_color)

    def get_box_index(self, row, col):
        """获取3x3方格的索引"""
        return (row // 3) * 3 + (col // 3)

    def bind_cell_click(self, callback):
        """绑定单元格点击事件"""
        for (row, col), cell in self.cells.items():
            cell.bind('<Button-1>', lambda e, r=row, c=col: callback(r, c)) 