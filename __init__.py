# uncompyle6 version 3.2.5
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.13 |Continuum Analytics, Inc.| (default, May 11 2017, 13:17:26) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: c:\Jenkins\live\output\win_64_static\Release\python-bundle\MIDI Remote Scripts\MackieControl\__init__.py
# Compiled at: 2018-07-05 14:45:24
from __future__ import absolute_import, print_function, unicode_literals
from .MackieControl import MackieControl

def create_instance(c_instance):
    return MackieControl(c_instance)


from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2675, product_ids=[
                         6], model_name='MCU Pro USB v3.1'), 
       PORTS_KEY: [
                 inport(props=[SCRIPT, REMOTE]),
                 inport(props=[]),
                 inport(props=[]),
                 inport(props=[]),
                 outport(props=[SCRIPT, REMOTE]),
                 outport(props=[]),
                 outport(props=[]),
                 outport(props=[])]}
# okay decompiling __init__.pyc
