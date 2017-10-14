#!/usr/bin/python3

"""
reduccion_gaussiana.py

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

from utilidades.lector_matrices import *
from utilidades.matriz import *


def imprimir_ayuda():
    texto_ayuda =\
"""Uso:
    Este programa es interactivo. Simplemente ejecute
        
        ./reduccion_gaussiana.py
        
        o
        
        python3 reduccion_gaussiana.py
"""


def main(argv):
    raw_matrix = ingresar()
    matriz = convertir(raw_matrix)
    for i in matriz:
        for j in i:
            print(j, end=' ')
        print("")
    matriz = Matriz(matriz)
    matriz.reduccion_gaussiana(True)
    print("")
    print(matriz)


if __name__ == '__main__':
    main(sys.argv)
