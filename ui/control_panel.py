import tkinter as tk
from utils.constants import COLORS

class ControlPanel:
    def __init__(self, control_frame, font_config, lang):
        self.control_frame = control_frame
        self.font_config = font_config
        self.lang = lang
        
        # 通用标签框样式
        self.label_frame_style = {
            'bg': '#FFFFFF',
            'fg': '#2c3e50',
            'font': self.font_config['title'],
            'labelanchor': 'n',
            'borderwidth': 1
        }
        
        # 通用按钮样式
        self.button_style = {
            'bg': '#FFFFFF',
            'fg': '#2c3e50',
            'relief': 'flat',
            'font': self.font_config['button'],
            'width': 6,
            'height': 2,
            'borderwidth': 1,
            'highlightthickness': 0
        }

    def create_difficulty_section(self, difficulty_callback):
        """创建难度选择区域"""
        difficulty_section = tk.LabelFrame(
            self.control_frame, 
            text=self.lang['difficulty'],
            **self.label_frame_style
        )
        difficulty_section.pack(fill='x', padx=5, pady=5)
        
        diff_grid = tk.Frame(difficulty_section, bg='#FFFFFF')
        diff_grid.pack(padx=5, pady=5)
        
        difficulties = [
            self.lang['difficulties']['easy'],
            self.lang['difficulties']['medium'],
            self.lang['difficulties']['hard'],
            self.lang['difficulties']['expert']
        ]
        
        for i, diff in enumerate(difficulties):
            row = i // 2
            col = i % 2
            btn = tk.Button(
                diff_grid, 
                text=diff,
                command=lambda d=diff: difficulty_callback(d),
                **self.button_style
            )
            btn.grid(row=row, column=col, padx=2, pady=2)

    def create_level_section(self, level_callback):
        """创建关卡选择区域"""
        level_section = tk.LabelFrame(
            self.control_frame, 
            text=self.lang['level'],
            **self.label_frame_style
        )
        level_section.pack(fill='x', padx=5, pady=5)
        
        level_grid = tk.Frame(level_section, bg='#FFFFFF')
        level_grid.pack(padx=5, pady=5)
        
        for level in range(1, 11):
            row = (level - 1) // 2
            col = (level - 1) % 2
            btn = tk.Button(
                level_grid, 
                text=str(level),
                command=lambda l=level: level_callback(l),
                **self.button_style
            )
            btn.grid(row=row, column=col, padx=2, pady=2)

    def create_numpad(self, number_callback):
        """创建数字键盘区域"""
        numpad_section = tk.LabelFrame(
            self.control_frame, 
            text=self.lang['numpad'],
            **self.label_frame_style
        )
        numpad_section.pack(fill='x', padx=5, pady=5)
        
        numpad_grid = tk.Frame(numpad_section, bg='#FFFFFF')
        numpad_grid.pack(padx=5, pady=5)
        
        for i in range(1, 10):
            row = (i - 1) // 3
            col = (i - 1) % 3
            btn = tk.Button(
                numpad_grid, 
                text=str(i),
                command=lambda n=i: number_callback(n),
                **self.button_style
            )
            btn.grid(row=row, column=col, padx=2, pady=2)