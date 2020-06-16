#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 19:35:14 2020

@author: ord
"""
import numpy as np
from rtlsdr import RtlSdr
from matplotlib import pyplot as plt
import scipy.signal as signal

sdr = RtlSdr()

#conigure device
sdr.sample_rate = 2.048e6 #Hz
sdr.center_freq = 105.5e6  #Hz
sdr.freq_correction = 60 #ppm
sdr.gain = 12.5
sdr.set_agc_mode(False)
#sdr.bandwidth = 10e6 #Hz

n = 500
nfft = 1024
tiempo_muestreo = n * nfft / sdr.sample_rate
iq = sdr.read_samples(n * nfft)

sdr.close()

# plt.specgram(iq, NFFT=1024, Fs=sdr.sample_rate, Fc = sdr.center_freq/1e6)
# plt.title("PSD of 'signal' loaded from file")
# plt.xlabel("Time")
# plt.ylabel("Frequency (MHz)")
# plt.show()  # if you've done this right, you should see a fun surprise here!

# Let's try a PSD plot of the same data
plt.psd(iq, NFFT=nfft, Fs=sdr.sample_rate, Fc=sdr.center_freq/1e6)
plt.title("PSD of 'signal' loaded from file")
plt.show() 


# And let's look at it on the complex plan
# Note that showing *every* data point would be time- and processing-intensive
# so we'll just show a few
# plt.scatter(np.real(iq), np.imag(iq))
# plt.title("Constellation of the 'signal' loaded from file")
# plt.show() 