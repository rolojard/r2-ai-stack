# ProfileManager Package

**Purpose**:  
Controls R2’s operational “profiles,” each of which gates features and
can auto‐revert after a timeout.

---

## Files

- `r2_profile_manager.py` — defines `ProfileManager`

---

## Usage

```python
from r2_profile_manager import ProfileManager

pm = ProfileManager()

# Switch to PhotoOp (enables cinematics)
pm.set_profile('PhotoOp')

# Query current profile
print(pm.get_profile())  # → PhotoOp

# Check feature flags
pm.is_attention_enabled()   # → True
pm.is_cinematic_enabled()   # → True
pm.is_quick_mood_enabled()  # → True
