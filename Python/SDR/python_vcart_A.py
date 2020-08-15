#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 16:38:25 2020

@author: ord
Resumen:
    
"""
import numpy as np
import scipy.signal as signal
import signal as syssig
import sys
import interfaz
import arduino_controlador as ard
import sdr_controlador as sdrcon
import sonido


def terminar_programa(signal_number=None, frame=None):
    print('\n\nCerrando...')
    # try:
    #     if sdr.device_opened:
    #         sdr.close()
    # except:
    #     pass
    sdrcon.sdr.cerrar()
    # if hilo_uart.is_alive():
    #     hilo_uart.close()
    # if arduino.isOpen():
    #     arduino.close()
    ard.arduino.cerrar()
    sys.exit()

def mapear():
    rango_elevacion, rango_azimut = interfaz.imprimir_menu_mapear()
    
    mapa_potencia = np.zeros((rango_azimut, rango_elevacion))
    
    for paso_azimut in range(rango_azimut):
        if paso_azimut % 2 == 0:
            for paso_elevacion in range(rango_elevacion):
                #Medir potencia aca y avanzar paso
                #Calculo la potencia de la señal
                potencia = sdrcon.sdr.leer_potencia()
                
                mapa_potencia[paso_azimut, paso_elevacion] = potencia
                
                print('Elevacion: {}, Azimut: {}, Potencia: {:2.2f}dB'. format(paso_elevacion, paso_azimut, potencia))
                
                ard.arduino.enviar_trama('<U>')
                
                while ard.arduino.flag_paso_realizado != True:
                    pass
                ard.arduino.flag_paso_realizado = False
        
        else:
            for paso_elevacion in range(rango_elevacion - 1, 0 - 1, -1):
                #Medir potencia aca y avanzar paso
                #Calculo la potencia de la señal
                potencia = sdrcon.sdr.leer_potencia()
                
                mapa_potencia[paso_azimut, paso_elevacion] = potencia
                
                print('Elevacion: {}, Azimut: {}, Potencia: {:2.2f}dB'. format(paso_elevacion, paso_azimut, potencia))
                
                ard.arduino.enviar_trama('<D>')
                
                while ard.arduino.flag_paso_realizado != True:
                    pass
                ard.arduino.flag_paso_realizado = False
        
        #Me corro hacia izquierda
        ard.arduino.enviar_trama('<L>')
        
        while ard.arduino.flag_paso_realizado != True:
            pass
        ard.arduino.flag_paso_realizado = False
    
    print('Graficando...')
    im, cbar = interfaz.mapa_de_potencia(mapa_potencia)
    
    nombre =    'mapa_potencia_' + \
                str(sdrcon.sdr.dispositivo.center_freq/1e9) + 'GHz_' + \
                str(rango_elevacion) + 'x' + str(rango_azimut)
    formato = 'png'
    im.figure.savefig(fname=nombre, format=formato)
    print('Imagen guardada como "{}.{}"'.format(nombre, formato))
    print('Listo\n\n')

def leer_potencia_actual():
    print('\n\nLeer potencia actual')
    print('--------------------------\n')
    potencia = sdrcon.sdr.leer_potencia()
    print('Potencia: {:2.2f}dB'. format(potencia))
    print('Listo\n\n')

    
#Asocio la señal de interrupcion de teclado a un handler para terminar el script
syssig.signal(syssig.SIGINT, terminar_programa)

#Inicia el programa
interfaz.splash()

ard.inicializar_arduino()
if ard.arduino.esta_abierto() == False:
    terminar_programa()

sdrcon.inicializar_sdr()
if sdrcon.sdr.esta_abierto() == False:
    terminar_programa()


print('\n')

while True:
    
    entrada = interfaz.imprimir_menu()
    
    if entrada == 1:
        ard.arduino.llevar_a_cero()
    
    elif entrada == 2:
        ard.arduino.leer_posicion_actual()
        
    elif entrada == 3:
        leer_potencia_actual()
        
    elif entrada == 4:
        mapear()

    elif entrada == 5:
        ard.arduino.reset()        
     
    elif entrada == 6:
        sonido.busqueda_manual()
        
    elif entrada == 7:
        terminar_programa()
    
    else:
        interfaz.orden_no_valida()

#Si llego aca, algo salio mal
terminar_programa()
    
    