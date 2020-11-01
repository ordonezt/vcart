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
import pandas

# mapa_potencia = 0

def terminar_programa(signal_number=None, frame=None):
    print('\n\nCerrando...')
    # try:
    #     if sdr.device_opened:
    #         sdr.close()
    # except:
    #     pass
    # global mapa_potencia
    
    # print('Graficando...')
    # titulo =    'Mapa de potencia ' + \
    #             str(sdrcon.sdr.get_frecuencia_central()/1e9) + 'GHz'
    # im, cbar = interfaz.mapa_de_potencia(mapa_potencia,  title=titulo)
    
    # nombre_archivo = 'Ultimo Mapeo'
    # formato = 'png'
    # im.figure.savefig(fname=nombre_archivo, format=formato)
    # print('Imagen guardada como "{}.{}"'.format(nombre_archivo, formato))
    # print('Listo\n\n')
    
    sdrcon.sdr.cerrar()
    # if hilo_uart.is_alive():
    #     hilo_uart.close()
    # if arduino.isOpen():
    #     arduino.close()
    ard.arduino.cerrar()
    sys.exit()

def mapear():
    
    
        
    rango_elevacion, rango_azimut = interfaz.imprimir_menu_mapear()
    
    mapa_potencia = np.zeros((rango_elevacion, rango_azimut))
    
    for paso_azimut in range(rango_azimut):
        if paso_azimut % 2 == 0:
            for paso_elevacion in range(rango_elevacion):
                #Medir potencia aca y avanzar paso
                #Calculo la potencia de la señal
                potencia = sdrcon.sdr.leer_potencia()
                
                mapa_potencia[paso_elevacion, paso_azimut] = potencia
                
                print('Elevacion: {}, Azimut: {}, Potencia: {:2.2f} dBFS'. format(paso_elevacion, paso_azimut, potencia))
                #ARRIBA
                ard.arduino.enviar_trama('3 1 15')
                
                while ard.arduino.flag_paso_realizado != True:
                    pass
                ard.arduino.flag_paso_realizado = False
        
        else:
            for paso_elevacion in range(rango_elevacion - 1, 0 - 1, -1):
                #Medir potencia aca y avanzar paso
                #Calculo la potencia de la señal
                potencia = sdrcon.sdr.leer_potencia()
                
                mapa_potencia[paso_elevacion, paso_azimut] = potencia
                
                print('Elevacion: {}, Azimut: {}, Potencia: {:2.2f} dBFS'. format(paso_elevacion, paso_azimut, potencia))
                #ABAJO
                ard.arduino.enviar_trama('3 0 15')
                
                while ard.arduino.flag_paso_realizado != True:
                    pass
                ard.arduino.flag_paso_realizado = False
        
        #Me corro hacia izquierda
        ard.arduino.enviar_trama('1 1 15')
        
        while ard.arduino.flag_paso_realizado != True:
            pass
        ard.arduino.flag_paso_realizado = False
    
    print('Mapeo terminado, volviendo al inicio...')
    for paso_azimut in range(rango_azimut):
        #Me corro hacia derecha para volver al inicio
        ard.arduino.enviar_trama('1 0 15')
        
        while ard.arduino.flag_paso_realizado != True:
            pass
        ard.arduino.flag_paso_realizado = False
    
    print('Graficando...')
    titulo =    'Mapa de potencia ' + \
                str(sdrcon.sdr.get_frecuencia_central()/1e9) + 'GHz'
    im, cbar = interfaz.mapa_de_potencia(mapa_potencia,  title=titulo)
    
    nombre_archivo = input('Ingrese un nombre para la imagen: ')
    formato = 'png'
    ruta_archivo = 'Mapeos/' + nombre_archivo
    im.figure.savefig(fname=ruta_archivo, format=formato)
    print('Imagen guardada como "{}.{}"'.format(nombre_archivo, formato))
    print('Listo\n\n')
    df=pandas.DataFrame(mapa_potencia)
    
    df.to_excel("Tablas/" + nombre_archivo + ".xlsx")


def leer_potencia_actual():
    print('\n\nLeer potencia actual')
    print('--------------------------\n')
    potencia = sdrcon.sdr.leer_potencia()
    print('Potencia: {:2.2f} dBFS'. format(potencia))
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
        sdrcon.sdr.configurar()
        
    elif entrada == 8:
        sdrcon.sdr.calibrar()
    
    elif entrada == 9:
        motor = input('3 elevacion, 1 azimutal: ')
        direccion = input('1 arriba/derecha, 0 abajo/izquierda: ')
        pasos = input('Cantidad de pasos: ')
        
        trama = motor +' ' + direccion + ' ' + pasos
        
        ard.arduino.enviar_trama(trama)
        
    
    elif entrada == 10:
        terminar_programa()
        
    else:
        interfaz.orden_no_valida()

#Si llego aca, algo salio mal
terminar_programa()
    
    