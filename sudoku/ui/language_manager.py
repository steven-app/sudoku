"""
Language management module.
Handles loading and providing localized text from language configuration.
"""

import json
from typing import Any
from ..config.settings import DEFAULT_SETTINGS, SUPPORTED_LANGUAGES

class LanguageManager:
    """Manages language configuration and text localization."""
    
    def __init__(self, language: str = None):
        """
        Initialize language manager.
        
        Args:
            language (str, optional): Initial language code. 
                                    Defaults to settings default language.
        """
        self.current_language = language or DEFAULT_SETTINGS['language']
        self.languages = {}
        self.load_language_config()

    def load_language_config(self) -> None:
        """Load language configuration from JSON file."""
        try:
            with open('sudoku/config/languages.json', 'r', encoding='utf-8') as f:
                self.languages = json.load(f)
        except FileNotFoundError:
            print("Warning: Language configuration file not found")
            self.languages = {}

    def set_language(self, language: str) -> bool:
        """
        Set current language if supported.

        Args:
            language (str): Language code to set

        Returns:
            bool: True if language was set successfully, False otherwise
        """
        if language in SUPPORTED_LANGUAGES and language in self.languages:
            self.current_language = language
            return True
        return False

    def get_text(self, *keys: str, **kwargs: Any) -> str:
        """
        Get localized text with nested keys.

        Args:
            *keys: Sequence of nested dictionary keys
            **kwargs: Format parameters

        Returns:
            str: Localized text
        """
        try:
            text = self.languages[self.current_language]
            for key in keys:
                text = text[key]
            if kwargs:
                return text.format(**kwargs)
            return text
        except (KeyError, AttributeError):
            return keys[-1]
  