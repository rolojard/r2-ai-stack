#!/usr/bin/env python3
from logicengine import LogicEngine    # adjust import to match the unzip

class LogicEngineDriver:
    """
    Controls your front and rear logic panels via the LogicEngine API.
    """
    def __init__(self, config_path='logic_config.json'):
        self.engine = LogicEngine(config_path)

    def set_pattern(self, pattern_name: str):
        """Switch your logic panels to a named pattern."""
        self.engine.set_pattern(pattern_name)

    def display_text(self, text: str):
        """Scroll or show text on your logic panel."""
        self.engine.set_text(text)
