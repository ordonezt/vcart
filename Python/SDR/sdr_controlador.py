#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 22:33:05 2020

@author: ord
"""
import numpy as np
from rtlsdr import RtlSdr

def inicializar_sdr():
    global sdr
    sdr = Sdr()

def calcular_potencia(X):  
    
    N = len(X)
    potencia = (1 / N) * sum(abs(X[n]) ** 2 for n in range(N))

    return 10 * np.log10(potencia)

class Sdr():
    
    def __init__(self):
        #Abro el dongle
        self.dispositivo = RtlSdr()
        
        #Lo configuro
        self.dispositivo.sample_rate = 2.048e6 #Hz
        self.dispositivo.center_freq = 1e9  #Hz
        self.dispositivo.freq_correction = 60 #ppm
        self.dispositivo.gain = 49.6 #dB
        self.dispositivo.set_agc_mode(False)
        
        self.nfft = 1024
        self.n = 256
    
    def leer_potencia(self):
        #Leo las muestras
        iq = self.dispositivo.read_samples(self.n * self.nfft)
        #Calculo la potencia de la señal
        potencia = calcular_potencia(iq) - self.dispositivo.gain
        
        return potencia
    
    def esta_abierto(self):
        return self.dispositivo.device_opened
    
    def cerrar(self):
        if self.esta_abierto():
            self.dispositivo.close()
