#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 23:29:45 2020

@author: ord
"""

from rtlsdr import RtlSdr

sdr = RtlSdr()

#conigure device
sdr.sample_rate = 2.048e6 #Hz
sdr.center_freq = 70e6  #Hz
sdr.freq_correction = 60 #ppm
sdr.gain = 'auto'

print(sdr.read_samples(512))