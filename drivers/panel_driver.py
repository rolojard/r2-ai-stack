#!/usr/bin/env python3
from pololu_maestro import Maestro

class PanelDriver:
    """
    Driver for Pololu Maestro servo controllers (dome panels).
    """
    def __init__(self, port='/dev/ttyACM0', device_number=1):
        # adjust port and device_number to your setup
        self.maestro = Maestro(port=port, device_number=device_number, baud=57600)
    
    def move_panels(self, mode: str):
        """
        Move your 4 dome + 3 side panels into a preset pose.
        Mode examples: 'neutral','sad','dramatic','panic'
        """
        if mode == 'neutral':
            # channels 0–6 to “home” positions
            for ch, pos in enumerate([6000,6000,6000,6000,6000,6000,6000]):
                self.maestro.set_target(ch, pos)
        elif mode == 'sad':
            for ch, pos in enumerate([5500,5500,5500,5500,5500,5500,5500]):
                self.maestro.set_target(ch, pos)
        elif mode == 'dramatic':
            for ch, pos in enumerate([6500,6500,6500,6500,6500,6500,6500]):
                self.maestro.set_target(ch, pos)
        elif mode == 'panic':
            for ch, pos in enumerate([7000,5000,7000,5000,7000,5000,7000]):
                self.maestro.set_target(ch, pos)
        else:
            print(f"[PanelDriver] Unknown mode '{mode}'")
