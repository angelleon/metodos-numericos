#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
gauss_jordan.py

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

from utilidades.lector_matrices import LectorMatrices


def preguntar_usar_fracciones():
    while True:
        answ = input("""
        Desea usar Fracciones (por defecto Sí)\n1\tSí\n2\tNo\n3\tSalir\n(opción): """)
        try:
            answ = int(answ)
        except ValueError:
            if len(answ) == 0:
                return True
            continue
        if answ == 1:
            return True
        elif answ == 2:
            return False
        elif answ == 3:
            raise KeyboardInterrupt


def main(argv):
    lector = LectorMatrices(cuadrada=True, fracciones=preguntar_usar_fracciones())
    matriz = lector.leer_matriz()
    matriz.determinar()
    if matriz.det == 0:
        print("La matriz no tiene inversa")
    else:
        matriz = matriz.inversa()
        print("Se encontró la inversa de la matriz A como A^-1 = \n\n")
        print(matriz)


if __name__ == '__main__':
    while True:
        try:
                main(sys.argv)
        except KeyboardInterrupt:
            print("\n\nSaliendo...")
            break
        except Exception:
            pass


"""
Escribir un programa que lea un S.E.L.
cuadrado e implemente los metodos de:
-> Gauss-Jordan
-> Jacobi
-> Gauss-Seidel
para resolverlo
el programa deberá verificar si los dos últimos métodos pueden implementarse
en caso negativo notificará al ususario
imprimirá la solución obtenida por cada metodo
el tiempo de ejecución y la cantidad de iteraciones
"""

