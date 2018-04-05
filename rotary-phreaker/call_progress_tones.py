#!/usr/bin/env python3

import pyaudio
import numpy as np
from abc import ABC, abstractmethod

from threading import Thread


class Noise(ABC):
    @abstractmethod
    def __init__(self):
        self.fs = 44100  # sampling rate, Hz, must be integer
        self.samples = None

    def play(self):
        p = pyaudio.PyAudio()

        # for paFloat32 sample values must be in range [-1.0, 1.0]
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=self.fs,
                        output=True)

        # play. May repeat with different volume values (if done interactively)
        stream.write(self.samples.tobytes())

        stream.stop_stream()
        stream.close()

        p.terminate()


class Tone(Noise):
    def __init__(self, frequency, duration, volume):
        super().__init__()
        self.frequency = frequency
        self.duration = duration
        self.volume = volume
        self.samples = self.gen_samples()

    def __add__(self, other):
        t = Tone(self.frequency, self.duration, self.volume)
        t.samples += other.samples
        return t

    def gen_samples(self):
        # generate samples, note conversion to float32 array
        return (np.sin(2 * np.pi * np.arange(self.fs * self.duration)
                       * self.frequency / self.fs)).astype(np.float32) * self.volume


class CosTone(Tone):
    def __init__(self, frequency, duration, volume):
        super().__init__(frequency, duration, volume)

    def gen_samples(self):
        # generate samples, note conversion to float32 array
        return (np.cos(2 * np.pi * np.arange(self.fs * self.duration)
                       * self.frequency / self.fs)).astype(np.float32) * self.volume


class Silence(Tone):
    def __init__(self, duration):
        super().__init__(0, duration, 0)


class CallProgressTone(ABC, Thread):
    """Represent an abstract skeleton for call progress tones.

    Follow the definition in the
    "Technische Beschreibung der analogen Wählanschlüsse am T-Net/ISDN der T-Com (1TR110-1)"."""
    @abstractmethod
    def __init__(self, new_patterns):
        super().__init__()
        self.patterns = new_patterns
        self._run = True

    def __exit__(self, *args):
        self._run = False

    def _first(self):
        res = []
        for tone in self.patterns[0]:
            res.append(tone.samples)
        return res

    def _second(self):
        res = []
        for tone in self.patterns[-1]:
            res.append(tone.samples)
        return res

    def play_endlessly(self):
        p = pyaudio.PyAudio()
        fs = 44100  # sampling rate, Hz, must be integer
        #  for paFloat32 sample values must be in range [-1.0, 1.0]
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=fs,
                        output=True)

        fl = self._first()
        sl = self._second()

        for sample in fl:
            stream.write(sample.tobytes())

        while self._run:
            for sample in sl:
                stream.write(sample.tobytes())

        stream.stop_stream()
        stream.close()

        p.terminate()


class Waehlton(CallProgressTone):
    """1 TR 110-1, Kap. 8.1"""
    def __init__(self):
        super().__init__([[Tone(425, 1, 1.0)]])


class Sonderwaehlton(CallProgressTone):
    """1 TR 110-1, Kap. 8.2"""
    def __init__(self):
        super().__init__([[Tone(425, 1, 1.0) + Tone(400, 1, 1.0)]])


class Freiton(CallProgressTone):
    """1 TR 110-1, Kap. 8.3"""
    def __init__(self):
        super().__init__([[Tone(425, 1, 1.0), Silence(4)]])


class Teilnehmerbesetztton(CallProgressTone):
    """1 TR 110-1, Kap. 8.4"""
    def __init__(self):
        super().__init__([[Tone(425, 0.48, 1.0), Silence(0.48)]])


class Gassenbesetztton(CallProgressTone):
    """1 TR 110-1, Kap. 8.5"""
    def __init__(self):
        super().__init__([[Tone(425, 0.24, 1.0), Silence(0.24)]])


class Aufschaltzeichen(CallProgressTone):
    """1 TR 110-1, Kap. 8.6"""
    def __init__(self):
        super().__init__([[Tone(425, 0.24, 1.0), Silence(0.24), Tone(425, 0.24, 1.0), Silence(1.28)]])


class Anklopfton(CallProgressTone):
    """1 TR 110-1, Kap. 8.7"""
    def __init__(self):
        super().__init__([[Tone(425, 0.2, 1.0), Silence(0.2), Tone(425, 0.2, 1.0), Silence(1)],
                          [Tone(425, 0.2, 1.0), Silence(0.2), Tone(425, 0.2, 1.0), Silence(5)]])


class Hinweiston(CallProgressTone):
    """1 TR 110-1, Kap. 8.8"""
    def __init__(self):
        super().__init__([[Tone(950, 0.33, 0.3), Tone(1400, 0.33, 0.3), Tone(1800, 0.33, 0.3), Silence(1)]])


class Suchton1(CallProgressTone):
    """1 TR 110-1, Kap. 8.9 """
    def __init__(self):
        super().__init__([[Tone(800, 1, 1.0)]])


class Suchton2(CallProgressTone):
    """1 TR 110-1, Kap. 8.9 """
    def __init__(self):
        super().__init__([[Tone(1100, 1, 1.0) + Tone(1200, 1, 1.0)]])


class DisablingTon(CallProgressTone):
    """1 TR 110-1, Kap. 8.9 """
    def __init__(self):
        super().__init__([[Tone(2100, 0.45, 1.0),
                           CosTone(2100, 0.45, 1.0),
                           Tone(2100, 0.45, 1.0),
                           CosTone(2100, 0.45, 1.0),
                           Tone(2100, 0.45, 1.0),
                           CosTone(2100, 0.45, 1.0),
                           Tone(2100, 0.45, 1.0),
                           CosTone(2100, 0.45, 1.0),
                           Tone(2100, 0.4, 1.0)], [Silence(1)]])
