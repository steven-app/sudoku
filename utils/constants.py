# Window settings
WINDOW_MIN_SIZE = (1000, 720)

# Colors
COLORS = {
    'BACKGROUND': '#FFFFFF',
    'SELECTED': '#E0E0E0',
    'ERROR': '#FFE6E6',
    'GRID_COLORS': [
        '#FFE4E1', '#E0EEE0', '#E6E6FA',
        '#F0F8FF', '#FFF0F5', '#F0FFFF',
        '#FFF5EE', '#F5F5F5', '#FFFAF0'
    ]
}

# Game settings
BOARD_SIZE = 9
HINTS_MAX = 3

# Font configurations
FONT_CONFIGS = {
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