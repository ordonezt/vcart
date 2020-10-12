#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 22:33:05 2020

@author: ord
"""
import numpy as np
from rtlsdr import RtlSdr
import interfaz


def inicializar_sdr():
    global sdr
    sdr = Sdr()

def calcular_potencia(X, Vref, Zo):  
    
    N = len(X)
    potencia = (Vref ** 2 / (N * Zo)) * (sum(abs(X[n]) ** 2)  for n in range(N))

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
        
        self.frecuencia_oscilador_local_lnb = 10.5e9
        
        self.limite_inferior_Ku = 11.45e9
        self.limite_superior_Ku = 12.25e9
        
        self.nfft = 1024
        self.n = 256
        
        self.Vref = 1#V
        self.Zo = 2e3#Ohm
        
    def leer_potencia(self):
        #Leo las muestras
        iq = self.dispositivo.read_samples(self.n * self.nfft)
        #Calculo la potencia de la señal
        potencia = calcular_potencia(iq, self.Vref, self.Zo) - self.dispositivo.gain
        
        return potencia
    
    def configurar(self):
        entrada = 0
        while entrada != 6:
            
            entrada = interfaz.imprimir_menu_configuracion()
            
            if entrada == 1:
                frecuencia = float(input('Ingrese una frecuencia entre {:f} Hz y {:f} (en Hz): '.format(self.limite_inferior_Ku, self.limite_superior_Ku)))
                if (frecuencia < self.limite_inferior_Ku) or (frecuencia > self.limite_superior_Ku):
                    print('Valor fuera de rango')
                else:
                    self.dispositivo.set_center_freq(frecuencia - self.frecuencia_oscilador_local_lnb)
                    
            elif entrada == 2:
                ancho_banda = float(input('Ingrese un ancho de banda entre 1 MHz y 3.2 MHz (En Hz): '))
                
                if (ancho_banda < 1e6) or (ancho_banda > 3.2e6):
                    print('Valor fuera de rango')
                else:
                    self.dispositivo.set_sample_rate(ancho_banda)
                
            elif entrada == 3:
                lista = np.array(self.dispositivo.valid_gains_db)
                
                try :
                    self.dispositivo.set_gain(float(input('Ingrese una ganancia entre {:2.1f} dB y {:2.1f} dB: '.format(np.min(lista), np.max(lista)))))
                    print('Ganancia configurada en {:2.1f} dB'.format(self.dispositivo.get_gain()))
                except:
                    print('Valor fuera de rango')
                
            elif entrada == 4:
                try:
                    self.n = int(input('Ingrese la cantidad de paquetes de 1024 muestras: '))
                except:
                    print('Valor fuera de rango')
                
            elif entrada == 5:
                frecuencia_central = self.get_frecuencia_central() #Hz
                ancho_banda = self.dispositivo.get_sample_rate() #Hz
                ganancia = self.dispositivo.get_gain() #dB
                paquetes = self.n
                tamanio_paquete = self.nfft
                
                print('Configuracion actual: ')
                print('Frecuencia central: {:f} Hz'.format(frecuencia_central))
                print('Ancho de banda: {:f} Hz'.format(ancho_banda))
                print('Ganancia: {:2.1f} dB'.format(ganancia))
                print('Mediciones compuestas por {} paquetes de {} muestras'.format(paquetes, tamanio_paquete))
                print('Tiempo aproximado por medicion: {:f} ms'.format(1e3 *paquetes * tamanio_paquete / ancho_banda))
            
            elif entrada == 6:
                print('Configuracion realizada\n')
                
            else:
                interfaz.orden_no_valida()
    
    def get_frecuencia_central(self):
        return self.dispositivo.get_center_freq() + self.frecuencia_oscilador_local_lnb
    
    def esta_abierto(self):
        return self.dispositivo.device_opened
    
    def cerrar(self):
        if self.esta_abierto():
            self.dispositivo.close()
