#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import serial
import struct
from enum import Enum
from time import sleep

class Button(Enum):
    RIGHT = 0x00
    LEFT = 0x01
    UP = 0x02
    DOWN = 0x03
    A = 0x04
    B = 0x05
    X = 0x06
    Y = 0x07
    HOME = 0x10
    
def press(ser, btn, duration=0.1, wait=0.1):
    #print('press {}'.format(btn.name))
    ser.write(struct.pack('B', btn.value))
    ser.write(struct.pack('B', 0x00))
    ser.flush()
    sleep(duration)
    ser.write(struct.pack('B', btn.value))
    ser.write(struct.pack('B', 0x01))
    ser.flush()
    sleep(wait)

def pressRep(ser, btn, repeat, duration=0.1, interval=0.1, wait=0.1):
	for i in range(repeat):
		press(ser, btn, duration, 0 if i == repeat - 1 else interval)
	sleep(wait)