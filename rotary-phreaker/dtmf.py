#!/usr/bin/env python3

from call_progress_tones import Noise, Tone


class DTMFTone(Noise):
    """Represents the tones used for dtmf."""
    def __init__(self, char, duration, volume):
        super().__init__()
        f1, f2 = DTMFTone.get_frequencies(char)
        # in order to avoid clipping, the volume gets divided in half
        t1 = Tone(f1, duration, volume/2)
        t2 = Tone(f2, duration, volume/2)

        self.samples = (t1 + t2).samples

    @staticmethod
    def get_frequencies(character):
        # high frequency component
        hfc = (1209, 1336, 1477, 1633)
        # low frequency component
        lfc = (697, 770, 852, 941)

        # a telephone keypad containing the widely unused keys A, B, C and D.
        keys = ("1", "2", "3", "A",
                "4", "5", "6", "B",
                "7", "8", "9", "C",
                "*", "0", "#", "D")
        return lfc[keys.index(character) // 4], hfc[keys.index(character) % 4]
