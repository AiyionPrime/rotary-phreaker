#!/usr/bin/env python3
import sys

import signal
from linphone import Linphone


class Daemon:
    def __init__(self):
        signal.signal(signal.SIGINT, self.on_sigint)

        # todo read config

        self.linphone = Linphone()

        # start thread
        self.linphone.start()

    def on_hook_up(self):
        pass

    def on_hook_down(self):
        pass

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
