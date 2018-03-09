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

        self.linphone = Linphone(user, password, host,
                                 inc_cb=self.on_incoming_call,
                                 hu_cb=self.on_self_hung_up,
                                 r_hu_cb=self.on_other_hung_up)
        self.cur_number = ""

        # start thread
        self.linphone.start()

    def on_hook_up(self):
        print("Hook got lifted.")
        self.linphone.answer()

    def on_hook_down(self):
        print("Hook was put down.")
        self.cur_number = ""
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
            print("Weird. Resetting.")
            self.cur_number = ""
        else:
            s_n = str(n)
            print("While it wasnt the digit {} was found.".format(s_n))
            self.cur_number += s_n
            print("therefore the current dial number is: {}".format(self.cur_number))
            # todo how to know if a number is completed?
            # hopefully there's another way than timeouting after a few seconds without dial?!
            # seems like one simply calls the unfinished number and watches out for upcoming errors
            # like "484 Address Incomplete"

    def on_sigint(self):
        self.linphone.__exit__()
        sys.exit(0)

if "__main__" == __name__:
    t = Daemon()
