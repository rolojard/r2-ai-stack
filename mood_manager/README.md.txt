# MoodManager Package

**Purpose**:  
Manages R2’s current “mood” state, updates hardware visuals, and
auto‐resets short‐lived moods like MAD, SCARED, and ALERT.

---

## Files

- `r2_mood_manager.py` — defines `MoodManager` class

---

## Usage

```python
from r2_mood_manager import MoodManager

mm = MoodManager()

# Set mood manually:
mm.set_mood('HAPPY')

# Get current mood:
print(mm.get_mood())  # => 'HAPPY'
