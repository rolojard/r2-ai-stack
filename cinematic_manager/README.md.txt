# CinematicManager Package

**Purpose**: Run pre-defined cinematic sequences (sound + panel moves + logic text)  
when triggered by the EventStack or other modules.

## Files

- `r2_cinematic_manager.py`  
  - Contains `CinematicManager` class  
  - Four example sequences:  
    - Leia_Message  
    - Vader_Entrance  
    - Jawa_Panic  
    - Vader_Encounter  

## Usage

```python
from r2_profile_manager import ProfileManager
from r2_cinematic_manager import CinematicManager
from sound_driver import SoundDriver
from panel_driver import PanelDriver

pm = ProfileManager()
sd = SoundDriver('/dev/ttyUSB0')
pd = PanelDriver('/dev/ttyACM0')

cm = CinematicManager(pm, sound_driver=sd, panel_driver=pd)

# Trigger a cinematic
cm.run_cinematic_sequence('Vader_Entrance')
