#!/usr/bin/env python3
import serial, time

class FilthyHPDriver:
    """
    Serial driver for FLthyHP-based boards (periscope lifter, spinner, holo lights).
    """
    def __init__(self, port='/dev/ttyUSB1', baudrate=115200, timeout=0.1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(1)

    def send_command(self, cmd: bytes):
        """Low‐level write."""
        self.ser.write(cmd)

    def set_periscope_height(self, mm: int):
        """
        Example protocol (adjust to your sketch):
        [0xAA][0x01][height_hi][height_lo][0x55]
        """
        hi = (mm >> 8) & 0xFF
        lo = mm & 0xFF
        packet = bytes([0xAA,0x01,hi,lo,0x55])
        self.send_command(packet)

    def spin_periscope(self, rpm: int):
        hi = (rpm >> 8) & 0xFF
        lo = rpm & 0xFF
        packet = bytes([0xAA,0x02,hi,lo,0x55])
        self.send_command(packet)

    def set_holo_brightness(self, level: int):
        """0–255 brightness."""
        packet = bytes([0xAA,0x03,level & 0xFF,0x00,0x55])
        self.send_command(packet)
