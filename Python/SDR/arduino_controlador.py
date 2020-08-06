#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 17:47:29 2020

@author: ord
"""
import time
import serial
import serial.tools.list_ports
from serial.threaded import LineReader, ReaderThread
import traceback
import sys
#from globales import PrintLines

def inicializar_arduino():
    global arduino
    arduino = Arduino()

class PrintLines(LineReader):
    def connection_made(self, transport):
        super(PrintLines, self).connection_made(transport)
        #sys.stdout.write('port opened\n')
        #self.write_line('hello world')

    def handle_line(self, data):
        #sys.stdout.write('line received: {}\n'.format(repr(data)))
        #global arduino
        
        # # global flag_posicion_cero
        # # global flag_paso_realizado
        # # global flag_estado_recibido
        
        # # global elevacion
        # # global azimut
        
        # # global fin_de_trama_derecho
        # # global fin_de_trama_izquierdo
        # # global fin_de_trama_inferior
        # # global fin_de_trama_superior
        
        if data == '<0>':
            arduino.flag_posicion_cero = True
        if data == '<OK>':
            arduino.flag_paso_realizado = True
        if data[0] == '<' and data[1] == 'S' and data[-1] == '>':
            arduino.flag_estado_recibido = True
            
            datos_unidos = data[2:-1]
            datos_separados = datos_unidos.split('@')
            
            arduino.elevacion = int(datos_separados[0])
            arduino.azimut = int(datos_separados[1])
            # print('Elevacion: {}'.format(elevacion))
            # print('Azimut: {}'.format(azimut))
            
            arduino.fin_de_trama_derecho = bool(int(datos_separados[2][0]))
            arduino.fin_de_trama_izquierdo = bool(int(datos_separados[2][1]))
            arduino.fin_de_trama_inferior = bool(int(datos_separados[2][2]))
            arduino.fin_de_trama_superior = bool(int(datos_separados[2][3]))
    
    def connection_lost(self, exc):
        if exc:
            traceback.print_exc(exc)
        #sys.stdout.write('port closed\n')

class Arduino:
    
    def __init__(self):
        
        self.baudrate = 9600
        
        print('Buscando un arduino...')
        
        puertos = list(serial.tools.list_ports.comports())
        
        for puerto in puertos:
            self.ser = serial.Serial(puerto.device, self.baudrate, timeout=1.0)
        
        if self.ser.isOpen() == True:
            print('Conectado a {}'.format(self.ser.name))
        else:
            print('Error, Arduino no conectado')
        
        print('Creando hilo de comunicacion...')
        self.hilo_uart = ReaderThread(self.ser, PrintLines)
        
        #if self.hilo_uart.is_alive():
        if self.hilo_uart._connection_made:
            print('Hilo creado')
        else:
            print('Error creando el hilo')
        
        self.flag_posicion_cero = False
        self.flag_paso_realizado = False
        self.flag_estado_recibido = False
        
        self.elevacion = 0
        self.azimut = 0
        
        self.fin_de_trama_derecho  = False
        self.fin_de_trama_izquierdo = False
        self.fin_de_trama_inferior = False
        self.fin_de_trama_superior = False
        
        self.iniciar()
    
    def iniciar(self):
        self.reset()
        self.hilo_uart.start()
        
    def reset(self):
        print('\n\nResetear arduino')
        print('--------------------\n')
        print('Esperando...')
        #Reseteamos el arduino
        self.ser.setDTR(False)
        #Esperamos 1 segundo
        time.sleep(0.1)
        self.ser.flushInput()
        self.ser.setDTR(True)  
        print('Listo\n\n')
    
    def enviar_trama(self, trama):
        self.ser.write(trama.encode())
    
    def cerrar(self):
        if self.hilo_uart.is_alive():
            self.hilo_uart.close()
        
        if self.ser.isOpen():
            self.ser.close()
    
    def esta_abierto(self):
        return self.ser.isOpen() and self.hilo_uart.is_alive()
    
    def llevar_a_cero(self):
        print('\n\nLlevar a posicion cero')
        print('--------------------------\n')
        self.enviar_trama('<0>')
        
        print('Esperando...')
        
        while self.flag_posicion_cero != True:
            pass
        self.flag_posicion_cero = False
        
        print('Listo\n\n')
    
    def leer_posicion_actual(self):
        print('\n\nLeer posicion actual')
        print('--------------------------\n')
        
        self.enviar_trama('<S>')
        
        while self.flag_estado_recibido != True:
            pass
        self.flag_estado_recibido = False
        
        print('Elevacion: {}'.format(self.elevacion))
        print('Azimut: {}\n\n'.format(self.azimut))
        
    def set_flag_posicion_cero(self):
        self.flag_posicion_cero = True
        