#!/usr/bin/env python3
"""
EventStackManager:
  Queues up and processes events in order—mood changes, profiles, cinematics, quick moods.
  Runs in a daemon thread so it never blocks your Flask API.
"""

import time
import threading

class EventStackManager:
    def __init__(self, profile_manager, mood_manager, cinematic_manager):
        self.pm = profile_manager
        self.mm = mood_manager
        self.cm = cinematic_manager

        self._stack = []
        self._lock = threading.Lock()
        self._running = False

    def add_event(self, event_type: str, data: str):
        """Add an event tuple (event_type, data) to the queue."""
        with self._lock:
            print(f"[EventStackManager] Queueing event: {event_type} -> {data}")
            self._stack.append((event_type, data))

    def start(self):
        """Begin processing the stack in a daemon thread."""
        if not self._running:
            print("[EventStackManager] Starting event loop")
            self._running = True
            thread = threading.Thread(target=self._loop, daemon=True)
            thread.start()

    def stop_stack(self):
        """Stop processing and clear pending events."""
        print("[EventStackManager] Stopping and clearing stack")
        self._running = False
        with self._lock:
            self._stack.clear()

    def _loop(self):
        while self._running:
            event = None
            with self._lock:
                if self._stack:
                    event = self._stack.pop(0)

            if event:
                e_type, data = event
                current_profile = self.pm.get_profile()
                print(f"[EventStackManager] Handling event: {e_type} -> {data} (Profile={current_profile})")

                try:
                    if e_type == 'mood':
                        # KidEvent block for MAD/SCARED
                        if current_profile == 'KidEvent' and data in ['MAD', 'SCARED']:
                            data = 'FRIENDLY'
                        self.mm.set_mood(data)

                    elif e_type == 'profile':
                        self.pm.set_profile(data)

                    elif e_type == 'cinematic':
                        if self.pm.is_cinematic_enabled():
                            self.cm.run_cinematic_sequence(data)

                    elif e_type == 'quick_mood':
                        if self.pm.is_quick_mood_enabled():
                            self.mm.set_mood(data)

                    else:
                        print(f"[EventStackManager] Unknown event type: {e_type}")
                except Exception as ex:
                    print(f"[EventStackManager] Error processing {e_type}: {ex}")

                # small delay between events
                time.sleep(0.5)

            else:
                time.sleep(0.1)

    def get_current_stack(self):
        """Return a snapshot list of pending events."""
        with self._lock:
            return [{'event_type': e, 'event_data': d} for e, d in self._stack]
