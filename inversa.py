#!/usr/bin/python3
# -*- coding: utf8 -*-
"""


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

from lector_matrices import *

from utilidades.matriz import *


def main(argv):
	while True:
		raw_matrix = ingresar()
		matriz = convertir(raw_matrix)
		matriz = Matriz(matriz)
		if not matriz.cuadrada:
			while True:
				print(
					"Ha proporcionado una matriz rectangular\nPara obtener una inversa es necesario que ingrese una "
					"matriz cuadrada")
				opc = input("1.- Reintentar\n2.- Salir")
				if opc == '1':
					break
				if opc == '2':
					return
		else:
			break
	inver = matriz.inversa(True)
	print("\nSe encrontro la matriz inversa A^-1 = ")
	print(inver)


if __name__ == '__main__':
	main(sys.argv)


