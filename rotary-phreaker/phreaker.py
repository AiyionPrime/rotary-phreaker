#!/usr/bin/env python3
import configparser
import sys
import signal

from linphone import Linphone
from pi_device import Pi3Rotary


class Daemon:
    def __init__(self):
        signal.signal(signal.SIGINT, self.on_sigint)

        config = configparser.ConfigParser()
        config.read("samples/config")

        user = config.get("Credentials", "username")
        password = config.get("Credentials", "password")
        host = config.get("Credentials", "hostname")

        self.pi3 = Pi3Rotary(up_cb=self.on_hook_up, down_cb=self.on_hook_down,
                             rotaryplate_not_home_cb=self.rotating, rotaryplate_home_cb=self.home)

        self.linphone = Linphone(user, password, host)

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

    def rotating(self):
        print("The rotaryplate is not in its homeposition.")

    def home(self, n):
        print("The rotaryplate is in its homeposition.")
        if n < 0:
            print("Weird.")
        else:
            print("While it wasnt the number {} was found.".format(str(n)))

    def on_sigint(self):
        self.linphone.__exit__()
        sys.exit(0)

if "__main__" == __name__:
    t = Daemon()
