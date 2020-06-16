#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 17:16:20 2020

@author: ord
"""

import time
import serial

#Abro el puerto serie del arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600)

while True:
    
    cantidad = input("Ingrese cantidad de mediciones entre 1 y 9: ")

    arduino.write(cantidad.encode())

    time.sleep(2)

    #Leo lineas del arduino hasta la palabra Fin
    for rawString in iter(lambda: arduino.readline, 'Fin'):
        #Imprimo los resultados
        print(rawString)
        #Le mando al arduino que ya termine la medicion
        arduino.write('r'.encode())
    
    print('Fin')

#Cierro los dispositivos
arduino.close()