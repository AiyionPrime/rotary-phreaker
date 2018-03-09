#!/usr/bin/env python3

from threading import Thread

from subprocess import Popen, PIPE


class Linphone(Thread):
    def __init__(self, user, password, host, inc_cb, r_hu_cb, hu_cb):
        super().__init__()
        self._run = True
        self.sip_credentials = {"user": user, "password": password, "host": host}
        self._linphone = Popen("linphonec", stdin=PIPE, stdout=PIPE)
        self._cmd("register sip:{}@{} {} {}".format(
            *[self.sip_credentials[x] for x in ["user", "host", "host", "password"]]))
        self.incoming_cb = inc_cb
        self.remote_hang_up_cb = r_hu_cb
        self.hang_up_cb = hu_cb

    def __exit__(self, *args):
        self._run = False
        self._linphone.terminate()

    def _cmd(self, cmd):
        self._linphone.stdin.write("".join([cmd, '\n']).encode("utf-8"))

    def answer(self):
        self._cmd("answer")

    def call(self, telephone_number):
        self._cmd("call sip:{}@{}".format(telephone_number, self.sip_credentials["host"]))

    def hang_up(self):
        self._cmd("terminate")

    def run(self):
        while self._run:
            output = self._linphone.stdout.readline().rstrip()
            if "contacting you" in output:
                self.incoming_cb()
            elif "terminated" in output:
                self.remote_hang_up_cb()
            elif "ended" in output:
                self.hang_up_cb()
