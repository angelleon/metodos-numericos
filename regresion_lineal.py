#!/usr/bin/python3
# -*- coding: utf8 -*-

"""
regresion_lineal

Copyright 2017 Angel Leon <luianglenlop@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
"""


import os
import sys
import logging as log
import stat
from utilidades.lector_puntos import AnalizadorSintactico, ErrorLexico, ErrorSintactico
from utilidades.lectores import leer_entero
import utilidades.funciones as funcion
from utilidades.matriz import Matriz, Renglon
try:
    from matplotlib import pyplot as plot
except ImportError:
    plot = None


def set_logging_level(level=log.DEBUG, start_msg="Iniciando depuración"):
    log.basicConfig(level=level)
    log.debug(start_msg)


def print_lib_missing():
    print(
        """
        ===========================================================================================
        ¡¡¡ Su sistema no cuenta con las bibliotecas necesarias para graficar. !!!

        Para acceder a las funciones de graficación por favor instale:

        python3-matplotlib >= 1.5.1

        e intentelo de nuevo.
        ===========================================================================================""")


def check_files(f_list):
    for f_name in f_list:
        if not os.path.isfile(f_name):
            log.critical("No existe el archivo: {}".format(f_name))
            exit(1)
        else:
            st = os.stat(f_name)
            if not bool(st.st_mode & stat.S_IREAD):
                log.critical("No se puede leer el archivo {}".format(f_name))
                exit(1)
            if st.st_size > 262144: # comprueba archivos mayores a 256 KiB
                log.critical("El archivo\n{}\nsupera el tamaño admitido".format(f_name))
                exit(1)


def check_argv(argv):
    if len(argv) == 1:
        log.critical("No se ha especificado ningun archivo del cual leer los puntos")
        exit(1)
    argv = argv[1:]
    opciones = []
    verbose = False
    for i in range(len(argv)):
        if argv[i] == "-v":
            set_logging_level()
            opciones.append(i)
            verbose = True
    if not verbose:
        set_logging_level(log.CRITICAL)
    cont = 0
    for i in opciones:
        argv.pop(i - cont)
        cont += 1
    check_files(argv)
    return argv


def graficar(p: funcion.Polinomio, x_vect: list, y_vect: list):
    input("Presione <Enter> para mostrar la grafica")
    if plot is None:
        print_lib_missing()
    else:
        N = len(x_vect)
        if N < 100:
            n = 100
        else:
            n = N * 3
        x_min = min(x_vect)
        x_max = max(x_vect)
        intervalo = x_max - x_min
        x_0 = x_min - intervalo * 0.2
        x_f = x_max + intervalo * 0.2
        delta_x = intervalo / n
        fig, ax = plot.subplots(1)
        # for x_i, y_i in x_vect, y_vect:
        #    ax.scatter((x_i,), (y_i,), color="blue")
        ax.scatter(x_vect, y_vect, color="blue")
        x_vals = [x_0 + delta_x * i for i in range(int((x_f - x_0) / delta_x))]
        y_vals = [p.evaluar(x_i) for x_i in x_vals]
        ax.plot(x_vals, y_vals, color="magenta")
        plot.show()


def print_resultados(p: funcion.Polinomio, N: int, n_files: int):
    print("\n=========================================================================================================")
    print()
    print("Se encontró la recta de regresión:")
    print("P(x) = {}".format(str(p)))
    print("Al leer una coleccion de {0} puntos desde {1} archivo{2}".format(N, n_files, ("" if n_files == 1 else "s")))
    print()
    print("=========================================================================================================\n")


def leer_puntos(f_list: list) -> (list, list):
    x_vect = []
    y_vect = []
    for f_name in f_list:
        with open(f_name, "r") as f:
            lineas = f.read()
            an_sint = AnalizadorSintactico(lineas)
            while True:
                x_i, y_i = an_sint.punto()
                if x_i is not None:
                    x_vect.append(x_i)
                    y_vect.append(y_i)
                if an_sint.vacio:
                    break
    return x_vect, y_vect


def llenar_matriz(sumas: dict, n: int) -> Matriz:
    key = "x^"
    reng = []
    for i in range(n + 1):
        r = []
        for j in range(n + 1):
            r.append(sumas[key + str(j + i)])
        reng.append(Renglon(r))
    key = 'yx^'
    reng_indep = [Renglon((sumas[key + str(i)],)) for i in range(n + 1)]
    return Matriz(reng, reng_indep)


def calcular_sumas(x_vect: list, y_vect: list, n: int) -> dict:
    sumas = {}
    key = "x^"
    for potencia in range(2 * n + 1):
        suma = 0
        for x_i in x_vect:
            suma += x_i ** potencia
        sumas[key + str(potencia)] = suma
    key = 'yx^'
    for potencia in range(n + 1):
        suma = 0
        for x_i, y_i in zip(x_vect, y_vect):
            suma += y_i * x_i ** potencia
        sumas[key + str(potencia)] = suma
    return sumas


def minimos_cuadrados(x_vect: list, y_vect: list, n: int) -> funcion.Polinomio:
    sumas = calcular_sumas(x_vect, y_vect, n)
    m_aum = llenar_matriz(sumas, n)
    m_aum.gauss_jordan()
    log.debug(repr(m_aum))
    coef = [m_aum.reng_aum[i][0] for i in range(n + 1)]
    poly = funcion.Polinomio(coef[::-1], [exp for exp in range(n + 1)][::-1])
    return poly


def main(argv):
    f_list = check_argv(argv[:])
    x_vect, y_vect = leer_puntos(f_list)
    cont = 1
    for x_i, y_i in zip(x_vect, y_vect):
        log.debug("P{0}: ({1}, {2})".format(cont, x_i, y_i))
        cont += 1
    N = len(x_vect)
    n = 1
    p = minimos_cuadrados(x_vect, y_vect, n)
    print_resultados(p, N, len(f_list))
    graficar(p, x_vect, y_vect)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print("Interrumpido por el usuario\nSaliendo...")
