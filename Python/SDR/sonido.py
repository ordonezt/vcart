#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 18:12:03 2020

@author: ord
"""

import sounddevice as sd
import numpy as np
import threading
import sdr_controlador as sdrcon
import control
import time as time_lib

import random

start_idx = 0
duracion = 10#Segundos
frequencia = 600#Hz
frecuencia_muestreo = 44.1e3#Hz
incremento = 0.01
amplitud = 0.05
sensibilidad = 100 #Veces de sonido /Veces de potencia relativa
offset = -70

def callback_sonido(outdata, frames, time, status):
    if status:
        print(status)
    global start_idx
    global amplitud
    global frequencia
    t = (start_idx + np.arange(frames)) / frecuencia_muestreo
    t = t.reshape(-1, 1)
    outdata[:] = amplitud * np.sin(2 * np.pi * frequencia * t)
    start_idx += frames

class hilo_potencia_sonido(threading.Thread):
    
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.corriendo = False
    
    def run(self):
        global amplitud
        self.corriendo = True
        #La latencia de 2 segundos y el tamaño de bloques fueron totalmente
        #aleatorios hasta que anduvo sin errores
        with sd.OutputStream(callback=callback_sonido, blocksize=10000, latency=2):
            while self.corriendo:
                potencia = control.db2mag(sdrcon.sdr.leer_potencia()) - control.db2mag(offset)
                #potencia = control.db2mag(-random.randint(55, 70))
                amplitud_aux = sensibilidad * potencia
                amplitud = amplitud_aux if amplitud_aux < 1 else 1
                print('Diferencia de potencia: {} veces'.format(potencia))
                print('Volumen: {}'.format(amplitud))
                time_lib.sleep(200e-3)
    
    def terminate(self):
        self.corriendo = False

def busqueda_manual():
    print('\n\nBusqueda manual')
    print('--------------------------\n')
    hilo = hilo_potencia_sonido('Hilo 1')
    hilo.start()
    
    input('Presione cualquier tecla para salir')
    hilo.terminate()
    print('Listo\n\n')
    
