#!/usr/bin/env python3

import RPi.GPIO as GPIO


class Pi3Rotary:
    def __init__(self, up_cb, down_cb, rotaryplate_not_home_cb, rotaryplate_home_cb):
        self._pins = {"hook": 16,
                      "dialing": 24,
                      "interrupt": 23}
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_onhook, GPIO.IN)
        GPIO.add_event_detect(self._pins["hook"], GPIO.BOTH, callback=self.hook_moved, bouncetime=100)
        GPIO.add_event_detect(self._pins["dialing"], GPIO.BOTH, callback=self.rotaryplate_not_home, bouncetime=100)

        self.hook_state = None
        self.hook_up_cb = up_cb
        self.hook_down_cb = down_cb
        self.hook_moved()

        self._rot_not_home = None
        self._rot_not_home_cb = rotaryplate_not_home_cb
        self._rot_home_cb = rotaryplate_home_cb
        self.rotaryplate_not_home()

        self._interrupt_counter = 0

        super().__init__()

    def hook_moved(self):
        inp = GPIO.input(self._pins["hook"])
        if inp:
            self.hook_state = 1
            self.hook_up_cb()
        else:
            self.hook_state = 0
            self.hook_down_cb()

    def rotaryplate_not_home(self):
        inp = GPIO.input(self._pins["dialing"])
        if inp:
            self._rot_not_home = 1
            self._rot_not_home_cb()
        else:
            self._rot_not_home = 0
            n = self._digit_from_interrupts()
            self._rot_home_cb(n)

    def _digit_from_interrupts(self, ints=None):
        if ints is None:
            ints = self._interrupt_counter
        if 10 == ints:
            return 0
        elif 0 == ints:
            return -1
        return ints
