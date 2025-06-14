#!/usr/bin/env python3
"""
ProfileManager:
  Manages R2’s high‐level operating profiles (LargeCon, PhotoOp, KidEvent, Parade, etc.)
  Handles enabled/disabled features per profile and auto‐revert timers.
"""

import time
import threading

class ProfileManager:
    def __init__(self):
        self.current_profile       = 'LargeCon'
        self._lock                 = threading.Lock()
        self._auto_revert_timer    = None
        self._auto_revert_target   = 'LargeCon'

        # Define each profile’s capabilities and optional auto‐revert timeout
        self.profiles = {
            'LargeCon': {
                'attention_enabled': True,
                'cinematic_enabled': False,
                'quick_mood_enabled': True,
                'auto_revert_seconds': None
            },
            'PhotoOp': {
                'attention_enabled': True,
                'cinematic_enabled': True,
                'quick_mood_enabled': True,
                'auto_revert_seconds': None
            },
            'KidEvent': {
                'attention_enabled': True,
                'cinematic_enabled': False,
                'quick_mood_enabled': True,
                'auto_revert_seconds': None
            },
            'Parade': {
                'attention_enabled': False,
                'cinematic_enabled': False,
                'quick_mood_enabled': False,
                'auto_revert_seconds': 20
            },
            'Sleepy': {
                'attention_enabled': False,
                'cinematic_enabled': False,
                'quick_mood_enabled': False,
                'auto_revert_seconds': None
            },
            'Emergency': {
                'attention_enabled': False,
                'cinematic_enabled': False,
                'quick_mood_enabled': False,
                'auto_revert_seconds': None
            }
        }

    def set_profile(self, profile_name: str):
        """Switch to a new profile, cancelling any previous auto‐revert."""
        with self._lock:
            if profile_name not in self.profiles:
                print(f"[ProfileManager] Unknown profile: '{profile_name}'")
                return

            print(f"[ProfileManager] Setting profile → {profile_name}")
            self.current_profile = profile_name

            # Cancel existing auto‐revert
            if self._auto_revert_timer:
                self._auto_revert_timer.cancel()
                self._auto_revert_timer = None

            # Schedule auto‐revert if configured
            secs = self.profiles[profile_name]['auto_revert_seconds']
            if secs:
                print(f"[ProfileManager] Will auto‐revert to '{self._auto_revert_target}' in {secs}s")
                timer = threading.Timer(secs, self._auto_revert)
                timer.daemon = True
                timer.start()
                self._auto_revert_timer = timer

    def _auto_revert(self):
        """Internal: revert back to the default profile."""
        print(f"[ProfileManager] Auto‐reverting to '{self._auto_revert_target}'")
        self.set_profile(self._auto_revert_target)

    def get_profile(self) -> str:
        """Return the name of the current profile."""
        with self._lock:
            return self.current_profile

    def is_attention_enabled(self) -> bool:
        """True if camera‐based attention should run under this profile."""
        return self.profiles[self.get_profile()]['attention_enabled']

    def is_cinematic_enabled(self) -> bool:
        """True if Cinematic sequences are allowed in this profile."""
        return self.profiles[self.get_profile()]['cinematic_enabled']

    def is_quick_mood_enabled(self) -> bool:
        """True if quick_mood events should be executed."""
        return self.profiles[self.get_profile()]['quick_mood_enabled']

    def get_auto_revert_status(self) -> dict:
        """Return whether an auto‐revert timer is active."""
        return {
            'active': bool(self._auto_revert_timer),
            'target': self._auto_revert_target
        }
