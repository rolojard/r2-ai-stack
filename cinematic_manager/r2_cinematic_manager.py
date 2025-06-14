#!/usr/bin/env python3
"""
CinematicManager:
  Runs pre-defined “cinematic” sequences (sound + panel movements + logic text)
  when triggered by the event stack or QA module.
"""

class CinematicManager:
    def __init__(self, profile_manager, sound_driver=None, panel_driver=None):
        self.profile_manager = profile_manager
        self.sound_driver    = sound_driver
        self.panel_driver    = panel_driver

        # Pre-approved sequences
        self.allowed_sequences = [
            'Leia_Message',
            'Vader_Entrance',
            'Jawa_Panic',
            'Vader_Encounter'  # custom example
        ]

    def run_cinematic_sequence(self, sequence_name: str):
        """Trigger a cinematic if the current profile allows it."""
        if not self.profile_manager.is_cinematic_enabled():
            print(f"[CinematicManager] Cinematics disabled → skipping '{sequence_name}'")
            return

        if sequence_name not in self.allowed_sequences:
            print(f"[CinematicManager] Unknown sequence: '{sequence_name}'")
            return

        print(f"[CinematicManager] Running sequence: {sequence_name}")

        if sequence_name == 'Leia_Message':
            self._leia_message()
        elif sequence_name == 'Vader_Entrance':
            self._vader_entrance()
        elif sequence_name == 'Jawa_Panic':
            self._jawa_panic()
        elif sequence_name == 'Vader_Encounter':
            self._vader_encounter()

    def _leia_message(self):
        print("[Cinematic] Leia Message")
        if self.sound_driver:
            self.sound_driver.play_mp3('0001_leia_message.mp3')
        if self.panel_driver:
            self.panel_driver.move_panels('scroll')    # example mode
        self.display_logic_text("Leia Organa speaks...")

    def _vader_entrance(self):
        print("[Cinematic] Vader Entrance")
        if self.sound_driver:
            self.sound_driver.play_mp3('0002_vader_entrance.mp3')
        if self.panel_driver:
            self.panel_driver.move_panels('dramatic')
        self.display_logic_text("Darth Vader Approaches")

    def _jawa_panic(self):
        print("[Cinematic] Jawa Panic")
        if self.sound_driver:
            self.sound_driver.play_mp3('0003_jawa_panic.mp3')
        if self.panel_driver:
            self.panel_driver.move_panels('panic')
        self.display_logic_text("Jawa! Jawa!")

    def _vader_encounter(self):
        print("[Cinematic] Vader Encounter")
        if self.sound_driver:
            self.sound_driver.play_mp3('0004_sad_whistle.mp3')
        if self.panel_driver:
            self.panel_driver.move_panels('sad')
        self.display_logic_text("Bow before Vader...")

    def display_logic_text(self, text: str):
        """
        Stub: send a string to your logic-light engine
        """
        print(f"[CinematicManager] Logic display: {text}")
