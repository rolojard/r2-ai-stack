#!/usr/bin/env python3
import serial, time

class SoundDriver:
    """
    Serial sound driver for DFPlayer (or similar).
    """
    def __init__(self, port='/dev/ttyTHS1', baudrate=9600, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)

    def _send(self, pkt: bytes):
        self.ser.write(pkt)
        time.sleep(0.05)

    def play_mp3(self, filename: str):
        idx = int(filename.split('/')[-1][:4])
        hi, lo = (idx>>8)&0xFF, idx&0xFF
        pkt = bytearray([0x7E,0xFF,0x06,0x03,0x00,hi,lo,0x00,0x00,0xEF])
        chk = 0xFFFF - sum(pkt[1:7]) + 1
        pkt[7], pkt[8] = (chk>>8)&0xFF, chk&0xFF
        self._send(pkt)

    def set_volume(self, level:int):
        level = max(0,min(30,level))
        pkt = bytearray([0x7E,0xFF,0x06,0x06,0x00,0x00,level,0x00,0x00,0xEF])
        chk = 0xFFFF - sum(pkt[1:7]) + 1
        pkt[7], pkt[8] = (chk>>8)&0xFF, chk&0xFF
        self._send(pkt)

    def stop(self):
        pkt = bytearray([0x7E,0xFF,0x06,0x16,0x00,0x00,0x00,0x00,0x00,0xEF])
        chk = 0xFFFF - sum(pkt[1:7]) + 1
        pkt[7], pkt[8] = (chk>>8)&0xFF, chk&0xFF
        self._send(pkt)
