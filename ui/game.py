import tkinter as tk
import random
import sys
import json
import os
from datetime import datetime
import threading
from tkinter import messagebox
from core.generator import SudokuGenerator
from core.validator import SudokuValidator
from utils.constants import WINDOW_MIN_SIZE, FONT_CONFIGS, COLORS, HINTS_MAX
import tkinter.font as tkfont
from ui.styles import GAME_STYLE

class SudokuGame:
    def __init__(self):
        """初始化"""
        # 创建主窗口
        self.window = tk.Tk()
        self.window.title("数独游戏")
        self.window.configure(bg='#FFFFFF')
        self.window.minsize(1000, 720)
        
        # 使主窗口可扩展
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=3)  # 游戏区域
        self.window.grid_columnconfigure(1, weight=1)  # 控制面板
        
        # 加载语言配置
        self.load_language_config()
        
        # 初始化游戏状态
        self.generator = SudokuGenerator()
        self.current_difficulty = self.lang['difficulties']['easy']
        self.current_level = 1
        self.selected_cell = None
        self.time_count = 0
        self.timer_running = False
        self.moves = []
        self.hints_remaining = 3
        self.cells = {}
        self.loading = False
        
        # 设置难度映射
        self.difficulty_mapping = {
            self.lang['difficulties']['easy']: 'easy',
            self.lang['difficulties']['medium']: 'medium',
            self.lang['difficulties']['hard']: 'hard',
            self.lang['difficulties']['expert']: 'expert'
        }
        
        # 设置颜色
        self.selected_color = '#E0E0E0'
        self.error_color = '#FFE6E6'
        self.colors = [
            '#FFE4E1', '#E0EEE0', '#E6E6FA',
            '#F0F8FF', '#FFF0F5', '#F0FFFF',
            '#FFF5EE', '#F5F5F5', '#FFFAF0'
        ]
        
        # 设置字体
        self.font_config = {
            'title': ('Microsoft YaHei', 12),
            'button': ('Microsoft YaHei', 10),
            'cell': ('Microsoft YaHei', 14),
            'button_bold': ('Microsoft YaHei', 10, 'bold')
        }
        
        # 创建框架
        self.create_frames()
        
        # 创建UI元素
        self.create_board()
        self.create_control_panel()
        
        # 开始新游戏
        self.start_new_game()
        
        # 加粗字体
        family = self.font_config['button'][0]
        size = self.font_config['button'][1]
        self.bold_font = tkfont.Font(
            family=family,
            size=size,
            weight='bold'
        )

    def setup_fonts(self):
        """设置字体配置"""
        if sys.platform.startswith('win'):
            self.font_config = {
                'title': ('Microsoft YaHei', 12),
                'button': ('Microsoft YaHei', 10),
                'cell': ('Microsoft YaHei', 14),
                'button_bold': ('Microsoft YaHei', 10, 'bold')
            }
        elif sys.platform.startswith('darwin'):
            self.font_config = {
                'title': ('.AppleSystemUIFont', 12),
                'button': ('.AppleSystemUIFont', 13),
                'cell': ('.AppleSystemUIFont', 18)
            }
        else:
            self.font_config = {
                'title': ('Noto Sans CJK SC Light', 12),
                'button': ('Noto Sans CJK SC Light', 13),
                'cell': ('Noto Sans CJK SC', 18)
            }

    def load_language_config(self):
        """加载语言配置"""
        try:
            # 获取当前文件的目录
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # 构建配置文件的完整路径
            config_path = os.path.join(current_dir, 'config', 'config.json')
            lang_path = os.path.join(current_dir, 'config', 'languages.json')
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                language = config.get('language', 'zh_CN')
                
            with open(lang_path, 'r', encoding='utf-8') as f:
                languages = json.load(f)
                self.lang = languages.get(language, languages['zh_CN'])
        except Exception as e:
            print(f"Error loading language config: {e}")
            # 使用��编码的中文作为后备
            self.lang = {
                "game_title": "数独游戏",
                "difficulty": "难度选择",
                "level": "关卡选择",
                "numpad": "数字键盘",
                "difficulties": {
                    "easy": "简单",
                    "medium": "中等",
                    "hard": "困难",
                    "expert": "专家"
                },
                "title_format": "数独游戏 - {} 第{}关 - {}"
            }

    def create_frames(self):
        """创建主要框架"""
        # 创建左侧游戏区域（可扩展）
        self.game_frame = tk.Frame(self.window, bg='#FFFFFF')
        self.game_frame.grid(row=0, column=0, sticky='nsew', padx=(20,10), pady=20)
        self.game_frame.grid_rowconfigure(0, weight=1)
        self.game_frame.grid_columnconfigure(0, weight=1)
        
        # 创建右侧控制面容器（可扩展）
        self.control_container = tk.Frame(self.window, bg='#FFFFFF')
        self.control_container.grid(row=0, column=1, sticky='nsew', padx=(10,20), pady=20)
        self.control_container.grid_rowconfigure(0, weight=1)
        self.control_container.grid_columnconfigure(0, weight=1)
        
        # 创建控制面板（固定宽度，在器中居中）
        self.control_frame = tk.Frame(self.control_container, bg='#FFFFFF', width=180)
        self.control_frame.place(relx=0.5, rely=0.5, anchor='center')
        self.control_frame.grid_propagate(False)

    def create_board(self):
        """创建数独棋盘"""
        # 创建计时器标签
        self.timer_label = tk.Label(
            self.game_frame,
            text="00:00",
            font=self.font_config['title'],
            bg='#FFFFFF'
        )
        self.timer_label.pack(pady=10)
        
        # 创建棋盘容器
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
                cell_frame.configure(bg=self.colors[color_index])
                
                cell = tk.Label(
                    cell_frame,
                    text="",
                    font=self.font_config['cell'],
                    bg=cell_frame.cget("bg"),
                    width=2,
                    height=1
                )
                cell.pack(expand=True)
                
                # 绑定点击事件
                cell.bind('<Button-1>', lambda e, row=i, col=j: self.cell_clicked(row, col))
                self.cells[(i, j)] = cell

        # 创建功能按钮容器（在棋盘下方）
        buttons_frame = tk.Frame(board_container, bg='#FFFFFF')
        buttons_frame.grid(row=9, column=0, columnspan=9, pady=(20, 0))

        # 通用按钮样式
        button_style = {
            'bg': '#FFFFFF',
            'fg': '#2c3e50',
            'relief': 'flat',
            'font': self.font_config['button'],
            'width': 6,
            'height': 2,
            'borderwidth': 1,
            'highlightthickness': 0
        }

        # 提示按钮
        self.hint_button = tk.Button(
            buttons_frame,
            text=f"提示({self.hints_remaining})",
            command=self.give_hint,
            **button_style
        )
        self.hint_button.pack(side=tk.LEFT, padx=10)

        # 撤销按钮
        self.undo_button = tk.Button(
            buttons_frame,
            text="撤销",
            command=self.undo_move,
            **button_style
        )
        self.undo_button.pack(side=tk.LEFT, padx=10)

        # 检查按钮
        self.check_button = tk.Button(
            buttons_frame,
            text="检查",
            command=self.check_solution,
            **button_style
        )
        self.check_button.pack(side=tk.LEFT, padx=10)

    def create_control_panel(self):
        """创建控制面板"""
        # 通用按钮样式（移除font参数）
        button_style = {
            'fg': '#2c3e50',
            'relief': 'solid',
            'width': 6,
            'height': 2,
            'borderwidth': 1,
            'highlightthickness': 0,
            'bg': '#FFFFFF'
        }

        # 标签框样式
        label_frame_style = {
            'bg': '#FFFFFF',
            'fg': '#2c3e50',
            'font': self.font_config['title'],
            'labelanchor': 'n',
            'borderwidth': 1
        }

        # 难度选择区域
        difficulty_section = tk.LabelFrame(
            self.control_frame,
            text=self.lang['difficulty'],
            **label_frame_style
        )
        difficulty_section.pack(fill='x', padx=5, pady=5)
        
        diff_grid = tk.Frame(difficulty_section, bg='#FFFFFF')
        diff_grid.pack(padx=5, pady=5)
        
        # 存储难度按钮的引用
        self.difficulty_buttons = {}
        
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
                command=lambda d=diff: self.change_difficulty(d),
                font=self.font_config['button_bold'] if diff == self.current_difficulty else self.font_config['button'],
                **button_style
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.difficulty_buttons[diff] = btn

        # 关卡选择区域
        level_section = tk.LabelFrame(
            self.control_frame,
            text=self.lang['level'],
            **label_frame_style
        )
        level_section.pack(fill='x', padx=5, pady=5)
        
        level_grid = tk.Frame(level_section, bg='#FFFFFF')
        level_grid.pack(padx=5, pady=5)
        
        # 存储关卡按钮的引用
        self.level_buttons = {}
        
        chinese_numbers = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
        
        for level in range(1, 11):
            row = (level - 1) // 2
            col = (level - 1) % 2
            btn = tk.Button(
                level_grid,
                text=chinese_numbers[level-1],
                command=lambda l=level: self.change_level(l),
                font=self.font_config['button_bold'] if level == self.current_level else self.font_config['button'],
                **button_style
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.level_buttons[level] = btn

        # 数字键盘区域
        numpad_section = tk.LabelFrame(
            self.control_frame, 
            text=self.lang['numpad'],
            **label_frame_style
        )
        numpad_section.pack(fill='x', padx=5, pady=5)
        
        numpad_grid = tk.Frame(numpad_section, bg='#FFFFFF')
        numpad_grid.pack(padx=5, pady=5)
        
        for i in range(1, 10):
            row = (i - 1) // 3
            col = (i - 1) % 3
            
            btn_frame = tk.Frame(numpad_grid, width=50, height=50, bg='#FFFFFF')
            btn_frame.grid(row=row, column=col, padx=3, pady=3)
            btn_frame.grid_propagate(False)
            
            btn = tk.Button(
                btn_frame, 
                text=str(i),
                command=lambda n=i: self.number_clicked(n),
                **button_style
            )
            btn.place(relx=0.5, rely=0.5, anchor='center', relwidth=1, relheight=1)

    def start_new_game(self):
        """开始新游戏"""
        # 用于标记是否需要显示加载窗口
        self.generation_completed = False
        
        def generate():
            difficulty = self.difficulty_mapping[self.current_difficulty]
            self.current_puzzle, self.solution = self.generator.generate_puzzle(difficulty)
            self.original_cells = {
                (i, j) for i in range(9) for j in range(9)
                if self.current_puzzle[i][j] != 0
            }
            self.generation_completed = True
            self.window.after(0, self.after_generate)
        
        def check_loading():
            if not self.generation_completed:
                self.show_loading()
        
        # 启动生成线程
        threading.Thread(target=generate).start()
        # 如果200ms后还没有生成完成，则显示加载窗口
        self.window.after(200, check_loading)

    def after_generate(self):
        """生成完成后的处理"""
        self.hide_loading()
        
        if not self.current_puzzle or not self.solution:
            messagebox.showerror("错误", "生成数独失败，请重试")
            return
            
        # 重置游戏状态
        self.selected_cell = None
        self.moves = []
        self.hints_remaining = 3
        self.hint_button.configure(text=f"提示({self.hints_remaining})")
        
        # 更新标题
        self.window.title(self.lang['title_format'].format(
            self.current_difficulty,
            self.current_level,
            datetime.now().strftime("%Y-%m-%d")
        ))
        
        # 更新棋盘
        self.update_board()
        
        # 重置并启动计时器
        self.time_count = 0
        self.timer_running = True
        self.update_timer()

    def update_board(self):
        """更新棋盘显示"""
        for i in range(9):
            for j in range(9):
                value = self.current_puzzle[i][j]
                cell = self.cells[(i, j)]
                if value != 0:
                    cell.configure(
                        text=str(value),
                        fg='#666666' if (i, j) in self.original_cells else '#2c3e50'
                    )
                else:
                    cell.configure(text="")

    def cell_clicked(self, row, col):
        """处理单元格点击事件"""
        if self.loading:
            return
            
        # 取消前的选中状态
        if self.selected_cell:
            old_row, old_col = self.selected_cell
            old_cell = self.cells[(old_row, old_col)]
            old_cell_frame = old_cell.master
            color_index = (old_row // 3) * 3 + (old_col // 3)
            old_cell_frame.configure(bg=self.colors[color_index])
            old_cell.configure(bg=self.colors[color_index])
            
        self.selected_cell = (row, col)
        cell = self.cells[(row, col)]
        cell_frame = cell.master
        cell_frame.configure(bg=self.selected_color)
        cell.configure(bg=self.selected_color)

    def number_clicked(self, number):
        """处理数字按钮点击事件"""
        if not self.selected_cell or self.loading:
            return
            
        row, col = self.selected_cell
        if (row, col) in self.original_cells:
            return
            
        # 检查移动是否有效
        if self.is_valid_move(row, col, number):
            # 保存当前值用于撤销
            old_value = self.current_puzzle[row][col]
            self.moves.append((row, col, old_value))
            
            # 更新值
            self.current_puzzle[row][col] = number
            cell = self.cells[(row, col)]
            cell.configure(text=str(number), fg='#2c3e50')
            
            # 检查是否完成
            if self.check_win():
                self.timer_running = False
                messagebox.showinfo("恭喜", "你已经完成了这个数独！")
        else:
            cell = self.cells[(row, col)]
            cell_frame = cell.master
            cell_frame.configure(bg=self.error_color)
            cell.configure(bg=self.error_color)
            self.window.after(500, lambda: (
                cell_frame.configure(bg=self.selected_color),
                cell.configure(bg=self.selected_color)
            ))

    def is_valid_move(self, row, col, num):
        """检查移动是否有效"""
        # 检查行
        for j in range(9):
            if j != col and self.current_puzzle[row][j] == num:
                return False
                
        # 检查列
        for i in range(9):
            if i != row and self.current_puzzle[i][col] == num:
                return False
                
        # 检查3x3方格
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if (i != row or j != col) and self.current_puzzle[i][j] == num:
                    return False
                    
        return True

    def check_win(self):
        """检查是否完成游戏"""
        for i in range(9):
            for j in range(9):
                if self.current_puzzle[i][j] == 0:
                    return False
        return True

    def on_key_press(self, event):
        """处理键盘事件"""
        if not self.selected_cell or self.loading:
            return
            
        if event.char in '123456789':
            self.number_clicked(int(event.char))
        elif event.char == '0' or event.keysym == 'BackSpace':
            self.clear_cell()

    def clear_cell(self):
        """清除选中的单元格"""
        if not self.selected_cell:
            return
            
        row, col = self.selected_cell
        if (row, col) not in self.original_cells:
            old_value = self.current_puzzle[row][col]
            if old_value != 0:
                self.moves.append((row, col, old_value))
            self.current_puzzle[row][col] = 0
            cell = self.cells[(row, col)]
            cell.configure(text="")

    def undo_move(self):
        """撤销上一步移动"""
        if not self.moves or self.loading:
            return
            
        row, col, value = self.moves.pop()
        self.current_puzzle[row][col] = value
        cell = self.cells[(row, col)]
        if value != 0:
            cell.configure(text=str(value), fg='#2c3e50')
        else:
            cell.configure(text="")

    def give_hint(self):
        """提供提示"""
        if self.hints_remaining <= 0 or not self.selected_cell or self.loading:
            return
            
        row, col = self.selected_cell
        if (row, col) in self.original_cells:
            return
            
        correct_value = self.solution[row][col]
        self.current_puzzle[row][col] = correct_value
        cell = self.cells[(row, col)]
        cell.configure(text=str(correct_value), fg='#2c3e50')
        
        self.hints_remaining -= 1
        self.hint_button.configure(text=f"提示({self.hints_remaining})")

    def check_solution(self):
        """检查当前解答"""
        if self.loading:
            return
            
        for i in range(9):
            for j in range(9):
                if self.current_puzzle[i][j] != 0 and self.current_puzzle[i][j] != self.solution[i][j]:
                    messagebox.showinfo("检查结果", "当前解答不正确")
                    return
        messagebox.showinfo("检查结果", "到目前为止都是正确的！")

    def change_difficulty(self, difficulty):
        """改变难度"""
        if difficulty != self.current_difficulty:
            # 更新按��字体
            self.difficulty_buttons[self.current_difficulty].configure(font=self.font_config['button'])
            self.difficulty_buttons[difficulty].configure(font=self.font_config['button_bold'])
            # 更新当前难度
            self.current_difficulty = difficulty
            self.start_new_game()

    def change_level(self, level):
        """改变关卡"""
        if level != self.current_level:
            # 更新按钮字体
            self.level_buttons[self.current_level].configure(font=self.font_config['button'])
            self.level_buttons[level].configure(font=self.font_config['button_bold'])
            # 更新当前关卡
            self.current_level = level
            self.start_new_game()

    def update_timer(self):
        """更新计时器"""
        if self.timer_running:
            minutes = self.time_count // 60
            seconds = self.time_count % 60
            self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
            self.time_count += 1
            self.window.after(1000, self.update_timer)

    def show_loading(self):
        """显示加载提示"""
        self.loading = True
        self.loading_window = tk.Toplevel(self.window)
        self.loading_window.transient(self.window)
        self.loading_window.grab_set()
        
        window_width = 200
        window_height = 100
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.loading_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.loading_window.title("请稍候")
        self.loading_window.configure(bg='#FFFFFF')
        
        label = tk.Label(
            self.loading_window,
            text="正在生成数独...",
            bg='#FFFFFF',
            font=self.font_config['button']
        )
        label.pack(expand=True)

    def hide_loading(self):
        """隐藏加载提示"""
        if hasattr(self, 'loading_window'):
            self.loading_window.destroy()
        self.loading = False

    def run(self):
        """运行游戏"""
        # 绑定键盘事件
        self.window.bind('<Key>', self.on_key_press)
        
        # 开始游戏循环
        self.window.mainloop()

    def get_block_color(self, row, col):
        """获取单元格所在九宫格的颜色"""
        block_row = row // 3
        block_col = col // 3
        block_index = block_row * 3 + block_col
        return GAME_STYLE['cell']['block_colors'][block_index]