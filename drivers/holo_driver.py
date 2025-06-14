#!/usr/bin/env python3
from filthyhp_driver import FilthyHPDriver

class HoloDriver(FilthyHPDriver):
    """Convenience subclass for holo lights."""
    def holo_on(self):
        self.set_holo_brightness(255)

    def holo_off(self):
        self.set_holo_brightness(0)
