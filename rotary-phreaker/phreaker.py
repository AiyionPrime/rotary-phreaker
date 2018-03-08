#!/usr/bin/env python3
import sys

import signal
from linphone import Linphone
from pi_device import Pi3Rotary


class Daemon:
    def __init__(self):
        signal.signal(signal.SIGINT, self.on_sigint)

        # todo read config
        self.pi3 = Pi3Rotary(up_cb=self.on_hook_up, down_cb=self.on_hook_down)

        self.linphone = Linphone("samus", "secretpasscode", "Gunship")

        # start thread
        self.linphone.start()

    def on_hook_up(self):
        print("Hook got lifted.")
        self.linphone.answer()

    def on_hook_down(self):
        print("Hook was put down.")
        self.linphone.hang_up()

    def on_incoming_call(self):
        pass

    def on_outgoing_call(self):
        pass

    def on_self_hung_up(self):
        pass

    def on_other_hung_up(self):
        pass

    def on_sigint(self):
        self.linphone.__exit__()
        sys.exit(0)

if "__main__" == __name__:
    t = Daemon()
