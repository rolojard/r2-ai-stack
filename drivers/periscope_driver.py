#!/usr/bin/env python3
from filthyhp_driver import FilthyHPDriver

class PeriscopeDriver(FilthyHPDriver):
    """Convenience subclass for periscope only."""
    def raise_periscope(self):
        self.set_periscope_height(100)   # mm

    def lower_periscope(self):
        self.set_periscope_height(0)
