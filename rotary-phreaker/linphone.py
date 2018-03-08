#!/usr/bin/env python3

from threading import Thread

from subprocess import Popen, PIPE


class Linphone(Thread):
    def __init__(self, user, password, host):
        super().__init__()
        self.sip_credentials = {"user": user, "password": password, "host": host}
        self._linphone = Popen("linphonec", stdin=PIPE, stdout=PIPE)
        self._cmd("register sip:{}@{} {} {}".format(
            *[self.sip_credentials[x] for x in ["user", "host", "host", "password"]]))

    def __exit__(self, *args):
        self._linphone.terminate()

    def _cmd(self, cmd):
        self._linphone.stdin.write("".join([cmd, '\n']).encode("utf-8"))

    def answer(self):
        self._cmd("answer")
