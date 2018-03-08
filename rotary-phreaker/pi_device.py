#!/usr/bin/env python3

import RPi.GPIO as GPIO


class Pi3Rotary:
    def __init__(self, up_cb, down_cb):
        self._pins = {"hook": 16,
                      "dialing": 24,
                      "interrupt": 23}
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_onhook, GPIO.IN)
        GPIO.add_event_detect(self._pins["hook"], GPIO.BOTH, callback=self.hook_moved, bouncetime=100)
        self.hook_state = None
        self.hook_up_cb = up_cb
        self.hook_down_cb = down_cb
        self.hook_moved()
        super().__init__()

    def hook_moved(self):
        inp = GPIO.input(self._pins["hook"])
        if inp:
            self.hook_state = 1
            self.hook_up_cb()
        else:
            self.hook_state = 0
            self.hook_down_cb()
