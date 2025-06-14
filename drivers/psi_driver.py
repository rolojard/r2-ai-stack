#!/usr/bin/env python3
import serial, time

class PsiDriver:
    """
    PSIPro v1.7 lights driver via serial.
    """
    def __init__(self, port='/dev/ttyUSB2', baudrate=115200, timeout=0.1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(0.5)

    def set_psi_state(self, index: int, state: bool):
        """
        Example protocol:
        [0xA5][index][0x01/0x00][checksum]
        """
        cmd = bytearray([0xA5, index, 1 if state else 0])
        chk = (sum(cmd) & 0xFF) ^ 0xFF
        cmd.append(chk)
        self.ser.write(cmd)
