# uncompyle6 version 3.2.5
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.13 |Continuum Analytics, Inc.| (default, May 11 2017, 13:17:26) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: c:\Jenkins\live\output\win_64_static\Release\python-bundle\MIDI Remote Scripts\MackieControl\MackieControlComponent.py
# Compiled at: 2018-07-05 14:45:24
from __future__ import absolute_import, print_function, unicode_literals
from .consts import *
import Live

class MackieControlComponent:
    u"""Baseclass for every 'sub component' of the Mackie Control. Just offers some """

    def __init__(self, main_script):
        self.__main_script = main_script

    def destroy(self):
        self.__main_script = None
        return

    def main_script(self):
        return self.__main_script

    def shift_is_pressed(self):
        return self.__main_script.shift_is_pressed()

    def option_is_pressed(self):
        return self.__main_script.option_is_pressed()

    def control_is_pressed(self):
        return self.__main_script.control_is_pressed()

    def alt_is_pressed(self):
        return self.__main_script.alt_is_pressed()

    def song(self):
        return self.__main_script.song()

    def script_handle(self):
        return self.__main_script.handle()

    def application(self):
        return self.__main_script.application()

    def send_midi(self, bytes):
        self.__main_script.send_midi(bytes)

    def request_rebuild_midi_map(self):
        self.__main_script.request_rebuild_midi_map()
# okay decompiling MackieControlComponent.pyc
