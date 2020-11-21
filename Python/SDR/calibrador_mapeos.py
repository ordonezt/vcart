#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 16:09:38 2020

@author: ord
"""
#Pedir potencia de calibracion
#Abrir todos los mapeos que no tengan calibrado en el nombre
#Generar nueva grilla calibrada
#Guardar la imagen y grilla calibrada

import os
import pandas as pd
import interfaz

# try:
#Pedir potencia de calibracion
potencia_de_calibracion = int(input('Ingrese la potencia de calibracion (dBFS): '))

#Abrir todos los mapeos que no tengan calibrado en el nombre
for archivo in os.listdir('Tablas/'):
    if archivo.endswith('xlsx') and ('calibrado' in archivo) == False:
        print('Archivo encontrado: ' + str(archivo))
        #Generar nueva grilla calibrada
        grilla = pd.read_excel('Tablas/' + str(archivo), sheet_name='Sheet1')
        grilla = grilla.to_numpy() - potencia_de_calibracion
        grilla = grilla[:, 1:]
        
        print('Graficando...')
        titulo = 'Mapa de potencia ({:2.2f} dBFS)'.format(potencia_de_calibracion)
        im, cbar = interfaz.mapa_de_potencia_calibrado(grilla,  title=titulo)
        
        #Guardar la imagen y grilla calibrada
        nombre_archivo = (archivo.split('.'))[0] + '_calibrado'
        formato = 'png'
        ruta_archivo = 'Mapeos/Calibrados/' + nombre_archivo
        im.figure.savefig(fname=ruta_archivo, format=formato)
        print('Imagen guardada como "{}.{}"'.format(nombre_archivo, formato))
        
        df = pd.DataFrame(grilla)
        df.to_excel("Tablas/Calibradas/" + nombre_archivo + ".xlsx")
        print('Datos guardados como "{}.{}"'.format(nombre_archivo, 'xlsx'))
        
        print('Listo\n\n')
            
# except:
#     print('Entrada no valida')
