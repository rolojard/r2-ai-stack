import threading
import time

class AttentionLayer:
    """
    Manages “attention” triggers when R2 spots something interesting.
    """

    def __init__(self, profile_manager, mood_manager):
        self.profile_manager = profile_manager
        self.mood_manager   = mood_manager

        self.attention_active = False
        self.attention_target = None
        self._lock = threading.Lock()
        self._timer = None
        self._duration = 5  # seconds to hold attention

    def trigger_attention(self, source: str, target_info: str):
        """Called by camera thread when a target is seen."""
        with self._lock:
            if not self.profile_manager.is_attention_enabled():
                print(f"[AttentionLayer] Attention disabled in profile → ignoring.")
                return
            if self.attention_active:
                print(f"[AttentionLayer] Already in attention mode → ignoring.")
                return

            print(f"[AttentionLayer] Triggering attention → {source}:{target_info}")
            self.attention_active = True
            self.attention_target = target_info

            # Move R2’s mood to CURIOUS
            self.mood_manager.set_mood("CURIOUS")

            # Start visuals & hardware hooks
            self.activate_attention_visuals()

            # Schedule clear
            self._timer = threading.Timer(self._duration, self.clear_attention)
            self._timer.daemon = True
            self._timer.start()

    def activate_attention_visuals(self):
        """
        Insert your hardware calls here:
         - dome panels move to “look at” target
         - HP / PSI indicators flash
         - logic lights change pattern
        """
        print("[AttentionLayer] Activating attention visuals")

    def clear_attention(self):
        """Clears the attention state and returns R2 to friendly mode."""
        with self._lock:
            print("[AttentionLayer] Clearing attention, returning to normal.")
            self.attention_active = False
            self.attention_target = None

            # Return mood to FRIENDLY
            self.mood_manager.set_mood("FRIENDLY")

            # Turn off visuals
            self.deactivate_attention_visuals()

    def deactivate_attention_visuals(self):
        """
        Insert your hardware calls here to restore default visuals:
         - dome returns to neutral
         - lights return to normal pattern
        """
        print("[AttentionLayer] Deactivating attention visuals")

    def force_clear_attention(self):
        """Immediately cancel attention, used by Force Stop All."""
        with self._lock:
            if self._timer:
                self._timer.cancel()
            if self.attention_active:
                print("[AttentionLayer] Force clearing attention.")
                self.clear_attention()
