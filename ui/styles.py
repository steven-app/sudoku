# 窗口样式
WINDOW_STYLE = {
    'bg': '#FFFFFF',
    'min_width': 1000,
    'min_height': 720
}

# 颜色配置
COLORS = {
    'background': '#FFFFFF',
    'text': '#2c3e50',
    'text_light': '#666666',
    'selected': '#E0E0E0',
    'error': '#FFE6E6',
    'grid_colors': [
        '#FFE4E1', '#E0EEE0', '#E6E6FA',
        '#F0F8FF', '#FFF0F5', '#F0FFFF',
        '#FFF5EE', '#F5F5F5', '#FFFAF0'
    ]
}

# 字体配置
FONTS = {
    'win': {
        'title': ('Microsoft YaHei UI Light', 12),
        'button': ('Microsoft YaHei UI Light', 13),
        'cell': ('Microsoft YaHei UI', 18)
    },
    'darwin': {
        'title': ('.AppleSystemUIFont', 12),
        'button': ('.AppleSystemUIFont', 13),
        'cell': ('.AppleSystemUIFont', 18)
    },
    'linux': {
        'title': ('Noto Sans CJK SC Light', 12),
        'button': ('Noto Sans CJK SC Light', 13),
        'cell': ('Noto Sans CJK SC', 18)
    }
}

# 通用标签框样式
LABEL_FRAME_STYLE = {
    'bg': '#FFFFFF',
    'fg': '#2c3e50',
    'labelanchor': 'n',
    'borderwidth': 1
}

# 通用按钮样式
BUTTON_STYLE = {
    'bg': '#FFFFFF',
    'fg': '#2c3e50',
    'relief': 'flat',
    'width': 6,
    'height': 2,
    'borderwidth': 1,
    'highlightthickness': 0
}

# 单元格样式
CELL_STYLE = {
    'width': 50,
    'height': 50,
    'borderwidth': 1,
    'relief': 'solid'
}

# 游戏区域样式
GAME_STYLE = {
    'cell': {
        'width': 2,
        'height': 1,
        'padx': 1,
        'pady': 1,
        'relief': 'solid',
        'borderwidth': 1,
        'highlightthickness': 0,
        'block_colors': [
            '#E6E6FA',  # 薰衣草紫 - 第一行第一块
            '#F9CBBE',  # 蜜桃粉 - 第一行第二块
            '#FFF2B8',  # 香草黄 - 第一行第三块
            '#D7BCE8',  # 柔雾紫 - 第二行第一块
            '#A7E0C9',  # 薄荷绿 - 第二行第二块
            '#FFD1BA',  # 珊瑚橙 - 第二行第三块
            '#B3E5FC',  # 浅蓝色 - 第三行第一块
            '#CDE7F0',  # 婴儿蓝 - 第三行第二块
            '#FADADD'   # 淡粉色 - 第三行第三块
        ]
    }
} 