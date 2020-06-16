#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 23:36:59 2020

@author: ord
"""

from rtlsdr import RtlSdr
from matplotlib import pyplot as plt

sdr = RtlSdr()

#conigure device
sdr.sample_rate = 2.048e6 #Hz
sdr.center_freq = 105.5e6  #Hz
sdr.freq_correction = 60 #ppm
sdr.gain = 12.5
sdr.bandwidth = 10e3 #Hz

#Las muestras vienen normalizadas a 127.5, 
samples = sdr.read_samples(100 * 1024)
sample_time = 256 * 1024

sdr.close()

psd, f = plt.psd(samples,NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6,color='g')
plt.title('Power spectral density')
plt.xlabel('Frequency (MHz)')
plt.ylabel('Relative power (dB)')
plt.show()