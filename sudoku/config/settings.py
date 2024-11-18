"""
Game settings configuration module.
Defines default game settings and configuration options.
"""

# Default game settings
DEFAULT_SETTINGS = {
    'language': 'zh_CN',
    'difficulty': 'easy',
    'level': 1,
    'hints_per_game': 3,
    'show_timer': True,
    'highlight_same_numbers': True
}

# Available languages
SUPPORTED_LANGUAGES = ['zh_CN', 'en_US']

# Game difficulties and their parameters
DIFFICULTY_SETTINGS = {
    'easy': {
        'empty_cells': 30,
        'hints_allowed': True
    },
    'medium': {
        'empty_cells': 40,
        'hints_allowed': True
    },
    'hard': {
        'empty_cells': 50,
        'hints_allowed': True
    },
    'expert': {
        'empty_cells': 60,
        'hints_allowed': False
    }
}
