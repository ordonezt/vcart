#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 14:37:53 2020

@author: ord
"""

import time
import serial

arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1.0)

#Reseteamos el arduino
arduino.setDTR(False)
#Esperamos 1 segundo
time.sleep(1)
arduino.flushInput()
arduino.setDTR(True)

with arduino:
    while 1:
    
        cantidad = input("Enviar: ")
    
        arduino.write(cantidad.encode())
    
        rawString = arduino.readline()
        print(rawString)