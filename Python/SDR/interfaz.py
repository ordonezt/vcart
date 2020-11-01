#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 17:20:33 2020

@author: ord
"""
import numpy as np
import os
import matplotlib.pyplot as plt

def imprimir_menu():
    print('Menu principal:')
    print('---------------\n')
    print('1) Llevar a posicion cero')
    print('2) Leer posicion actual')
    print('3) Leer potencia actual')
    print('4) Mapear')
    print('5) Resetear Arduino')
    print('6) Busqueda manual')
    print('7) Configurar SDR')
    print('8) Calibrar')
    print('9) Mover motores')
    print('10) Salir')
    try:
        entrada = int(input('Ingrese una accion: '))
    except:
        entrada = -1
    
    return entrada

def imprimir_menu_configuracion():
    print('\n')
    print('Configurar SDR:')
    print('---------------\n')
    print('1) Frecuencia central')
    print('2) Ancho de banda')
    print('3) Ganancia')
    print('4) Cantidad de muestras por medicion')
    print('5) Leer configuracion actual')
    print('6) Salir')
    try:
        entrada = int(input('Ingrese una accion: '))
    except:
        entrada = -1
    
    return entrada



def orden_no_valida():
    print('Orden no valida')
    return

borrar_consola = lambda: os.system('clear')

def splash():
    print('VCART (Very Cheap Argentinian Radio Telescope)')
    print('Iniciando...')

def imprimir_menu_mapear():
    print('\n\nMapear')
    print('----------\n')
    
    rango_elevacion = int(input('Ingrese la cantidad de pasos de elevacion: '))
    rango_azimut = int(input('Ingrese la cantidad de pasos de azimut: '))
    
    return rango_elevacion, rango_azimut
    
def mapa_de_potencia(data, ax=None,
            cbar_kw={}, title="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """
    cbarlabel = 'Potencia absoluta[dBFS]'
    
    # vmin = -66#dB
    # vmax = -54#dB
    # vmax = 10
    # vmin = -100000
    
    # if (data.any() > vmax) or (data.any() < vmin):
    #     vmax = None
    #     vmin = None
    
    if not ax:
        fig = plt.figure()
        ax = plt.axes()
        

    # Plot the heatmap
    # im = ax.imshow(data, vmin=None, vmax=None, origin='lower', **kwargs)
    
    # Plot the heatmap
    im = ax.imshow(data, interpolation='lanczos', vmin=None, vmax=None, origin='lower', **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, labelpad=20, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    # ax.set_xticklabels(col_labels)
    # ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=False, bottom=True,
                   labeltop=False, labelbottom=True)

    # Rotate the tick labels and set their alignment.
    # plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             # rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    #ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)
    
    ax.set_ylabel('Elevacion')
    ax.set_xlabel('Azimut')
    
    #plt.cla()
    ax.set_title(title)
    
    fig.show()
    
    return im, cbar