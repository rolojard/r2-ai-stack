# EventStackManager Package

**Purpose**: Queue and handle asynchronous events in a safe, FIFO order.

## Files

- `r2_event_stack_manager.py`  
  - Class `EventStackManager`  
  - Call `add_event(type, data)` to schedule actions  
  - Supported event types:
    - `mood`
    - `profile`
    - `cinematic`
    - `quick_mood`

## Usage

```python
from r2_profile_manager import ProfileManager
from r2_mood_manager    import MoodManager
from r2_cinematic_manager import CinematicManager
from r2_event_stack_manager import EventStackManager

pm = ProfileManager()
mm = MoodManager()
cm = CinematicManager(pm)
esm = EventStackManager(pm, mm, cm)

esm.start()
esm.add_event('mood', 'HAPPY')
esm.add_event('cinematic', 'Leia_Message')
