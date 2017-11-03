#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
sumas_riemman.py 

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

import sys
from utilidades.lectores import leer_intervalo, leer_csignif
from utilidades.util import calc_toler
from utilidades.funciones import *
from utilidades.lector_polinomios import Lector_polinomios


def print_lib_missing():
    print(
    """
    ===========================================================================================
    ¡¡¡ Su sistema no cuenta con las bibliotecas necesarias para graficar. !!!
    
    Para acceder a las funciones de graficación por favor instale:
    
    python3-mathplotlib >= 1.5.1
    
    e intentelo de nuevo.
    ===========================================================================================""")


try:
    from matplotlib import pyplot
except ImportError:
    print_lib_missing()
    pyplot = None


def graficar(f=Funcion, n=2, a=0, b=1):
    if pyplot is None:
        print_lib_missing()
        exit(0)
    else:
        print("atender ToDo")


def riemman(f=Funcion(), n=2, a=0, b=1):
    delta_x = (b - a) / n
    area = 0
    for i in range(n):
        area += f.evaluar(a + delta_x * i)
    return area * delta_x


def integrar(f=Funcion(), a=0, b=1, toler=0.5):
    error = toler * 2
    n = 1
    area_calc = 0
    F = f.integrar()
    area_real = F.evaluar(b) - F.evaluar(a)
    while error > toler:
        area_calc = riemman(f, n, a, b)
        error = 100 * (area_real - area_calc) / area_real
        n += 1
    return area_calc, n


def main(argv):
    c_signif = leer_csignif()
    toler = calc_toler(c_signif)
    a, b = leer_intervalo()
    lect_func = LectorFunciones()
    f = lect_func.leer_funcion()
    area, n = integrar(f, a, b, toler)
    graficar(f, n, a, b)


if __name__ == '__main__':
    main(sys.argv)



