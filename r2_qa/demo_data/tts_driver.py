#!/usr/bin/env python3
"""
TTSDriver:
  Uses gTTS to generate an MP3 from a text string
  and then plays it via your SoundDriver.
"""

import os, uuid
from gtts import gTTS
from sound_driver import SoundDriver  # assume exists in PYTHONPATH

class TTSDriver:
    def __init__(self, out_dir: str = "tts_outputs"):
        os.makedirs(out_dir, exist_ok=True)
        self.out_dir = out_dir
        self.sound_driver = SoundDriver()

    def speak(self, text: str):
        """Generate TTS MP3 and play it on your sound hardware."""
        filename = os.path.join(self.out_dir, f"{uuid.uuid4()}.mp3")
        gTTS(text=text, lang="en").save(filename)
        # send file to DFPlayer via SoundDriver
        self.sound_driver.play_mp3(filename)
