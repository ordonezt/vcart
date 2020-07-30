#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 18:55:49 2020

@author: ord
"""
import sys, traceback
import serial
import time
from serial.threaded import LineReader, ReaderThread
import signal as syssig

def terminar_programa(signal_number, frame):
    print('\n\nCerrando...')
#    sdr.close()
    protocolo.close()
    sys.exit()

class PrintLines(LineReader):
    def connection_made(self, transport):
        super(PrintLines, self).connection_made(transport)
        sys.stdout.write('port opened\n')
        self.write_line('hello world')

    def handle_line(self, data):
        #sys.stdout.write('line received: {}\n'.format(repr(data)))
        
        if data == '<0>':
            flag_posicion_cero = True
        if data == '<OK>':
            flag_paso_realizado = True
        if data[0] == '<' and data[1] == 'S' and data[-1] == '>':
            flag_estado_recibido = True
            
            datos_unidos = data[2:-1]
            datos_separados = datos_unidos.split('@')
            
            elevacion = int(datos_separados[0])
            azimut = int(datos_separados[1])
            # print('Elevacion: {}'.format(elevacion))
            # print('Azimut: {}'.format(azimut))
            
            fin_de_trama_derecho = bool(int(datos_separados[2][0]))
            fin_de_trama_izquierdo = bool(int(datos_separados[2][1]))
            fin_de_trama_inferior = bool(int(datos_separados[2][2]))
            fin_de_trama_superior = bool(int(datos_separados[2][3]))


    def connection_lost(self, exc):
        if exc:
            traceback.print_exc(exc)
        sys.stdout.write('port closed\n')

#Asocio la señal de interrupcion de teclado a un handler para terminar el script
syssig.signal(syssig.SIGINT, terminar_programa)

ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=1.0)
# with ReaderThread(ser, PrintLines) as protocol:
#     while True:
#         aux = 1
    #protocol.write_line('hello')
    #time.sleep(10)

protocolo = ReaderThread(ser, PrintLines)
protocolo.start()

n = 0
while True:
    if n == 20:
        print('MAIN')
    n += 1
    