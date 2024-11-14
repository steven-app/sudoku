def get_box_coordinates(row, col):
    """获取指定位置所在的3x3方格的起始坐标"""
    box_row = 3 * (row // 3)
    box_col = 3 * (col // 3)
    return box_row, box_col

def get_box_index(row, col):
    """获取指定位置所在的3x3方格的索引(0-8)"""
    return (row // 3) * 3 + (col // 3)

def format_time(seconds):
    """格式化时间显示"""
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def get_cell_position(event, cell_size=50):
    """根据点击事件获取单元格位置"""
    row = event.y // cell_size
    col = event.x // cell_size
    if 0 <= row < 9 and 0 <= col < 9:
        return row, col
    return None

def is_valid_position(row, col):
    """检查位置是否有效"""
    return 0 <= row < 9 and 0 <= col < 9

def is_valid_value(value):
    """检查数值是否有效"""
    return isinstance(value, int) and 0 <= value <= 9

def deep_copy_board(board):
    """深拷贝数独板"""
    return [[board[i][j] for j in range(9)] for i in range(9)]

def get_empty_board():
    """获取空的数独板"""
    return [[0 for _ in range(9)] for _ in range(9)]

def count_filled_cells(board):
    """计算已填充的单元格数量"""
    return sum(1 for row in board for cell in row if cell != 0)

def get_difficulty_ratio(difficulty):
    """获取难度对应的填充比例"""
    ratios = {
        'easy': 0.5,      # 50% cells filled
        'medium': 0.4,    # 40% cells filled
        'hard': 0.3,      # 30% cells filled
        'expert': 0.25    # 25% cells filled
    }
    return ratios.get(difficulty, 0.5) 