#!/usr/bin/env python3
import serial, time

class HcrDriver:
    """
    Serial interface to the HumanCyborgRelations vocalizer.
    """
    def __init__(self, port='/dev/ttyUSB3', baudrate=115200, timeout=0.1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(1)

    def send_text(self, text: str):
        """
        Send a text packet—your sketch decides how to parse and speak.
        """
        data = text.encode('utf-8') + b'\n'
        self.ser.write(data)
