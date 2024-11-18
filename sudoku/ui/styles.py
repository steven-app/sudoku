"""
Styles configuration module for the Sudoku game UI.
Provides centralized management of colors, fonts, and layout parameters.
"""

import sys
from typing import Dict, Tuple, Any

class GameStyles:
    """
    Defines and manages all UI styles for the Sudoku game.
    Includes colors, fonts, dimensions, and component-specific styles.
    """
    
    # 布局配置
    LAYOUT = {
        'window': {
            'min_width': 1000,
            'min_height': 720,
            'padding': 20
        },
        'cell': {
            'size': 55,
            'padding': 1,
            'block_padding': 3
        },
        'grid': {
            'line_width': 1,
            'block_line_width': 2
        },
        'control': {
            'width': 180,
            'padding': 5
        },
        'button': {
            'width': 6,
            'height': 2,
            'padding': 2
        }
    }

    # 颜色配置
    COLORS = {
        'background': '#FFFFFF',  # 主背景色
        'board': {
            'background': '#FFFFFF',  # 棋盘背景
            'grid_line': '#2c3e50',  # 网格线颜色
            'block_line': '#2c3e50', # 3x3宫格边界颜色
            'selected': '#E0E0E0',   # 选中单元格颜色
            'error': '#FF4444'       # 错误单元格颜色
        },
        'text': {
            'primary': '#2c3e50',    # 主要文字颜色
            'secondary': '#666666',   # 次要文字颜色（原始数字）
            'input': '#2c3e50'       # 玩家输入的数字颜色
        },
        'box_colors': [              # 3x3宫格背景色
            '#E6E6FA',  # 淡紫色 Lavender
            '#FFB6C1',  # 浅粉色 Light Pink (替换原来的珊瑚色)
            '#FFF2B8',  # 淡黄色 Light Yellow
            '#D7BCE8',  # 浅紫色 Light Purple
            '#A7E0C9',  # 薄荷绿 Mint Green
            '#87CEEB',  # 天蓝色 Sky Blue (替换原来的橙粉色)
            '#B3E5FC',  # 浅蓝色 Light Blue
            '#CDE7F0',  # 粉蓝色 Powder Blue
            '#FADADD'   # 浅玫瑰 Light Rose
        ],
        'button': {
            'bg': '#FFFFFF',
            'fg': '#2c3e50'
        }
    }

    def __init__(self):
        """Initialize styles configuration."""
        self.setup_fonts()

    def setup_fonts(self) -> None:
        """Set up system-specific fonts."""
        if sys.platform.startswith('win'):
            self.fonts = {
                'title': ('Microsoft YaHei UI Light', 12),
                'button': ('Microsoft YaHei UI Light', 13),
                'cell': ('Microsoft YaHei UI', 18)
            }
        elif sys.platform.startswith('darwin'):
            self.fonts = {
                'title': ('.AppleSystemUIFont', 12),
                'button': ('.AppleSystemUIFont', 13),
                'cell': ('.AppleSystemUIFont', 18)
            }
        else:
            self.fonts = {
                'title': ('Noto Sans CJK SC Light', 12),
                'button': ('Noto Sans CJK SC Light', 13),
                'cell': ('Noto Sans CJK SC', 18)
            }

    def get_fonts(self) -> Dict[str, Tuple[str, int]]:
        """Get font configurations.
        
        Returns:
            Dict[str, Tuple[str, int]]: Font configurations for different UI elements
        """
        return self.fonts

    def get_cell_style(self, row: int, col: int, state: str = 'normal') -> Dict[str, Any]:
        """Get style for a cell."""
        base_style = {
            'width': 2,
            'height': 1,
            'font': self.fonts['cell'],
            'relief': 'flat',
            'borderwidth': 1
        }

        # 设置背景色和文字颜色
        if state == 'selected':
            base_style['bg'] = self.COLORS['board']['selected']
            base_style['fg'] = self.COLORS['text']['primary']
        elif state == 'error':
            base_style['bg'] = self.COLORS['board']['error']
            base_style['fg'] = self.COLORS['text']['primary']
        elif state == 'original':
            color_index = (row // 3) * 3 + (col // 3)
            base_style['bg'] = self.COLORS['box_colors'][color_index]
            base_style['fg'] = self.COLORS['text']['secondary']
        else:
            color_index = (row // 3) * 3 + (col // 3)
            base_style['bg'] = self.COLORS['box_colors'][color_index]
            base_style['fg'] = self.COLORS['text']['primary']

        return base_style

    def get_button_style(self, is_current: bool = False) -> Dict[str, Any]:
        """
        Get style for buttons.
        
        Args:
            is_current (bool): Whether this button represents current selection
            
        Returns:
            Dict[str, Any]: Button style configuration
        """
        font_name, font_size = self.fonts['button']
        return {
            'bg': self.COLORS['button']['bg'],
            'fg': self.COLORS['button']['fg'],
            'relief': 'flat',
            'font': (font_name, font_size, 'bold' if is_current else 'normal'),
            'width': 6,
            'height': 2,
            'borderwidth': 1,
            'highlightthickness': 0
        }

    def get_label_frame_style(self) -> Dict[str, Any]:
        """Get style for label frames."""
        return {
            'bg': self.COLORS['background'],
            'fg': self.COLORS['text']['primary'],
            'font': self.fonts['title'],
            'labelanchor': 'n',
            'borderwidth': 1
        }

    def get_frame_style(self, frame_type: str = 'default') -> Dict[str, Any]:
        """Get style for frames."""
        base_style = {
            'bg': self.COLORS['background'],
            'relief': 'flat',
            'borderwidth': 0
        }

        if frame_type == 'board':
            base_style.update({
                'bg': self.COLORS['board']['grid_line'],
                'relief': 'solid',
                'borderwidth': 1,
                'padx': 2,
                'pady': 2
            })

        return base_style

    def get_numpad_frame_style(self) -> Dict[str, Any]:
        """Get style configuration for numpad button frames."""
        return {
            'width': self.LAYOUT['cell']['size'],
            'height': self.LAYOUT['cell']['size'],
            'bg': self.COLORS['background']
        }

    def get_numpad_button_style(self) -> Dict[str, Any]:
        """Get style configuration for numpad buttons."""
        return {
            'bg': self.COLORS['button']['bg'],
            'fg': self.COLORS['button']['fg'],
            'relief': 'flat',
            'font': self.fonts['button'],
            'borderwidth': 1,
            'highlightthickness': 0
        }

    def get_numpad_layout(self) -> Dict[str, Any]:
        """Get layout configuration for numpad buttons."""
        return {
            'padx': self.LAYOUT['cell']['padding'],
            'pady': self.LAYOUT['cell']['padding']
        }
