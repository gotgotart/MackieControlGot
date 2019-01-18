# uncompyle6 version 3.2.5
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.13 |Continuum Analytics, Inc.| (default, May 11 2017, 13:17:26) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: c:\Jenkins\live\output\win_64_static\Release\python-bundle\MIDI Remote Scripts\MackieControl\MainDisplay.py
# Compiled at: 2018-07-05 14:45:24
from __future__ import absolute_import, print_function, unicode_literals
from .MackieControlComponent import *

class MainDisplay(MackieControlComponent):
    u""" Representing one main 2 row display of a Mackie Control or Extension
    """

    def __init__(self, main_script):
        MackieControlComponent.__init__(self, main_script)
        self.__stack_offset = 0
        self.__last_send_messages = [[], []]

    def destroy(self):
        NUM_CHARS_PER_DISPLAY_LINE = 54
        upper_message = ('Ableton Live').center(NUM_CHARS_PER_DISPLAY_LINE)
        self.send_display_string(upper_message, 0, 0)
        lower_message = ('Device is offline').center(NUM_CHARS_PER_DISPLAY_LINE)
        self.send_display_string(lower_message, 1, 0)
        MackieControlComponent.destroy(self)

    def stack_offset(self):
        return self.__stack_offset

    def set_stack_offset(self, offset):
        u"""This is the offset that one gets by 'stacking' several MackieControl XTs:
           the first is at index 0, the second at 8, etc ...
        """
        self.__stack_offset = offset

    def send_display_string(self, display_string, display_row, cursor_offset):
        if display_row == 0:
            offset = cursor_offset
        else:
            if display_row == 1:
                offset = NUM_CHARS_PER_DISPLAY_LINE + 2 + cursor_offset
            else:
                assert 0
        message_string = [ ord(c) for c in display_string ]
        for i in range(len(message_string)):
            if message_string[i] >= 128:
                message_string[i] = 0

        if self.__last_send_messages[display_row] != message_string:
            self.__last_send_messages[display_row] = message_string
            if self.main_script().is_extension():
                device_type = SYSEX_DEVICE_TYPE_XT
            else:
                device_type = SYSEX_DEVICE_TYPE
            display_sysex = (
             240, 0, 0, 102, device_type, 18, offset) + tuple(message_string) + (247, )
            self.send_midi(display_sysex)

    def refresh_state(self):
        self.__last_send_messages = [[], []]

    def on_update_display_timer(self):
        pass
# okay decompiling MainDisplay.pyc
