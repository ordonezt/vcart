#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 16:38:25 2020

@author: ord
Resumen:
    
"""
import numpy as np
from rtlsdr import RtlSdr
import scipy.signal as signal
import signal as syssig
import sys
import time
import serial
from serial.threaded import LineReader, ReaderThread
import os
import traceback

borrar_consola = lambda: os.system('clear')

flag_posicion_cero = False
flag_paso_realizado = False
flag_estado_recibido = False

elevacion = 0
azimut = 0

fin_de_trama_derecho  = False
fin_de_trama_izquierdo = False
fin_de_trama_inferior = False
fin_de_trama_superior = False

def terminar_programa(signal_number=None, frame=None):
    print('\n\nCerrando...')
    # if sdr.isOpen():
    #     sdr.close()
    if hilo_uart.is_alive():
        hilo_uart.close()
    if arduino.isOpen():
        arduino.close()
        
    sys.exit()

def get_potencia(X):  
    
    N = len(X)
    potencia = (1 / N) * sum(abs(X[n]) ** 2 for n in range(N))

    return 10 * np.log10(potencia)

def esperar_hasta(dispositivo, trama):
    #Leo lineas del arduino hasta que indique que termino
    for n, rawString in enumerate(iter(lambda: dispositivo.readline(), trama)):
        if n % 5:
            print('.', end='')

class PrintLines(LineReader):
    def connection_made(self, transport):
        super(PrintLines, self).connection_made(transport)
        #sys.stdout.write('port opened\n')
        #self.write_line('hello world')

    def handle_line(self, data):
        #sys.stdout.write('line received: {}\n'.format(repr(data)))
        global flag_posicion_cero
        global flag_paso_realizado
        global flag_estado_recibido
        
        global elevacion
        global azimut
        
        global fin_de_trama_derecho
        global fin_de_trama_izquierdo
        global fin_de_trama_inferior
        global fin_de_trama_superior
        
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
        #sys.stdout.write('port closed\n')

#Asocio la señal de interrupcion de teclado a un handler para terminar el script
syssig.signal(syssig.SIGINT, terminar_programa)

print('VCAR (Very Cheap Argentinian Radio Telescope)')
print('Iniciando...')
print('Arduino...', end='')
#Abro el puerto serie del arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1.0)
if arduino.isOpen:
    print('Listo')
else:
    print('Error')
    terminar_programa()

print('Hilo de comunicaciones...', end='')
hilo_uart = ReaderThread(arduino, PrintLines)
#Reseteamos el arduino
arduino.setDTR(False)
#Esperamos 1 segundo
time.sleep(1)
arduino.flushInput()
arduino.setDTR(True)
hilo_uart.start()

if hilo_uart.is_alive():
    print('Listo')
else:
    print('Error')
    terminar_programa()


#Abro el dongle
# sdr = RtlSdr()

# #Lo configuro
# sdr.sample_rate = 2.048e6 #Hz
# sdr.center_freq = 433.83e6  #Hz
# sdr.freq_correction = 60 #ppm
# sdr.gain = 0.0 #dB
# sdr.set_agc_mode(False)

# nfft = 1024
# n = 256
print('\n')
with arduino:
    while True:
        
        # cantidad = input("Ingrese cantidad de mediciones entre 1 y 9: ")
    
        # arduino.write(cantidad.encode())
    
        # #Leo lineas del arduino (posicion) hasta la palabra Fin
        # for rawString in iter(lambda: arduino.readline(), b'Fin\r\n'):
        #     #Leo las muestras
        #     iq = sdr.read_samples(n * nfft)
            
        #     #Calculo la potencia de la señal
        #     potencia = get_potencia(iq) - sdr.gain
            
        #     #Imprimo los resultados
        #     print('Medicion ' + str(rawString.decode("utf-8")) + ': {:2.2f} dB'.format(potencia))
            
        #     #Le mando al arduino que ya termine la medicion y "mueva los motores"
        #     arduino.write(bytes(b'r'))
        print('Menu principal:')
        print('---------------\n')
        print('1) Llevar a posicion cero')
        print('2) Leer posicion actual')
        print('3) Leer potencia actual')
        print('4) Mapear')
        print('5) Resetear Arduino')
        print('6) Salir')
        entrada = int(input('Ingrese una accion: '))
        print(entrada)
        
        if entrada == 1:
            #borrar_consola()
            print('\n\nLlevar a posicion cero')
            print('--------------------------\n')
            arduino.write(bytes(b'<0>'))
            
            print('Esperando...', end='')
            
            while flag_posicion_cero != True:
                pass
            flag_posicion_cero = False
            
            print('Listo\n\n')
        
        elif entrada == 2:
            
            #borrar_consola()
            print('\n\nLeer posicion actual')
            print('--------------------------\n')
            
            arduino.write(bytes(b'<S>'))
            
            while flag_estado_recibido != True:
                pass
            flag_estado_recibido = False
            
            print('Elevacion: {}'.format(elevacion))
            print('Azimut: {}\n\n'.format(azimut))
            
            
        elif entrada == 3:
            borrar_consola()
        elif entrada == 4:
            #borrar_consola()
            print('\n\nMapear')
            print('----------\n')
            
            rango_elevacion = int(input('Ingrese la cantidad de pasos de elevacion: '))
            rango_azimut = int(input('Ingrese la cantidad de pasos de azimut: '))
            
            for paso_azimut in range(rango_azimut):
                if paso_azimut % 2 == 0:
                    for paso_elevacion in range(rango_elevacion):
                        print(paso_azimut, paso_elevacion)
                        #Medir potencia aca y avanzar paso
                        
                        
                        arduino.write(b'<U>')
                        
                        while flag_paso_realizado != True:
                            pass
                        flag_paso_realizado = False
                        
                        print('Paso realizado')
                else:
                    for paso_elevacion in range(rango_elevacion - 1, 0, -1):
                        print(paso_azimut, paso_elevacion)
                        #Medir potencia aca y avanzar paso
                        
                        
                        arduino.write(b'<D>')
                        
                        while flag_paso_realizado != True:
                            pass
                        flag_paso_realizado = False
                        
                        print('Paso realizado')
                
                #Me corro hacia izquierda
                arduino.write(b'<L>')
                
                while flag_paso_realizado != True:
                    pass
                flag_paso_realizado = False
                
                print('Paso realizado')
            
            print('Listo\n\n')

        elif entrada == 5:
            #Reseteamos el arduino
            arduino.setDTR(False)
            #Esperamos 1 segundo
            time.sleep(1)
            arduino.flushInput()
            arduino.setDTR(True)                 
            
        elif entrada == 6:
            #borrar_consola()
            terminar_programa()
        else:
            borrar_consola()

# #Cierro los dispositivos
# arduino.close()
#sdr.close()