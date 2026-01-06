import os
import numpy as np
from scipy.io.wavfile import write


class MusicAgent:
    def __init__(self, mode="guided", params=None, prompt=None):
        self.mode = mode
        self.params = params or {}
        self.prompt = prompt or ""

    def run(self):
        print("Gerando áudio...")

        if not os.path.exists("storage"):
            os.makedirs("storage")

        duration = self.params.get("duration", 5)
        sr = 44100

        t = np.linspace(0, duration, int(sr * duration), endpoint=False)
        audio = 0.5 * np.sin(2 * np.pi * 440 * t)
        audio = np.stack([audio, audio], axis=1)

        path = "storage/music_001.wav"
        write(path, sr, (audio * 32767).astype(np.int16))

        return os.path.basename(path)
