#!/usr/bin/env python3
"""
MoodManager:
  Tracks R2’s current mood, updates hardware visuals, and auto‐resets
  certain short‐lived moods (MAD, SCARED, ALERT) after a configured timeout.
"""

import time
import threading

class MoodManager:
    def __init__(self):
        self.current_mood = 'NEUTRAL'
        self._lock = threading.Lock()
        self._timestamp = time.time()
        # moods that auto‐reset: {mood_name: seconds}
        self.auto_reset_moods = {
            'MAD':     8,
            'SCARED':  8,
            'ALERT':   5
        }
        # All valid moods
        self.valid_moods = [
            'NEUTRAL', 'HAPPY', 'FRIENDLY', 'CURIOUS',
            'MAD', 'SCARED', 'EXCITED', 'SHY',
            'SLEEPY', 'SAD', 'PROUD', 'ALERT'
        ]

        # Start the background auto‐reset loop
        thread = threading.Thread(target=self._auto_reset_loop, daemon=True)
        thread.start()

    def _auto_reset_loop(self):
        while True:
            time.sleep(1)
            with self._lock:
                if self.current_mood in self.auto_reset_moods:
                    elapsed = time.time() - self._timestamp
                    if elapsed >= self.auto_reset_moods[self.current_mood]:
                        # Reset short‐lived moods to CURIOUS
                        print(f"[MoodManager] Auto‐resetting '{self.current_mood}' → 'CURIOUS'")
                        self._set_mood_internal('CURIOUS')

    def set_mood(self, mood_name: str):
        """Public API: change R2’s mood immediately."""
        with self._lock:
            if mood_name not in self.valid_moods:
                print(f"[MoodManager] Unknown mood: '{mood_name}'")
                return
            self._set_mood_internal(mood_name)

    def _set_mood_internal(self, mood_name: str):
        """Internal helper to avoid duplicate lock code."""
        print(f"[MoodManager] Mood set to '{mood_name}'")
        self.current_mood = mood_name
        self._timestamp = time.time()
        # TODO: insert hardware update hooks here:
        #   self.update_hp_leds(mood_name)
        #   self.update_psi(mood_name)
        #   self.update_logic_display(mood_name)

    def get_mood(self) -> str:
        """Return the current mood."""
        with self._lock:
            return self.current_mood

    # Hardware‐stub methods:

    def update_hp_leds(self, mood_name: str):
        """Hook: update HP LED ring based on mood."""
        pass

    def update_psi(self, mood_name: str):
        """Hook: update PSI lights based on mood."""
        pass

    def update_logic_display(self, mood_name: str):
        """Hook: update logic panel display text/pattern."""
        pass
