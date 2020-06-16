#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 12:43:14 2020

@author: ord
Resumen:
    La idea es realizar una medicion de potencia por cada confimacion del
    arduino de que estamos en una posicion estable
    
    Potencia:
        1) Para medir potencia con el sdr es necesario calibrarlo a una 
        frecuencia determinada (la de trabajo) y nosotros no estamos en
        condiciones de hacerlo (corona time)
        2) Es necesario APAGAR el AGC ya que va a manejar la ganancia a su
        gusto
        3) Calculamos la potencia de la señal muestreada
    
    Arduino:        
        1) Se le indica cuantas mediciones se van a hacer
        2) El arduino responde cuando ya se "posiciono"
        3) Le contestamos que ya hicimos la medicion y avance a la siguiente posicion
"""
import numpy as np
from rtlsdr import RtlSdr
import scipy.signal as signal
import signal as syssig
import sys
import time
import serial


def terminar_programa(signal_number, frame):
    print('\n\nCerrando...')
    sdr.close()
    arduino.close()
    sys.exit()

def get_potencia(X):  
    #f, psd = signal.welch(muestras,sample_rate,nfft=10*nfft,return_onesided=False)
    
    # #Calculo la densidad de potencia de la señal [unidad_señal²/Hz]
    # f, psd = signal.periodogram(muestras, sdr.sample_rate, nfft=nfft, return_onesided=False)
    
    # #Averiguo la potencia promedio en dBunidad_señal
    # potencia = 10 * np.log10(np.mean(psd) * sdr.sample_rate)
    
    #Potencia señal discreta:
    # Px = (1 / N) * Sumatoria(|X(n)|^2);  n in range(0, N)
    
    N = len(X)
    potencia = (1 / N) * sum(abs(X[n]) ** 2 for n in range(N))

    return 10 * np.log10(potencia)

#Asocio la señal de interrupcion de teclado a un handler para terminar el script
syssig.signal(syssig.SIGINT, terminar_programa)

#Abro el puerto serie del arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1.0)

#Abro el dongle
sdr = RtlSdr()

#Lo configuro
sdr.sample_rate = 2.048e6 #Hz
sdr.center_freq = 433.83e6  #Hz
sdr.freq_correction = 60 #ppm
sdr.gain = 0.0 #dB
sdr.set_agc_mode(False)

nfft = 1024
n = 256

#Reseteamos el arduino
arduino.setDTR(False)
#Esperamos 1 segundo
time.sleep(1)
arduino.flushInput()
arduino.setDTR(True)

with arduino:
    while True:
        
        cantidad = input("Ingrese cantidad de mediciones entre 1 y 9: ")
    
        arduino.write(cantidad.encode())
    
        #Leo lineas del arduino (posicion) hasta la palabra Fin
        for rawString in iter(lambda: arduino.readline(), b'Fin\r\n'):
            #Leo las muestras
            iq = sdr.read_samples(n * nfft)
            
            #Calculo la potencia de la señal
            potencia = get_potencia(iq) - sdr.gain
            
            #Imprimo los resultados
            print('Medicion ' + str(rawString.decode("utf-8")) + ': {:2.2f} dB'.format(potencia))
            
            #Le mando al arduino que ya termine la medicion y "mueva los motores"
            arduino.write(bytes(b'r'))
        

# #Cierro los dispositivos
# arduino.close()
sdr.close()
