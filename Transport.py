# uncompyle6 version 3.2.5
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.1 |Continuum Analytics, Inc.| (default, May 11 2017, 13:25:24) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: c:\Jenkins\live\output\win_64_static\Release\python-bundle\MIDI Remote Scripts\MackieControl\Transport.py
# Compiled at: 2018-07-05 14:45:24
from __future__ import absolute_import, print_function, unicode_literals
from .MackieControlComponent import *
import datetime
got_log_file='c:/temp/ableton_mackie.log'
got_debug=True
#import pprint
#import inspect
#import sys
#import json
import time

import inspect
 
def line_numb():
    '''Returns the current line number in our program'''
    return inspect.currentframe().f_back.f_lineno

def got_log(got_line_numb,got_log_str):
    if got_debug:
        with open(got_log_file, 'a+') as f:
            print('{} | line {} | {}'.format(datetime.datetime.now(),got_line_numb,got_log_str), file=f)

class Transport(MackieControlComponent):
    """Representing the transport section of the Mackie Control: """

    def __init__(self, main_script):
        MackieControlComponent.__init__(self, main_script)
        self.__forward_button_down = False
        self.____rewind_button_down = False
        self.__zoom_button_down = False
        self.__scrub_button_down = False
        self.__cursor_left_is_down = False
        self.__cursor_right_is_down = False
        self.__cursor_up_is_down = False
        self.__cursor_down_is_down = False
        self.__cursor_repeat_delay = 0
        self.__transport_repeat_delay = 0
        self.____fast_forward_counter = 0
        self.__fast___rewind_counter = 0
        self.__jog_step_count_forward = 0
        self.__jog_step_count_backwards = 0
        self.__last_focussed_clip_play_state = CLIP_STATE_INVALID
        self.song().add_record_mode_listener(self.__update_record_button_led)
        self.song().add_is_playing_listener(self.__update_play_button_led)
        self.song().add_loop_listener(self.__update_loop_button_led)
        self.song().add_punch_out_listener(self.__update_punch_out_button_led)
        self.song().add_punch_in_listener(self.__update_punch_in_button_led)
        self.song().add_can_jump_to_prev_cue_listener(self.__update_prev_cue_button_led)
        self.song().add_can_jump_to_next_cue_listener(self.__update_next_cue_button_led)
        self.application().view.add_is_view_visible_listener(b'Session', self.__on_session_is_visible_changed)
        self.refresh_state()

    def destroy(self):
        self.song().remove_record_mode_listener(self.__update_record_button_led)
        self.song().remove_is_playing_listener(self.__update_play_button_led)
        self.song().remove_loop_listener(self.__update_loop_button_led)
        self.song().remove_punch_out_listener(self.__update_punch_out_button_led)
        self.song().remove_punch_in_listener(self.__update_punch_in_button_led)
        self.song().remove_can_jump_to_prev_cue_listener(self.__update_prev_cue_button_led)
        self.song().remove_can_jump_to_next_cue_listener(self.__update_next_cue_button_led)
        self.application().view.remove_is_view_visible_listener(b'Session', self.__on_session_is_visible_changed)
        for note in transport_control_switch_ids:
            self.send_midi((NOTE_ON_STATUS, note, BUTTON_STATE_OFF))

        for note in jog_wheel_switch_ids:
            self.send_midi((NOTE_ON_STATUS, note, BUTTON_STATE_OFF))

        for note in marker_control_switch_ids:
            self.send_midi((NOTE_ON_STATUS, note, BUTTON_STATE_OFF))

        MackieControlComponent.destroy(self)

    def refresh_state(self):
        self.__update_play_button_led()
        self.__update_record_button_led()
        self.__update_prev_cue_button_led()
        self.__update_next_cue_button_led()
        self.__update_loop_button_led()
        self.__update_punch_in_button_led()
        self.__update_punch_out_button_led()
        self.__forward_button_down = False
        self.____rewind_button_down = False
        self.__zoom_button_down = False
        self.__scrub_button_down = False
        self.__cursor_left_is_down = False
        self.__cursor_right_is_down = False
        self.__cursor_up_is_down = False
        self.__cursor_down_is_down = False
        self.__cursor_repeat_delay = 0
        self.__transport_repeat_delay = 0
        self.____fast_forward_counter = 0
        self.__fast___rewind_counter = 0
        self.__jog_step_count_forward = 0
        self.__jog_step_count_backwards = 0
        self.__last_focussed_clip_play_state = CLIP_STATE_INVALID
        self.__update_forward_rewind_leds()
        self.__update_zoom_button_led()
        self.__update_scrub_button_led()

    def session_is_visible(self):
        return self.application().view.is_view_visible(b'Session')

    def selected_clip_slot(self):
        return self.song().view.highlighted_clip_slot

    def on_update_display_timer(self):
        if self.__transport_repeat_delay > 2:
            if self.alt_is_pressed():
                base_acceleration = 1
            else:
                base_acceleration = self.song().signature_numerator
            if self.song().is_playing:
                base_acceleration *= 4
            if not (self.__forward_button_down and self.____rewind_button_down):
                if self.__forward_button_down:
                    self.____fast_forward_counter += 1
                    self.__fast___rewind_counter -= 4
                    if not self.alt_is_pressed():
                        self.__fast_forward(base_acceleration + max(1, self.____fast_forward_counter / 4))
                    else:
                        self.__fast_forward(base_acceleration)
                if self.____rewind_button_down:
                    self.__fast___rewind_counter += 1
                    self.____fast_forward_counter -= 4
                    if not self.alt_is_pressed():
                        self.__rewind(base_acceleration + max(1, self.__fast___rewind_counter / 4))
                    else:
                        self.__rewind(base_acceleration)
        else:
            self.__transport_repeat_delay += 1
        if self.__cursor_repeat_delay > 2:
            if self.__cursor_left_is_down:
                self.__on_cursor_left_pressed()
            if self.__cursor_right_is_down:
                self.__on_cursor_right_pressed()
            if self.__cursor_up_is_down:
                self.__on_cursor_up_pressed()
            if self.__cursor_down_is_down:
                self.__on_cursor_down_pressed()
        else:
            self.__cursor_repeat_delay += 1
        if self.session_is_visible():
            self.__update_zoom_led_in_session()

    def handle_marker_switch_ids(self, switch_id, value):
        got_log(line_numb(),'switch_id : {}'.format(switch_id))
        if switch_id == SID_MARKER_FROM_PREV:
            if value == BUTTON_PRESSED:
                self.__jump_to_prev_cue()
        else:
            if switch_id == SID_MARKER_FROM_NEXT:
                if value == BUTTON_PRESSED:
                    self.__jump_to_next_cue()
            else:
                if switch_id == SID_MARKER_LOOP:
                    if value == BUTTON_PRESSED:
                        self.__toggle_loop()
                else:
                    if switch_id == SID_MARKER_PI:
                        if value == BUTTON_PRESSED:
                            if self.control_is_pressed():
                                self.__set_loopstart_from_cur_position()
                            else:
                                self.__toggle_punch_in()
                    else:
                        if switch_id == SID_MARKER_PO:
                            if value == BUTTON_PRESSED:
                                if self.control_is_pressed():
                                    self.__set_loopend_from_cur_position()
                                else:
                                    self.__toggle_punch_out()
                        else:
                            if switch_id == SID_MARKER_HOME:
                                if value == BUTTON_PRESSED:
                                    self.__goto_home()
                            else:
                                if switch_id == SID_MARKER_END:
                                    if value == BUTTON_PRESSED:
                                        self.__goto_end()

    def handle_transport_switch_ids(self, switch_id, value):
        if switch_id == SID_TRANSPORT_REWIND:
            if value == BUTTON_PRESSED:
                self.__rewind()
                self.____rewind_button_down = True
            else:
                if value == BUTTON_RELEASED:
                    self.____rewind_button_down = False
                    self.__fast___rewind_counter = 0
            self.__update_forward_rewind_leds()
        else:
            if switch_id == SID_TRANSPORT_FAST_FORWARD:
                if value == BUTTON_PRESSED:
                    self.__fast_forward()
                    self.__forward_button_down = True
                else:
                    if value == BUTTON_RELEASED:
                        self.__forward_button_down = False
                        self.____fast_forward_counter = 0
                self.__update_forward_rewind_leds()
            else:
                if switch_id == SID_TRANSPORT_STOP:
                    if value == BUTTON_PRESSED:
                        self.__stop_song()
                else:
                    if switch_id == SID_TRANSPORT_PLAY:
                        if value == BUTTON_PRESSED:
                            self.__start_song()
                    else:
                        if switch_id == SID_TRANSPORT_RECORD:
                            if value == BUTTON_PRESSED:
                                self.__toggle_record()

    def handle_jog_wheel_rotation(self, value):
        got_log(line_numb(),'jog wheel rotation value : {}'.format(value))
        backwards = value >= 64
        if self.control_is_pressed():
            if self.alt_is_pressed():
                step = 0.1
            else:
                step = 1.0
            if backwards:
                amount = -(value - 64)
            else:
                amount = value
            tempo = max(20, min(999, self.song().tempo + amount * step))
            self.song().tempo = tempo
        else:
            if self.session_is_visible():
                if backwards:
                    amount = -(value - 64)
                else:
                    amount = value
            

                self.__got_move_loop(amount,"beat")
            else:
                if backwards:
                    step = max(1.0, (value - 64) / 2.0)
                else:
                    step = max(1.0, value / 2.0)
                if self.song().is_playing:
                    step *= 4.0
                if self.alt_is_pressed():
                    step /= 4.0
                if self.__scrub_button_down:
                    if backwards:
                        self.song().scrub_by(-step)
                    else:
                        self.song().scrub_by(step)
                else:
                    if backwards:
                        self.song().jump_by(-step)
                    else:
                        self.song().jump_by(step)

    def handle_jog_wheel_switch_ids(self, switch_id, value):
        if switch_id == SID_JOG_CURSOR_UP:
            if value == BUTTON_PRESSED:
                self.__cursor_up_is_down = True
                self.__cursor_repeat_delay = 0
                self.__on_cursor_up_pressed()
            elif value == BUTTON_RELEASED:
                self.__cursor_up_is_down = False
        else:
            if switch_id == SID_JOG_CURSOR_DOWN:
                if value == BUTTON_PRESSED:
                    self.__cursor_down_is_down = True
                    self.__cursor_repeat_delay = 0
                    self.__on_cursor_down_pressed()
                elif value == BUTTON_RELEASED:
                    self.__cursor_down_is_down = False
            else:
                if switch_id == SID_JOG_CURSOR_LEFT:
                    if value == BUTTON_PRESSED:
                        self.__cursor_left_is_down = True
                        self.__cursor_repeat_delay = 0
                        self.__on_cursor_left_pressed()
                    elif value == BUTTON_RELEASED:
                        self.__cursor_left_is_down = False
                else:
                    if switch_id == SID_JOG_CURSOR_RIGHT:
                        if value == BUTTON_PRESSED:
                            self.__cursor_right_is_down = True
                            self.__cursor_repeat_delay = 0
                            self.__on_cursor_right_pressed()
                        elif value == BUTTON_RELEASED:
                            self.__cursor_right_is_down = False
                    else:
                        if switch_id == SID_JOG_ZOOM:
                            if value == BUTTON_PRESSED:
                                if self.session_is_visible():
                                    if self.selected_clip_slot():
                                        if self.alt_is_pressed():
                                            self.selected_clip_slot().has_stop_button = not self.selected_clip_slot().has_stop_button
                                        elif self.option_is_pressed():
                                            self.selected_clip_slot().stop()
                                        else:
                                            self.selected_clip_slot().fire()
                                else:
                                    self.__zoom_button_down = not self.__zoom_button_down
                                    self.__update_zoom_button_led()
                        else:
                            if switch_id == SID_JOG_SCRUB:
                                if value == BUTTON_PRESSED:
                                    if self.session_is_visible():
                                        if self.option_is_pressed():
                                            self.song().stop_all_clips()
                                        else:
                                            self.song().view.selected_scene.fire_as_selected()
                                    else:
                                        self.__scrub_button_down = not self.__scrub_button_down
                                        self.__update_scrub_button_led()

    def __on_cursor_up_pressed(self):
        nav = Live.Application.Application.View.NavDirection
        if self.__zoom_button_down:
            self.application().view.zoom_view(nav.up, b'', self.alt_is_pressed())
        else:
            self.application().view.scroll_view(nav.up, b'', self.alt_is_pressed())

    def __on_cursor_down_pressed(self):
        nav = Live.Application.Application.View.NavDirection
        if self.__zoom_button_down:
            self.application().view.zoom_view(nav.down, b'', self.alt_is_pressed())
        else:
            self.application().view.scroll_view(nav.down, b'', self.alt_is_pressed())

    def __on_cursor_left_pressed(self):
        nav = Live.Application.Application.View.NavDirection
        if self.__zoom_button_down:
            self.application().view.zoom_view(nav.left, b'', self.alt_is_pressed())
        else:
            self.application().view.scroll_view(nav.left, b'', self.alt_is_pressed())

    def __on_cursor_right_pressed(self):
        nav = Live.Application.Application.View.NavDirection
        if self.__zoom_button_down:
            self.application().view.zoom_view(nav.right, b'', self.alt_is_pressed())
        else:
            self.application().view.scroll_view(nav.right, b'', self.alt_is_pressed())

    def __toggle_record(self):        
        # if session is recording, set and activate loop, and stop recording
        if ( self.song().session_record ):
            for got_track in self.song().tracks:
                if got_track.arm==True:
                    got_clip_slot_id=got_track.playing_slot_index
                    got_log(line_numb(),'got_clip_slot_id : {}'.format(got_clip_slot_id))
                    if got_clip_slot_id!=-1:
                        got_clip_slot=got_track.clip_slots[got_clip_slot_id]
                        if got_clip_slot.clip:
                            got_clip=got_clip_slot.clip
                            
                            got_loop_length=got_clip.signature_numerator*got_clip.signature_denominator
                            got_log(line_numb(),'got_clip.signature_numerator*got_clip.signature_denominator : {}'.format(got_loop_length))                                
                            # set the loop length to the previous clip loop length if available
                            # else it will be the signature numerator ( see previous statement )
                            if got_track.clip_slots[got_clip_slot_id-1]:
                                if got_track.clip_slots[got_clip_slot_id-1].clip:
                                    if got_track.clip_slots[got_clip_slot_id-1].clip.looping:
                                        got_loop_length=got_track.clip_slots[got_clip_slot_id-1].clip.loop_end-got_track.clip_slots[got_clip_slot_id-1].clip.loop_start
                                        got_log(line_numb(),'previous clip start,stop are : {},{} done'.format(got_track.clip_slots[got_clip_slot_id-1].clip.loop_start,got_track.clip_slots[got_clip_slot_id-1].clip.loop_end))
                                    else:
                                        got_log(line_numb(),'previous clip is not looping')
                                else:
                                    got_log(line_numb(),'previous clip slot has no clip')
                            else:
                                got_log(line_numb(),'there is no previous clip slot')
                            # the new loop start/end will be the previous loop that have been recorded
                            got_position=got_clip.playing_position
                            got_log(line_numb(),'got_position : {} done'.format(got_position))
                            got_clip_new_loop_start=(got_position//got_loop_length-1)*got_loop_length
                            got_clip_new_loop_end=(got_position//got_loop_length)*got_loop_length
                            
                            # in case there was no previous loop ( stop record pressed before the loop length )
                            if got_clip_new_loop_start<0:
                                got_clip_new_loop_start=0
                                got_clip_new_loop_end=got_loop_length
                            
                            got_log(line_numb(),'clip start,stop will be : {},{} done'.format(got_clip_new_loop_start,got_clip_new_loop_end))
                            
                            got_clip.looping=True    
                            got_clip.position=got_clip_new_loop_start
                            got_clip.start_marker=got_clip.position
                            got_clip.loop_end=got_clip_new_loop_end
                            
                            
            # stop recording session                
            self.song().session_record = not self.song().session_record

        got_clip_slot_to_show=None
        if ( not self.song().session_record ):
            for got_track in self.song().tracks:
                if got_track.arm==True:
                    # find the last clip slot of the track that already has a clip
                    got_last_clip_stop_with_clip_id=-1
                    for i,got_clip_slot in enumerate(got_track.clip_slots):
                        got_last_clip_slot_id=i
                        if got_clip_slot.has_clip:
                            got_last_clip_stop_with_clip_id=i

                    # start recording the next clip slot
                    got_track.clip_slots[got_last_clip_stop_with_clip_id+1].set_fire_button_state(True)
                    # show this clip
                    self.song().view.highlighted_clip_slot=got_track.clip_slots[got_last_clip_stop_with_clip_id+1]


    def __got_move_loop(self,got_amount,got_unit):

        if self.session_is_visible():

        

            clip_slot = self.selected_clip_slot()
            if clip_slot and clip_slot.clip:
                got_clip=clip_slot.clip
                got_increment=0
                
                if ( got_unit == "beat" ):
                    got_increment=got_clip.signature_denominator
                if ( got_unit == "loop" ):
                    if got_clip.looping:
                        got_increment=got_clip.loop_end-got_clip.loop_start
                    else:
                        got_increment=got_clip.signature_denominator*got_clip.signature_numerator
                if ( got_unit == "bar" ):
                    got_increment=got_clip.signature_denominator*got_clip.signature_numerator
                    
                if got_clip.looping:
                    got_clip.position=got_clip.position+got_increment*got_amount
                    got_clip.start_marker=got_clip.position
                    
                else:
                    got_clip.looping=True
                    got_clip.position=got_clip.position+got_increment*got_amount
                    got_clip.looping=False
                    got_clip.start_marker=got_clip.start_marker+got_increment*got_amount
                    # the order in which we move the start stop marker depends on the direction
                    # because if we move the start marker forward first, it may get behind the
                    # end marker, which will cause an error
                    #got_log(line_numb(),'end_marker is {}'.format(got_clip.end_marker))
                    #got_log(line_numb(),'got_increment*got_amount is {}'.format(got_increment*got_amount))
                    #got_log(line_numb(),'end_time is {}'.format(got_clip.end_time))
                    #if got_amount<0:
                    #    got_clip.start_marker=got_clip.start_marker+got_increment*got_amount
                    #    got_clip.end_marker=got_clip.end_marker+got_increment*got_amount
                    #else:
                    #    got_clip.end_marker=got_clip.end_marker+got_increment*got_amount
                    #    got_clip.start_marker=got_clip.start_marker+got_increment*got_amount
    
    
    def __rewind(self, acceleration=1):
        beats = acceleration
        self.song().jump_by(-beats)

    def __fast_forward(self, acceleration=1):
        beats = acceleration
        self.song().jump_by(beats)

    def __stop_song(self):
        self.song().stop_playing()

    def __start_song(self):
        if self.shift_is_pressed():
            if not self.song().is_playing:
                self.song().continue_playing()
            else:
                self.song().stop_playing()
        else:
            if self.control_is_pressed():
                self.song().play_selection()
            else:
                self.song().start_playing()

    def __toggle_follow(self):
        self.song().follow_song = not self.song().follow_song

    def __toggle_loop(self):
        self.song().loop = not self.song().loop

    def __toggle_punch_in(self):
        self.song().punch_in = not self.song().punch_in

    def __toggle_punch_out(self):
        self.song().punch_out = not self.song().punch_out

    def __jump_to_prev_cue(self):
        self.song().jump_to_prev_cue()

    def __jump_to_next_cue(self):
        self.song().jump_to_next_cue()

    def __set_loopstart_from_cur_position(self):
        if self.song().current_song_time < self.song().loop_start + self.song().loop_length:
            old_loop_start = self.song().loop_start
            self.song().loop_start = self.song().current_song_time
            self.song().loop_length += old_loop_start - self.song().loop_start

    def __set_loopend_from_cur_position(self):
        if self.song().current_song_time > self.song().loop_start:
            self.song().loop_length = self.song().current_song_time - self.song().loop_start

    def __goto_home(self):
        self.song().current_song_time = 0

    def __goto_end(self):
        self.song().current_song_time = self.song().last_event_time

    def __on_session_is_visible_changed(self):
        if not self.session_is_visible():
            self.__update_zoom_button_led()

    def __update_zoom_led_in_session(self):
        if self.session_is_visible():
            clip_slot = self.selected_clip_slot()
            if clip_slot and clip_slot.clip:
                if clip_slot.clip.is_triggered:
                    state = CLIP_TRIGGERED
                elif clip_slot.clip.is_playing:
                    state = CLIP_PLAYING
                else:
                    state = CLIP_STOPPED
            else:
                state = CLIP_STOPPED
            if state != self.__last_focussed_clip_play_state:
                self.__last_focussed_clip_play_state = state
                if state == CLIP_PLAYING:
                    self.send_midi((NOTE_ON_STATUS, SID_JOG_ZOOM, BUTTON_STATE_ON))
                elif state == CLIP_TRIGGERED:
                    self.send_midi((NOTE_ON_STATUS, SID_JOG_ZOOM, BUTTON_STATE_BLINKING))
                else:
                    self.send_midi((NOTE_ON_STATUS, SID_JOG_ZOOM, BUTTON_STATE_OFF))

    def __update_forward_rewind_leds(self):
        if self.__forward_button_down:
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_FAST_FORWARD, BUTTON_STATE_ON))
            self.__transport_repeat_delay = 0
        else:
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_FAST_FORWARD, BUTTON_STATE_OFF))
        if self.____rewind_button_down:
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_REWIND, BUTTON_STATE_ON))
            self.__transport_repeat_delay = 0
        else:
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_REWIND, BUTTON_STATE_OFF))

    def __update_zoom_button_led(self):
        if self.__zoom_button_down:
            self.send_midi((NOTE_ON_STATUS, SID_JOG_ZOOM, BUTTON_STATE_ON))
        else:
            self.send_midi((NOTE_ON_STATUS, SID_JOG_ZOOM, BUTTON_STATE_OFF))

    def __update_scrub_button_led(self):
        if self.__scrub_button_down:
            self.send_midi((NOTE_ON_STATUS, SID_JOG_SCRUB, BUTTON_STATE_ON))
        else:
            self.send_midi((NOTE_ON_STATUS, SID_JOG_SCRUB, BUTTON_STATE_OFF))

    def __update_play_button_led(self):
        if self.song().is_playing:
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_PLAY, BUTTON_STATE_ON))
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_STOP, BUTTON_STATE_OFF))
        else:
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_PLAY, BUTTON_STATE_OFF))
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_STOP, BUTTON_STATE_ON))

    def __update_record_button_led(self):
        if self.song().record_mode:
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_RECORD, BUTTON_STATE_ON))
        else:
            self.send_midi((NOTE_ON_STATUS, SID_TRANSPORT_RECORD, BUTTON_STATE_OFF))

    def __update_follow_song_button_led(self):
        if self.song().follow_song:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_FROM_PREV, BUTTON_STATE_ON))
        else:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_FROM_PREV, BUTTON_STATE_OFF))

    def __update_prev_cue_button_led(self):
        if self.song().can_jump_to_prev_cue:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_FROM_PREV, BUTTON_STATE_ON))
        else:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_FROM_PREV, BUTTON_STATE_OFF))

    def __update_next_cue_button_led(self):
        if self.song().can_jump_to_next_cue:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_FROM_NEXT, BUTTON_STATE_ON))
        else:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_FROM_NEXT, BUTTON_STATE_OFF))

    def __update_loop_button_led(self):
        if self.song().loop:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_LOOP, BUTTON_STATE_ON))
        else:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_LOOP, BUTTON_STATE_OFF))

    def __update_punch_in_button_led(self):
        if self.song().punch_in:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_PI, BUTTON_STATE_ON))
        else:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_PI, BUTTON_STATE_OFF))

    def __update_punch_out_button_led(self):
        if self.song().punch_out:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_PO, BUTTON_STATE_ON))
        else:
            self.send_midi((NOTE_ON_STATUS, SID_MARKER_PO, BUTTON_STATE_OFF))
# okay decompiling Transport.pyc
